import os
import streamlit as st
import numpy as np
import librosa
import matplotlib.pyplot as plt
from scipy import signal
from src.encoder import encode_audio
from src.decoder import decode_audio, verify_audio_quality
from src.metrics import compute_compression_ratio, compute_snr
from src.visualization import compare_waveforms, compare_spectrograms
from src.utils import (
    ensure_directories, save_uploaded_tempfile, format_bytes, get_project_root,
    get_adaptive_sample_count, downsample_audio_for_display, prepare_audio_for_spectrogram
)


def page_home():
    """Home page with project overview and instructions."""
    st.title("🎵 Audio Compression & Analysis Dashboard")
    
    st.markdown("""
    ## Project Overview
    This dashboard evaluates the performance of perceptual audio encoding at multiple bitrates.
    
    ### Features:
    - **Encode** audio files at multiple bitrates using FFmpeg
    - **Decode** compressed audio back to WAV format
    - **Analyze** compression metrics (ratio, SNR)
    - **Visualize** waveforms and spectrograms
    - **Compare** original vs. compressed audio quality
    
    ### How to Use:
    1. Navigate to **Compression & Analysis** to upload and process audio files
    2. Use **Visualization** to view waveforms and spectrograms
    3. Monitor compression ratio and SNR metrics in the reports
    
    ### Requirements:
    - Audio files should be in WAV or MP3 format
    - FFmpeg must be installed for MP3 encoding: https://ffmpeg.org/download.html
    """)
    
    st.info("💡 **Tip:** Use the sidebar to navigate between different sections of the dashboard.")


