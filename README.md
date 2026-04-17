# Asssignment-1---Audio-Compression-and-Coding
# Evaluating Perceptual Audio Encoding Performance

## Project Description
This project evaluates the performance of perceptual audio encoding at multiple bitrates.

The system:
- Encodes audio files at multiple bitrates
- Computes Signal-to-Noise Ratio (SNR)
- Generates waveform and spectrogram
- Displays results on a visualization dashboard

## Team Members
- Triệu Tiến Nguyên 202414651
- Nguyễn Lâm Tuấn Linh 202414637

## Tools Used
- Python
- FFmpeg
- Librosa
- Streamlit
- Trello (Project Management)

## Project Structure
src/ → source code  
data/ → input audio  
output/ → generated results (created automatically)

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run the dashboard: `python main.py`
3. Upload an audio file in the Streamlit app and select bitrates to process.