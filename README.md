# Evaluating Perceptual Audio Encoding Performance

## Technical Tasks & Live Demo Output

A comprehensive dashboard for evaluating audio compression performance at multiple bitrates with real-time analysis and visualization.

## Team
- Triệu Tiến Nguyên (202414651)
- Nguyễn Lâm Tuấn Linh (202414637)

## What It Does

This project implements a complete audio compression analysis system:

### 🔧 Technical Tasks
1. **Encode audio at multiple bitrates** using FFmpeg MP3 encoding
2. **Extract waveform & spectrogram** visualizations for quality assessment
3. **Compute SNR/bitrate metrics** to quantify compression quality
4. **Compare speech vs music** performance across different audio types
5. **Build interactive visualization dashboard** with Streamlit

### 🎯 Live Demo Output
- **Students load 2-3 audio files** through the web interface
- **Run encoding live** with real-time progress tracking
- **System displays bitrate, compression ratio, SNR** in interactive tables and charts
- **Show spectrogram comparison** between original and compressed audio
- **Play original vs compressed** audio for subjective quality assessment

## Quick Start

### Requirements
- Python 3.8+
- FFmpeg (for MP3 encoding)

### Installation
```bash
pip install -r requirements.txt
```

### Install FFmpeg
**Windows:** Download from https://ffmpeg.org/download.html
**macOS:** `brew install ffmpeg`
**Linux:** `sudo apt install ffmpeg`

### Run
```bash
python main.py
```
Open http://localhost:8501

## Usage

1. **Upload** audio files (WAV/MP3 format)
2. **Navigate** between sections:
   - **Home**: Project overview and instructions
   - **Visualization**: Compare waveforms and spectrograms of two audio files
   - **Compression & Analysis**: Encode at multiple bitrates and analyze quality
3. **Select** bitrates to test (32, 64, 96, 128, 192, 256, 320 kbps)
4. **Click** "Encode & Analyze" for real-time processing
5. **View** results: compression ratios, SNR values, and audio playback comparison

## Key Features

### 🎵 Audio Playback
- Listen to original vs compressed audio
- Compare subjective quality at different bitrates
- Side-by-side playback controls

### 📊 Quality Metrics
- **Signal-to-Noise Ratio (SNR)**:
  - **>30 dB**: Excellent quality (transparent)
  - **20-30 dB**: Good quality (minor artifacts)
  - **10-20 dB**: Acceptable quality (noticeable compression)
  - **<10 dB**: Poor quality (significant distortion)

### 📈 Compression Ratio
- Measures file size reduction
- Higher ratios = better compression
- Trade-off with audio quality

### 🔍 Visual Analysis
- **Waveform comparison**: Time-domain representation
- **Spectrogram comparison**: Frequency-domain analysis
- **Metrics visualization**: Charts showing quality vs bitrate trade-offs

## Project Structure

```
├── main.py                 # Entry point
├── src/
│   ├── dashboard.py        # Streamlit web interface
│   ├── encoder.py          # MP3 encoding functionality
│   ├── decoder.py          # Audio decoding
│   ├── metrics.py          # Quality calculations
│   ├── visualization.py    # Plotting functions
│   └── utils.py           # Helper functions
├── data/original/         # Input audio files
├── output/
│   ├── encoded/          # Compressed MP3 files
│   ├── decoded/          # Decoded WAV files
│   ├── reports/          # Analysis reports
│   └── spectrogram/      # Generated plots
└── requirements.txt      # Python dependencies
```

## Educational Value

This project demonstrates:
- **Perceptual audio coding** principles
- **Lossy compression** techniques
- **Quality assessment** methodologies
- **Real-time data processing** and visualization
- **Web application development** with Streamlit

Perfect for computer science and audio engineering students learning about multimedia compression and signal processing.
- **4:1** = file is 1/4 original size
- Higher ratios = more compression = smaller files

## Project Structure
```
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── src/
│   ├── dashboard.py     # Web interface
│   ├── encoder.py       # MP3 encoding
│   ├── decoder.py       # Audio decoding
│   ├── metrics.py       # Quality calculations
│   └── visualization.py # Plots
└── data/original/       # Input audio files
```

## Dependencies
- librosa: Audio processing
- numpy: Numerical operations
- scipy: Signal processing
- matplotlib: Plotting
- streamlit: Web interface
- soundfile: Audio I/O
- ffmpeg-python: MP3 encoding