def page_visualization():
    """Visualization page for waveforms and spectrograms."""
    st.title("📊 Visualization")
    
    st.markdown("### Load and Visualize Audio Files")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file_1 = st.file_uploader("Upload First Audio File", type=['wav', 'mp3'], key="file1")
    
    with col2:
        uploaded_file_2 = st.file_uploader("Upload Second Audio File", type=['wav', 'mp3'], key="file2")
    
    if uploaded_file_1 and uploaded_file_2:
        try:
            # Save temporary files
            temp_file_1 = save_uploaded_tempfile(uploaded_file_1)
            temp_file_2 = save_uploaded_tempfile(uploaded_file_2)
            
            # Load audio data
            y1, sr1 = librosa.load(temp_file_1, sr=None)
            y2, sr2 = librosa.load(temp_file_2, sr=None)
            
            # Display file information
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"File 1: {uploaded_file_1.name}")
                st.write(f"Sample Rate: {sr1} Hz")
                st.write(f"Duration: {len(y1) / sr1:.2f} seconds")
                st.write(f"File Size: {format_bytes(uploaded_file_1.size)}")
                st.audio(temp_file_1)
            
            with col2:
                st.subheader(f"File 2: {uploaded_file_2.name}")
                st.write(f"Sample Rate: {sr2} Hz")
                st.write(f"Duration: {len(y2) / sr2:.2f} seconds")
                st.write(f"File Size: {format_bytes(uploaded_file_2.size)}")
                st.audio(temp_file_2)
            
            # Visualization options
            viz_option = st.radio("Select Visualization:", ["Waveforms", "Spectrograms", "Both"])
            
            if viz_option in ["Waveforms", "Both"]:
                st.subheader("🌊 Waveforms Comparison")
                
                # Progress indicator for processing
                with st.spinner("Preparing waveforms..."):
                    # Get adaptive sample counts
                    start_idx_1, samples_to_show_1, decimate_1 = get_adaptive_sample_count(len(y1), sr1)
                    start_idx_2, samples_to_show_2, decimate_2 = get_adaptive_sample_count(len(y2), sr2)
                    
                    # Prepare data for display
                    y1_display = downsample_audio_for_display(y1[start_idx_1:start_idx_1+samples_to_show_1], decimate_1)
                    y2_display = downsample_audio_for_display(y2[start_idx_2:start_idx_2+samples_to_show_2], decimate_2)
                    
                    # Create figure
                    fig, axes = plt.subplots(2, 1, figsize=(12, 6))
                    
                    # Plot waveform 1
                    axes[0].plot(y1_display)
                    duration_1 = len(y1) / sr1
                    display_duration_1 = samples_to_show_1 / sr1
                    if duration_1 > 30:
                        axes[0].set_title(f"Waveform - {uploaded_file_1.name} (showing first {display_duration_1:.1f}s of {duration_1:.1f}s)")
                    else:
                        axes[0].set_title(f"Waveform - {uploaded_file_1.name} ({duration_1:.2f}s)")
                    axes[0].set_xlabel("Sample")
                    axes[0].set_ylabel("Amplitude")
                    axes[0].grid(True, alpha=0.3)
                    
                    # Plot waveform 2
                    axes[1].plot(y2_display)
                    duration_2 = len(y2) / sr2
                    display_duration_2 = samples_to_show_2 / sr2
                    if duration_2 > 30:
                        axes[1].set_title(f"Waveform - {uploaded_file_2.name} (showing first {display_duration_2:.1f}s of {duration_2:.1f}s)")
                    else:
                        axes[1].set_title(f"Waveform - {uploaded_file_2.name} ({duration_2:.2f}s)")
                    axes[1].set_xlabel("Sample")
                    axes[1].set_ylabel("Amplitude")
                    axes[1].grid(True, alpha=0.3)
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Display info about waveforms shown
                    if samples_to_show_1 < len(y1) or samples_to_show_2 < len(y2):
                        st.info(f"📊 Large files: Showing first 60 seconds to preserve waveform detail. Use the compression analysis page to process full files.")
            
            if viz_option in ["Spectrograms", "Both"]:
                st.subheader("📈 Spectrograms Comparison")
                
                # Progress indicator for processing
                with st.spinner("Computing spectrograms (this may take a moment for large files)..."):
                    # Prepare audio for efficient spectrogram computation
                    y1_spec, params1, sr1_spec = prepare_audio_for_spectrogram(y1, sr1)
                    y2_spec, params2, sr2_spec = prepare_audio_for_spectrogram(y2, sr2)
                    
                    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
                    
                    # Spectrogram 1
                    f, t, Sxx = signal.spectrogram(y1_spec, fs=sr1_spec, nperseg=params1['nperseg'], noverlap=params1['noverlap'])
                    im1 = axes[0].pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap="viridis")
                    axes[0].set_ylabel('Frequency [Hz]')
                    duration_1 = len(y1) / sr1
                    display_duration_1 = params1['max_duration']
                    if duration_1 > 300:
                        axes[0].set_title(f"Spectrogram - {uploaded_file_1.name} (first {display_duration_1:.0f}s of {duration_1:.1f}s)")
                    else:
                        axes[0].set_title(f"Spectrogram - {uploaded_file_1.name} ({duration_1:.2f}s)")
                    cbar1 = plt.colorbar(im1, ax=axes[0], label='Power [dB]')
                    
                    # Spectrogram 2
                    f, t, Sxx = signal.spectrogram(y2_spec, fs=sr2_spec, nperseg=params2['nperseg'], noverlap=params2['noverlap'])
                    im2 = axes[1].pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap="viridis")
                    axes[1].set_ylabel('Frequency [Hz]')
                    axes[1].set_xlabel('Time [s]')
                    duration_2 = len(y2) / sr2
                    display_duration_2 = params2['max_duration']
                    if duration_2 > 300:
                        axes[1].set_title(f"Spectrogram - {uploaded_file_2.name} (first {display_duration_2:.0f}s of {duration_2:.1f}s)")
                    else:
                        axes[1].set_title(f"Spectrogram - {uploaded_file_2.name} ({duration_2:.2f}s)")
                    cbar2 = plt.colorbar(im2, ax=axes[1], label='Power [dB]')
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Display optimization info
                    if params1['max_samples'] < len(y1) or params2['max_samples'] < len(y2):
                        st.warning(f"⚡ **Large files detected:** Only the first {params1['max_duration']:.0f}s is shown for performance. Use the compression analysis page for complete file analysis.")
        
        except Exception as e:
            st.error(f"Error processing files: {str(e)}")


