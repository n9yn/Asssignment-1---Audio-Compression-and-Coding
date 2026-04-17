import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import os

def generate_waveform_visualization(audio_file, output_image_path):
    """
    Generates a waveform visualization for the given audio file and saves it as an image.

    Args:
        audio_file (str): Path to the audio file.
        output_image_path (str): Path to save the waveform image.

    Returns:
        None
    """
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)

    # Create the plot
    plt.figure(figsize=(12, 4))
    librosa.display.waveshow(y, sr=sr)
    plt.title("Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    # Save the plot
    plt.savefig(output_image_path)
    plt.close()  # Close the figure to free memory
    print(f"Waveform visualization saved to {output_image_path}")

def generate_spectrogram_visualization(audio_file, output_image_path):
    """
    Generates a spectrogram visualization for the given audio file and saves it as an image.

    Args:
        audio_file (str): Path to the audio file.
        output_image_path (str): Path to save the spectrogram image.

    Returns:
        None
    """
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)

    # Compute the spectrogram
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

    # Create the plot
    plt.figure(figsize=(12, 4))
    librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar(format='%+2.0f dB')
    plt.title("Spectrogram")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")

    # Save the plot
    plt.savefig(output_image_path)
    plt.close()  # Close the figure to free memory
    print(f"Spectrogram visualization saved to {output_image_path}")

if __name__ == "__main__":
    # Example usage
    audio_file = "../data/music.wav"
    waveform_path = "../output/waveform.png"
    spectrogram_path = "../output/spectrogram.png"

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(waveform_path), exist_ok=True)

    generate_waveform_visualization(audio_file, waveform_path)
    generate_spectrogram_visualization(audio_file, spectrogram_path)