import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(__file__))

from encoder import encode_audio
from decoder import decode_audio
from metrics import compute_compression_ratio, compute_snr
from visualization import (generate_waveform_visualization, generate_spectrogram_visualization,
                          extract_waveform, plot_waveform, save_waveform_image,
                          extract_spectrogram, plot_spectrogram, save_spectrogram_image)
import tempfile
import shutil
import matplotlib.pyplot as plt

# Get project root
project_root = os.path.dirname(os.path.dirname(__file__))

st.set_page_config(page_title="Audio Compression Dashboard", layout="wide")
st.title("🎵 Audio Compression and Coding Dashboard")

# Sidebar navigation
page = st.sidebar.radio("Select Page", ["Home", "Compression & Analysis", "Visualization"])

if page == "Home":
    st.markdown("""
    ## Welcome to Audio Compression Dashboard
    
    This application provides comprehensive audio compression and analysis tools:
    
    ### Features:
    - **Compression & Analysis**: Encode audio at different bitrates and analyze compression metrics
    - **Visualization**: Generate waveform and spectrogram visualizations
    
    ### How to use:
    1. Select a page from the sidebar
    2. Upload an audio file
    3. Select your options and process
    
    Start by uploading an audio file!
    """)

elif page == "Visualization":
    st.header("📊 Spectrogram Visualization Tool")
    st.markdown("### Task Breakdown: Extract → Plot → Save")
    
    uploaded_file = st.file_uploader("Choose an audio file for visualization", type=["wav", "mp3", "flac"])
    
    if uploaded_file is not None:
        # Save uploaded file to temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.read())
            audio_file = tmp_file.name
        
        st.success("✓ File uploaded successfully!")
        
        # Visualization options
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🌊 Generate Waveform", key="waveform_btn"):
                with st.spinner("Extracting and processing waveform..."):
                    try:
                        # Task 1: Extract waveform
                        y, sr = extract_waveform(audio_file)
                        st.info(f"✓ Task 1 - Waveform extracted: {len(y)} samples at {sr} Hz")
                        
                        # Task 2: Plot waveform
                        fig = plot_waveform(y, sr)
                        st.info("✓ Task 2 - Waveform plot generated")
                        st.pyplot(fig)
                        
                        # Task 3: Save waveform
                        output_dir = os.path.join(project_root, "output", "visualizations")
                        output_path = os.path.join(output_dir, f"{os.path.splitext(uploaded_file.name)[0]}_waveform.png")
                        save_waveform_image(fig, output_path)
                        st.success(f"✓ Task 3 - Waveform saved to:\n{output_path}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                    finally:
                        # Cleanup
                        if os.path.exists(audio_file):
                            os.unlink(audio_file)
        
        with col2:
            if st.button("📊 Generate Spectrogram", key="spectrogram_btn"):
                with st.spinner("Extracting and processing spectrogram..."):
                    try:
                        # Extract spectrogram
                        S_db, sr = extract_spectrogram(audio_file)
                        st.info(f"✓ Spectrogram extracted: shape {S_db.shape}")
                        
                        # Plot spectrogram
                        fig = plot_spectrogram(S_db, sr)
                        st.info("✓ Spectrogram plot generated")
                        st.pyplot(fig)
                        
                        # Save spectrogram
                        output_dir = os.path.join(project_root, "output", "visualizations")
                        output_path = os.path.join(output_dir, f"{os.path.splitext(uploaded_file.name)[0]}_spectrogram.png")
                        save_spectrogram_image(fig, output_path)
                        st.success(f"✓ Spectrogram saved to:\n{output_path}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                    finally:
                        # Cleanup
                        if os.path.exists(audio_file):
                            os.unlink(audio_file)

else:  # Compression & Analysis page
    st.header("🎚️ Audio Compression & Analysis")
    
    uploaded_file = st.file_uploader("Choose an audio file for compression", type=["wav", "mp3", "flac"], key="compression_upload")

    if uploaded_file is not None:
        # Save uploaded file to temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.read())
            original_file = tmp_file.name

        st.sidebar.success("✓ File uploaded successfully!")

        # Bitrate selection
        bitrates = st.sidebar.multiselect("Select bitrates (kbps)", [64, 128, 192, 256, 320], default=[128, 256])

        if st.sidebar.button("▶️ Process Audio"):
            # Create output directories
            output_dir = os.path.join(project_root, "output")
            encoded_dir = os.path.join(output_dir, "encoded")
            decoded_dir = os.path.join(output_dir, "decoded")
            reports_dir = os.path.join(output_dir, "reports")
            vis_dir = os.path.join(output_dir, "visualizations")
            os.makedirs(encoded_dir, exist_ok=True)
            os.makedirs(decoded_dir, exist_ok=True)
            os.makedirs(reports_dir, exist_ok=True)
            os.makedirs(vis_dir, exist_ok=True)

            # Encode
            with st.spinner("Encoding audio..."):
                encode_audio(original_file, encoded_dir, bitrates)

            results = []

            for bitrate in bitrates:
                encoded_file = os.path.join(encoded_dir, f"{os.path.splitext(os.path.basename(original_file))[0]}_{bitrate}kbps.mp3")
                decoded_file = os.path.join(decoded_dir, f"{os.path.splitext(os.path.basename(original_file))[0]}_{bitrate}kbps_decoded.wav")

                with st.spinner(f"Processing {bitrate} kbps..."):
                    # Decode
                    decode_audio(encoded_file, decoded_file)

                    # Compute metrics
                    compression_ratio_file = os.path.join(reports_dir, f"compression_ratio_{bitrate}kbps.txt")
                    compute_compression_ratio(original_file, encoded_file, compression_ratio_file)

                    snr_value = compute_snr(original_file, decoded_file)

                    # Generate visualizations for original and decoded
                    orig_waveform = os.path.join(vis_dir, "original_waveform.png")
                    orig_spectrogram = os.path.join(vis_dir, "original_spectrogram.png")
                    dec_waveform = os.path.join(vis_dir, f"decoded_waveform_{bitrate}kbps.png")
                    dec_spectrogram = os.path.join(vis_dir, f"decoded_spectrogram_{bitrate}kbps.png")

                    generate_waveform_visualization(original_file, orig_waveform)
                    generate_spectrogram_visualization(original_file, orig_spectrogram)
                    generate_waveform_visualization(decoded_file, dec_waveform)
                    generate_spectrogram_visualization(decoded_file, dec_spectrogram)

                    results.append({
                        "bitrate": bitrate,
                        "snr": snr_value,
                        "compression_ratio_file": compression_ratio_file,
                        "orig_waveform": orig_waveform,
                        "orig_spectrogram": orig_spectrogram,
                        "dec_waveform": dec_waveform,
                        "dec_spectrogram": dec_spectrogram
                    })

            # Display results
            st.header("📈 Analysis Results")

            for res in results:
                st.subheader(f"Bitrate: {res['bitrate']} kbps")
                st.metric("SNR (dB)", f"{res['snr']:.2f}")

                with open(res['compression_ratio_file'], 'r') as f:
                    st.text(f.read())

                col1, col2 = st.columns(2)
                with col1:
                    st.image(res['orig_waveform'], caption="Original Waveform")
                    st.image(res['orig_spectrogram'], caption="Original Spectrogram")
                with col2:
                    st.image(res['dec_waveform'], caption=f"Decoded Waveform ({res['bitrate']} kbps)")
                    st.image(res['dec_spectrogram'], caption=f"Decoded Spectrogram ({res['bitrate']} kbps)")

            # Clean up temp file
            os.unlink(original_file)

    else:
        st.info("📁 Please upload an audio file to start compression and analysis.")