def page_compression():
    """Compression and Analysis page."""
    st.title("🔧 Compression & Analysis")
    
    st.markdown("### Encode, Decode, and Analyze Audio Files")
    
    # File upload
    uploaded_file = st.file_uploader("Upload an audio file", type=['wav', 'mp3'], key="compression_file")
    
    if uploaded_file:
        try:
            # Save temporary file
            temp_input = save_uploaded_tempfile(uploaded_file)
            
            # Load audio info
            y, sr = librosa.load(temp_input, sr=None)
            original_size = os.path.getsize(temp_input)
            
            st.subheader("📁 File Information")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Sample Rate", f"{sr} Hz")
            with col2:
                st.metric("Duration", f"{len(y) / sr:.2f} s")
            with col3:
                st.metric("Original Size", format_bytes(original_size))
            
            # Bitrate selection
            st.subheader("⚙️ Encoding Settings")
            col1, col2 = st.columns(2)
            
            with col1:
                bitrates = st.multiselect(
                    "Select bitrates (kbps):",
                    [32, 64, 96, 128, 192, 256, 320],
                    default=[64, 128, 256]
                )
            
            with col2:
                max_bitrate = sr * 16 // 1000  # Theoretical max based on sample rate
                st.info(f"Max recommended: {max_bitrate} kbps")
            
            if st.button("🚀 Encode & Analyze", key="encode_btn"):
                if not bitrates:
                    st.error("Please select at least one bitrate")
                else:
                    try:
                        # Create output directories
                        project_root = get_project_root()
                        output_dir = os.path.join(project_root, "output", "encoded")
                        decoded_dir = os.path.join(project_root, "output", "decoded")
                        report_dir = os.path.join(project_root, "output", "reports")
                        ensure_directories(output_dir, decoded_dir, report_dir)
                        
                        # Progress tracking
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        results = []
                        total_steps = len(bitrates) * 3  # encode, decode, analyze
                        current_step = 0
                        
                        for i, bitrate in enumerate(bitrates):
                            # Encode
                            status_text.text(f"Encoding at {bitrate} kbps...")
                            encoded_files = encode_audio(temp_input, output_dir, [bitrate])
                            current_step += 1
                            progress_bar.progress(current_step / total_steps)
                            
                            if encoded_files:
                                encoded_file = encoded_files[0]
                                
                                # Decode
                                status_text.text(f"Decoding {bitrate} kbps audio...")
                                base_name = os.path.splitext(os.path.basename(uploaded_file.name))[0]
                                decoded_file = os.path.join(decoded_dir, f"{base_name}_{bitrate}kbps_decoded.wav")
                                decode_audio(encoded_file, decoded_file)
                                current_step += 1
                                progress_bar.progress(current_step / total_steps)
                                
                                # Analyze
                                status_text.text(f"Analyzing quality metrics...")
                                report_file = os.path.join(report_dir, f"{base_name}_{bitrate}kbps_analysis.txt")
                                comp_ratio = compute_compression_ratio(temp_input, encoded_file, report_file)
                                current_step += 1
                                progress_bar.progress(current_step / total_steps)
                                
                                # Compute SNR
                                snr = compute_snr(temp_input, decoded_file)
                                
                                compressed_size = os.path.getsize(encoded_file)
                                
                                results.append({
                                    'bitrate': bitrate,
                                    'compression_ratio': comp_ratio,
                                    'snr': snr,
                                    'original_size': original_size,
                                    'compressed_size': compressed_size,
                                    'encoded_file': encoded_file,
                                    'decoded_file': decoded_file
                                })
                        
                        status_text.text("✅ Analysis Complete!")
                        progress_bar.progress(1.0)
                        
                        # Display results
                        st.subheader("📊 Analysis Results")
                        
                        # Results table
                        results_data = []
                        for r in results:
                            results_data.append({
                                'Bitrate (kbps)': r['bitrate'],
                                'Compression Ratio': f"{r['compression_ratio']:.2f}x",
                                'SNR (dB)': f"{r['snr']:.2f}" if r['snr'] != float('inf') else "∞",
                                'Original Size': format_bytes(r['original_size']),
                                'Compressed Size': format_bytes(r['compressed_size'])
                            })
                        
                        st.dataframe(results_data, use_container_width=True)
                        
                        # Audio Playback Section
                        st.subheader("🎵 Audio Playback & Comparison")
                        st.markdown("Compare original vs compressed audio quality:")
                        
                        # Original audio playback
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Original Audio:**")
                            try:
                                st.audio(temp_input)
                            except Exception as e:
                                st.error(f"Could not load original audio: {str(e)}")
                        
                        # Compressed audio options
                        with col2:
                            st.markdown("**Compressed Audio:**")
                            selected_bitrate = st.selectbox(
                                "Select bitrate to play:",
                                [r['bitrate'] for r in results],
                                key="playback_bitrate"
                            )
                            
                            # Find selected result
                            selected_result = next(r for r in results if r['bitrate'] == selected_bitrate)
                            
                            try:
                                st.audio(selected_result['decoded_file'])
                                st.caption(f"Playing {selected_bitrate} kbps compressed audio")
                            except Exception as e:
                                st.error(f"Could not load compressed audio: {str(e)}")
                        
                        # Quality comparison metrics for selected bitrate
                        st.markdown("---")
                        st.subheader("📈 Quality Metrics for Selected Bitrate")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Bitrate", f"{selected_result['bitrate']} kbps")
                        with col2:
                            st.metric("Compression Ratio", f"{selected_result['compression_ratio']:.2f}x")
                        with col3:
                            snr_display = f"{selected_result['snr']:.2f} dB" if selected_result['snr'] != float('inf') else "∞ dB"
                            st.metric("SNR", snr_display)
                        
                        # Visualization of metrics
                        if len(results) > 1:
                            st.subheader("📈 Metrics Comparison")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                fig, ax = plt.subplots()
                                bitrates_list = [r['bitrate'] for r in results]
                                comp_ratios = [r['compression_ratio'] for r in results]
                                ax.plot(bitrates_list, comp_ratios, marker='o', linewidth=2, markersize=8)
                                ax.set_xlabel("Bitrate (kbps)")
                                ax.set_ylabel("Compression Ratio")
                                ax.set_title("Compression Ratio vs Bitrate")
                                ax.grid(True, alpha=0.3)
                                st.pyplot(fig)
                            
                            with col2:
                                fig, ax = plt.subplots()
                                snr_values = [r['snr'] if r['snr'] != float('inf') else 100 for r in results]
                                ax.plot(bitrates_list, snr_values, marker='s', linewidth=2, markersize=8, color='orange')
                                ax.set_xlabel("Bitrate (kbps)")
                                ax.set_ylabel("SNR (dB)")
                                ax.set_title("Signal-to-Noise Ratio vs Bitrate")
                                ax.grid(True, alpha=0.3)
                                st.pyplot(fig)
                    
                    except Exception as e:
                        st.error(f"Error during encoding/analysis: {str(e)}")
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")


def main():
    """Main dashboard function."""
    st.set_page_config(
        page_title="Audio Compression Dashboard",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to:",
        ["Home", "Visualization", "Compression & Analysis"],
        label_visibility="collapsed"
    )
    
    # Display selected page
    if page == "Home":
        page_home()
    elif page == "Visualization":
        page_visualization()
    elif page == "Compression & Analysis":
        page_compression()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### About
    Audio Compression & Coding Dashboard  
    Evaluating Perceptual Audio Encoding Performance
    
    [GitHub Repository](https://github.com/n9yn/Asssignment-1---Audio-Compression-and-Coding.git)
    """)


if __name__ == "__main__":
    main()
