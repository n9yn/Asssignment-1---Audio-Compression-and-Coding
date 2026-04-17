import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import os

def extract_waveform(audio_file):
    """
    [TASK 1] Extracts waveform data from an audio file.

    Args:
        audio_file (str): Path to the audio file.

    Returns:
        tuple: (waveform_data, sample_rate) where waveform_data is the audio time series
               and sample_rate is the sampling rate.
    """
    y, sr = librosa.load(audio_file, sr=None)
    print(f"Waveform extracted from {audio_file}: {len(y)} samples at {sr} Hz")
    return y, sr

def plot_waveform(y, sr, title="Waveform"):
    """
    [TASK 2] Plots the extracted waveform data.

    Args:
        y (np.ndarray): Audio time series.
        sr (int): Sampling rate.
        title (str): Title for the waveform plot. Default is "Waveform".

    Returns:
        matplotlib.figure.Figure: The figure object containing the plot.
    """
    fig = plt.figure(figsize=(12, 4))
    librosa.display.waveshow(y, sr=sr)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    print("Waveform plot generated")
    return fig

def save_waveform_image(fig, output_image_path):
    """
    [TASK 3] Saves the waveform plot to an image file.

    Args:
        fig (matplotlib.figure.Figure): The figure object to save.
        output_image_path (str): Path to save the waveform image.

    Returns:
        str: The path to the saved waveform image.
    """
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    fig.savefig(output_image_path, dpi=100, bbox_inches='tight')
    plt.close(fig)  # Close the figure to free memory
    print(f"Waveform image saved to {output_image_path}")
    return output_image_path

def generate_waveform_visualization(audio_file, output_image_path, title="Waveform"):
    """
    Generates a waveform visualization for the given audio file and saves it as an image.
    This is a convenience function that combines extract, plot, and save operations.

    Args:
        audio_file (str): Path to the audio file.
        output_image_path (str): Path to save the waveform image.
        title (str): Title for the waveform plot. Default is "Waveform".

    Returns:
        str: The path to the saved waveform image.
    """
    # Task 1: Extract waveform
    y, sr = extract_waveform(audio_file)
    
    # Task 2: Plot waveform
    fig = plot_waveform(y, sr, title=title)
    
    # Task 3: Save waveform image
    return save_waveform_image(fig, output_image_path)

def extract_spectrogram(audio_file):
    """
    Extracts spectrogram data from an audio file.

    Args:
        audio_file (str): Path to the audio file.

    Returns:
        tuple: (spectrogram_db, sample_rate) where spectrogram_db is the spectrogram in dB scale
               and sample_rate is the sampling rate.
    """
    y, sr = librosa.load(audio_file, sr=None)
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    print(f"Spectrogram extracted from {audio_file}: shape {S_db.shape}")
    return S_db, sr

def plot_spectrogram(S_db, sr, title="Spectrogram"):
    """
    Plots the extracted spectrogram data.

    Args:
        S_db (np.ndarray): Spectrogram in dB scale.
        sr (int): Sampling rate.
        title (str): Title for the spectrogram plot. Default is "Spectrogram".

    Returns:
        matplotlib.figure.Figure: The figure object containing the plot.
    """
    fig = plt.figure(figsize=(12, 4))
    img = librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar(img, format='%+2.0f dB')
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    print("Spectrogram plot generated")
    return fig

def save_spectrogram_image(fig, output_image_path):
    """
    Saves the spectrogram plot to an image file.

    Args:
        fig (matplotlib.figure.Figure): The figure object to save.
        output_image_path (str): Path to save the spectrogram image.

    Returns:
        str: The path to the saved spectrogram image.
    """
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    fig.savefig(output_image_path, dpi=100, bbox_inches='tight')
    plt.close(fig)  # Close the figure to free memory
    print(f"Spectrogram image saved to {output_image_path}")
    return output_image_path

def generate_spectrogram_visualization(audio_file, output_image_path, title="Spectrogram"):
    """
    Generates a spectrogram visualization for the given audio file and saves it as an image.
    This is a convenience function that combines extract, plot, and save operations.

    Args:
        audio_file (str): Path to the audio file.
        output_image_path (str): Path to save the spectrogram image.
        title (str): Title for the spectrogram plot. Default is "Spectrogram".

    Returns:
        str: The path to the saved spectrogram image.
    """
    # Extract spectrogram
    S_db, sr = extract_spectrogram(audio_file)
    
    # Plot spectrogram
    fig = plot_spectrogram(S_db, sr, title=title)
    
    # Save spectrogram image
    return save_spectrogram_image(fig, output_image_path)

if __name__ == "__main__":
    # Example usage
    audio_file = "../data/music.wav"
    waveform_path = "../output/waveform.png"
    spectrogram_path = "../output/spectrogram.png"

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(waveform_path), exist_ok=True)

    generate_waveform_visualization(audio_file, waveform_path)
    generate_spectrogram_visualization(audio_file, spectrogram_path)