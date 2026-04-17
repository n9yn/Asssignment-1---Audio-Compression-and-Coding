import os
import streamlit as st
import numpy as np
import librosa
import matplotlib.pyplot as plt
from src.encoder import encode_audio
from src.decoder import decode_audio, verify_audio_quality
from src.metrics import compute_compression_ratio, compute_snr, compare_snr
from src.visualization import compare_waveforms, compare_spectrograms
from src.utils import get_project_root, ensure_directories, save_uploaded_tempfile, format_bytes


def compute_signal_to_noise_ratio(signal, noise):
    """
    Computes the Signal-to-Noise Ratio (SNR) in decibels (dB).

    Args:
        signal (numpy.ndarray): The original signal.
        noise (numpy.ndarray): The noise signal.

    Returns:
        float: The SNR value in decibels.
    """
    signal_power = np.mean(np.square(signal))
    noise_power = np.mean(np.square(noise))
    
    if noise_power == 0:
        return float('inf')
    
    snr = 10 * np.log10(signal_power / noise_power)
    return snr


def validate_snr(signal, noise):
    """
    Validates the SNR calculation by ensuring the signal and noise are compatible.

    Args:
        signal (numpy.ndarray): The original signal.
        noise (numpy.ndarray): The noise signal.

    Returns:
        bool: True if validation passes, False otherwise.
    """
    if len(signal) != len(noise):
        return False
    
    if np.any(noise == 0):
        return False
    
    return True


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
            
            with col2:
                st.subheader(f"File 2: {uploaded_file_2.name}")
                st.write(f"Sample Rate: {sr2} Hz")
                st.write(f"Duration: {len(y2) / sr2:.2f} seconds")
                st.write(f"File Size: {format_bytes(uploaded_file_2.size)}")
            
            # Visualization options
            viz_option = st.radio("Select Visualization:", ["Waveforms", "Spectrograms", "Both"])
            
            if viz_option in ["Waveforms", "Both"]:
                st.subheader("🌊 Waveforms Comparison")
                fig, axes = plt.subplots(2, 1, figsize=(12, 6))
                
                axes[0].plot(y1[:5000])  # Plot first 5000 samples
                axes[0].set_title(f"Waveform - {uploaded_file_1.name}")
                axes[0].set_xlabel("Sample")
                axes[0].set_ylabel("Amplitude")
                
                axes[1].plot(y2[:5000])
                axes[1].set_title(f"Waveform - {uploaded_file_2.name}")
                axes[1].set_xlabel("Sample")
                axes[1].set_ylabel("Amplitude")
                
                plt.tight_layout()
                st.pyplot(fig)
            
            if viz_option in ["Spectrograms", "Both"]:
                st.subheader("📈 Spectrograms Comparison")
                from scipy import signal
                
                fig, axes = plt.subplots(2, 1, figsize=(12, 8))
                
                # Spectrogram 1
                f, t, Sxx = signal.spectrogram(y1, fs=sr1)
                im1 = axes[0].pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap="viridis")
                axes[0].set_ylabel('Frequency [Hz]')
                axes[0].set_title(f"Spectrogram - {uploaded_file_1.name}")
                plt.colorbar(im1, ax=axes[0], label='Power [dB]')
                
                # Spectrogram 2
                f, t, Sxx = signal.spectrogram(y2, fs=sr2)
                im2 = axes[1].pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap="viridis")
                axes[1].set_ylabel('Frequency [Hz]')
                axes[1].set_xlabel('Time [s]')
                axes[1].set_title(f"Spectrogram - {uploaded_file_2.name}")
                plt.colorbar(im2, ax=axes[1], label='Power [dB]')
                
                plt.tight_layout()
                st.pyplot(fig)
        
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
    
    [GitHub Repository](https://github.com/NguyenLamTuanLinh/Asssignment-1---Audio-Compression-and-Coding)
    """)


if __name__ == "__main__":
    main()
