# Assignment-1---Audio-Compression-and-Coding
# Evaluating Perceptual Audio Encoding Performance

**Repository:** [https://github.com/NguyenLamTuanLinh/Asssignment-1---Audio-Compression-and-Coding](https://github.com/NguyenLamTuanLinh/Asssignment-1---Audio-Compression-and-Coding)

## Project Description
This project evaluates the performance of perceptual audio encoding at multiple bitrates.

The system:
- Encodes audio files at multiple bitrates
- Computes Signal-to-Noise Ratio (SNR)
- Generates waveform and spectrogram visualizations
- Provides an interactive dashboard for analysis

## Updates - Phase 3: Metrics & Analysis ✅

### Completed Tasks:
- ✅ **Generate Spectrogram Visualization** (Task breakdown:)
  - ✅ **Extract Waveform**: Load audio data and extract waveform samples
  - ✅ **Plot Waveform**: Create visual representation of audio waveform
  - ✅ **Save Waveform Image**: Save plots to PNG files

### New Features in Visualization Module:
- `extract_waveform()` - Extract audio time series data
- `plot_waveform()` - Create waveform visualization
- `save_waveform_image()` - Save waveform plot to file
- `extract_spectrogram()` - Extract spectrogram data
- `plot_spectrogram()` - Create spectrogram visualization
- `save_spectrogram_image()` - Save spectrogram plot to file

### Dashboard Pages:
1. **Home** - Project overview and instructions
2. **Visualization** - Generate waveform and spectrogram visualizations
3. **Compression & Analysis** - Encode, decode, and analyze audio

## Team Members
- Triệu Tiến Nguyên 202414651
- Nguyễn Lâm Tuấn Linh 202414637

## Tools Used
- Python 3.x
- FFmpeg
- Librosa (audio analysis)
- Matplotlib (visualization)
- SciPy (signal processing)
- Streamlit (dashboard)
- NumPy (numerical computing)

## Project Structure
```
├── main.py                 # Entry point
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── src/                   # Source code
│   ├── dashboard.py      # Streamlit dashboard
│   ├── encoder.py        # Audio encoding functions
│   ├── decoder.py        # Audio decoding functions
│   ├── metrics.py        # Analysis metrics
│   └── visualization.py  # Waveform & spectrogram generation
├── data/
│   └── original/         # Input audio files
└── output/              # Generated results (created automatically)
    ├── encoded/         # Encoded audio files
    ├── decoded/         # Decoded audio files
    ├── reports/         # Analysis reports
    └── visualizations/  # Generated plots
```

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/NguyenLamTuanLinh/Asssignment-1---Audio-Compression-and-Coding.git
   cd Asssignment-1---Audio-Compression-and-Coding
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add audio files to `data/original/` directory

## How to Run

### Start the Dashboard:
```bash
python main.py
```
This launches the Streamlit web interface.

### Usage:
1. Navigate to **Visualization** page to generate plots
2. Navigate to **Compression & Analysis** page to:
   - Upload an audio file
   - Select target bitrates (64, 128, 192, 256, 320 kbps)
   - Process audio: encode → decode → analyze
   - View metrics and visualizations

## Output Files Generated:
- **Encoded files**: `.mp3` files at different bitrates
- **Decoded files**: `.wav` files decoded from compressed audio
- **Reports**: Compression ratio and metrics
- **Visualizations**: PNG images of waveforms and spectrograms

## Key Metrics:
- **Compression Ratio**: Original size / Compressed size
- **SNR (Signal-to-Noise Ratio)**: Quality measure in dB
- **Bitrate**: Target encoding bitrate in kbps