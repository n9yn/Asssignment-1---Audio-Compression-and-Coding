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

# ============================================================================
# PHASE 4: SETUP STREAMLIT DASHBOARD
# ============================================================================
# This file implements the main Streamlit dashboard for audio compression
# and analysis. It provides multiple pages for different functionality:
# - Home: Project overview and instructions
# - Visualization: Generate waveform and spectrogram visualizations
# - Compression & Analysis: Encode, decode, and analyze audio
# ============================================================================

# Get project root
project_root = os.path.dirname(os.path.dirname(__file__))

# ============================================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Audio Compression Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #FF6B35;
    }
    
    /* Sidebar styling */
    .css-1d0tpyp {
        background-color: #F0F2F6;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    
    /* Metric styling */
    .metric-card {
        background-color: #F0F2F6;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================
with st.sidebar:
    st.markdown("---")
    st.markdown("## 📋 Navigation")
    st.markdown("---")
    
    # Page selection
    page = st.radio("Select Page", 
                     ["🏠 Home", 
                      "📊 Visualization", 
                      "🎚️ Compression & Analysis"],
                     label_visibility="collapsed")
    
    st.markdown("---")
    
    # Project info section
    with st.expander("ℹ️ Project Information", expanded=False):
        st.markdown("""
        ### Audio Compression & Coding
        
        **Version:** 1.0  
        **Phase:** 4 - Visualization & Dashboard
        
        **Team Members:**
        - Triệu Tiến Nguyên (202414651)
        - Nguyễn Lâm Tuấn Linh (202414637)
        
        **Repository:**  
        [GitHub](https://github.com/n9yn/Asssignment-1---Audio-Compression-and-Coding)
        """)
    
    # Quick links
    with st.expander("🔗 Quick Links", expanded=False):
        st.markdown("""
        - [Project Repo](https://github.com/n9yn/Asssignment-1---Audio-Compression-and-Coding)
        - [Documentation](https://github.com/n9yn/Asssignment-1---Audio-Compression-and-Coding#readme)
        """)
    
    # Settings section
    with st.expander("⚙️ Settings", expanded=False):
        st.write("**Display Options:**")
        show_debug = st.checkbox("Show debug information", value=False)
        max_upload_size = st.slider("Max upload size (MB)", 10, 500, 100)

# ============================================================================
# PAGE ROUTING
# ============================================================================

# Extract page name (remove emoji)
page_name = page.split(" ", 1)[1]

if page_name == "Home":
    # ========================================================================
    # HOME PAGE
    # ========================================================================
    st.title("🎵 Audio Compression and Coding Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Welcome to the Dashboard
        
        This comprehensive audio compression analysis tool enables you to:
        - **Encode** audio files at multiple bitrates
        - **Analyze** compression metrics (SNR, compression ratio)
        - **Visualize** waveforms and spectrograms
        - **Compare** original vs. compressed audio quality
        
        ### 🚀 Getting Started
        1. Go to the **Visualization** page to generate audio plots
        2. Visit **Compression & Analysis** to process your audio files
        3. Select compression parameters and view detailed results
        """)
    
    with col2:
        st.info("""
        ### 📌 Quick Stats
        - **Total Pages:** 3
        - **Supported Formats:** WAV, MP3, FLAC
        - **Bitrate Options:** 64-320 kbps
        - **Metrics:** SNR, Compression Ratio
        """)
    
    st.markdown("---")
    
    # Features section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🌊 Waveform Visualization
        Extract, plot, and save waveform images
        for audio analysis and comparison.
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Spectrogram Analysis
        Generate high-quality spectrogram
        visualizations with frequency domain analysis.
        """)
    
    with col3:
        st.markdown("""
        ### 📈 Quality Metrics
        Compute SNR and compression ratios
        for objective audio quality assessment.
        """)
    
    st.markdown("---")
    st.markdown("### 📚 Learn More")
    st.markdown("""
    - Need help? Check the [documentation](https://github.com/n9yn/Asssignment-1---Audio-Compression-and-Coding#readme)
    - Report issues on [GitHub Issues](https://github.com/n9yn/Asssignment-1---Audio-Compression-and-Coding/issues)
    """)

elif page_name == "Visualization":
    # ========================================================================
    # VISUALIZATION PAGE
    # ========================================================================
    st.title("📊 Spectrogram Visualization Tool")
    
    st.markdown("""
    ### Task Breakdown: Extract → Plot → Save
    
    This tool allows you to generate high-quality waveform and spectrogram visualizations
    for audio files. The process includes three main steps:
    
    1. **Extract** - Load and extract audio data
    2. **Plot** - Generate visual representation
    3. **Save** - Save plots to PNG files
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Choose an audio file for visualization", 
                                        type=["wav", "mp3", "flac"],
                                        help="Upload WAV, MP3, or FLAC file")
    
    with col2:
        if uploaded_file is not None:
            file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
            st.metric("File Size", f"{file_size_mb:.2f} MB")
    
    if uploaded_file is not None:
        # Save uploaded file to temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.read())
            audio_file = tmp_file.name
        
        st.success("✅ File uploaded successfully!")
        
        st.markdown("---")
        
        # Visualization options
        st.markdown("### Select Visualizations to Generate:")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🌊 Generate Waveform", key="waveform_btn", use_container_width=True):
                with st.spinner("⏳ Extracting and processing waveform..."):
                    try:
                        # Task 1: Extract waveform
                        y, sr = extract_waveform(audio_file)
                        st.info(f"✓ Task 1 - Waveform extracted")
                        st.caption(f"📊 {len(y):,} samples at {sr} Hz")
                        
                        # Task 2: Plot waveform
                        fig = plot_waveform(y, sr)
                        st.info("✓ Task 2 - Waveform plot generated")
                        st.pyplot(fig, use_container_width=True)
                        
                        # Task 3: Save waveform
                        output_dir = os.path.join(project_root, "output", "visualizations")
                        output_path = os.path.join(output_dir, f"{os.path.splitext(uploaded_file.name)[0]}_waveform.png")
                        save_waveform_image(fig, output_path)
                        st.success(f"✓ Task 3 - Waveform saved")
                        st.caption(f"📁 {output_path}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                    finally:
                        # Cleanup
                        if os.path.exists(audio_file):
                            os.unlink(audio_file)
        
        with col2:
            if st.button("📊 Generate Spectrogram", key="spectrogram_btn", use_container_width=True):
                with st.spinner("⏳ Extracting and processing spectrogram..."):
                    try:
                        # Extract spectrogram
                        S_db, sr = extract_spectrogram(audio_file)
                        st.info(f"✓ Spectrogram extracted")
                        st.caption(f"📊 Shape: {S_db.shape}")
                        
                        # Plot spectrogram
                        fig = plot_spectrogram(S_db, sr)
                        st.info("✓ Spectrogram plot generated")
                        st.pyplot(fig, use_container_width=True)
                        
                        # Save spectrogram
                        output_dir = os.path.join(project_root, "output", "visualizations")
                        output_path = os.path.join(output_dir, f"{os.path.splitext(uploaded_file.name)[0]}_spectrogram.png")
                        save_spectrogram_image(fig, output_path)
                        st.success(f"✓ Spectrogram saved")
                        st.caption(f"📁 {output_path}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                    finally:
                        # Cleanup
                        if os.path.exists(audio_file):
                            os.unlink(audio_file)
    else:
        st.info("👆 Start by uploading an audio file above")

else:  # Compression & Analysis page
    # ========================================================================
    # COMPRESSION & ANALYSIS PAGE
    # ========================================================================
    st.title("🎚️ Audio Compression & Analysis")
    
    st.markdown("""
    ### Comprehensive Compression Pipeline
    
    Upload an audio file, select compression parameters, and analyze the results:
    - **Encode** at multiple bitrates
    - **Decode** and reconstruct
    - **Measure** quality metrics
    - **Visualize** original vs. compressed
    """)
    
    st.markdown("---")
    
    uploaded_file = st.file_uploader("Choose an audio file for compression", 
                                    type=["wav", "mp3", "flac"],
                                    key="compression_upload",
                                    help="Upload WAV, MP3, or FLAC file")

    if uploaded_file is not None:
        # Save uploaded file to temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.read())
            original_file = tmp_file.name

        st.sidebar.success("✓ File uploaded successfully!")
        
        st.markdown("---")

        # Compression settings in sidebar
        st.sidebar.markdown("### ⚙️ Compression Settings")
        bitrates = st.sidebar.multiselect(
            "Select bitrates (kbps)",
            [64, 128, 192, 256, 320],
            default=[128, 256],
            help="Select one or more bitrates for compression"
        )

        if st.sidebar.button("▶️ Process Audio", use_container_width=True):
            if not bitrates:
                st.error("❌ Please select at least one bitrate")
            else:
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
                with st.spinner("🔄 Encoding audio..."):
                    encode_audio(original_file, encoded_dir, bitrates)

                results = []

                for bitrate in bitrates:
                    encoded_file = os.path.join(encoded_dir, f"{os.path.splitext(os.path.basename(original_file))[0]}_{bitrate}kbps.mp3")
                    decoded_file = os.path.join(decoded_dir, f"{os.path.splitext(os.path.basename(original_file))[0]}_{bitrate}kbps_decoded.wav")

                    with st.spinner(f"🔄 Processing {bitrate} kbps..."):
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
                st.markdown("---")
                st.header("📈 Analysis Results")

                # Summary metrics
                st.markdown("### 📊 Summary")
                cols = st.columns(len(results))
                for idx, res in enumerate(results):
                    with cols[idx]:
                        st.metric(f"Bitrate: {res['bitrate']} kbps", f"{res['snr']:.2f} dB", "SNR")

                # Detailed results
                for res in results:
                    with st.expander(f"📌 Details - {res['bitrate']} kbps", expanded=False):
                        # Metrics info
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader(f"Bitrate: {res['bitrate']} kbps")
                            st.metric("SNR (dB)", f"{res['snr']:.2f}")
                        
                        with col2:
                            with open(res['compression_ratio_file'], 'r') as f:
                                st.text(f.read())
                        
                        st.markdown("---")

                        # Visualizations
                        st.markdown("### Visualizations")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Original Audio**")
                            st.image(res['orig_waveform'], caption="Waveform", use_column_width=True)
                            st.image(res['orig_spectrogram'], caption="Spectrogram", use_column_width=True)
                        with col2:
                            st.markdown(f"**Decoded Audio ({res['bitrate']} kbps)**")
                            st.image(res['dec_waveform'], caption="Waveform", use_column_width=True)
                            st.image(res['dec_spectrogram'], caption="Spectrogram", use_column_width=True)

                # Clean up temp file
                os.unlink(original_file)
                st.success("✅ Processing complete!")

    else:
        st.info("👆 Upload an audio file to start compression and analysis")
