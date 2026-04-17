import os
import numpy as np
import librosa

def compute_compression_ratio(original_file, compressed_file, output_file=None):
    """
    Compute compression ratio between original and compressed files.

    Args:
        original_file (str): Path to original file
        compressed_file (str): Path to compressed file
        output_file (str, optional): Path to save results

    Returns:
        float: Compression ratio (original_size / compressed_size)
    """
    if not os.path.exists(original_file):
        raise FileNotFoundError(f"Original file not found: {original_file}")
    if not os.path.exists(compressed_file):
        raise FileNotFoundError(f"Compressed file not found: {compressed_file}")

    original_size = os.path.getsize(original_file)
    compressed_size = os.path.getsize(compressed_file)

    if compressed_size == 0:
        raise ValueError("Compressed file is empty")

    ratio = original_size / compressed_size

    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as f:
            f.write(f"Original: {original_size} bytes\n")
            f.write(f"Compressed: {compressed_size} bytes\n")
            f.write(f"Ratio: {ratio:.2f}:1\n")

    return ratio

def compute_snr(original_file, compressed_file):
    """
    Compute Signal-to-Noise Ratio between original and compressed audio.

    Args:
        original_file (str): Path to original audio
        compressed_file (str): Path to compressed audio

    Returns:
        float: SNR in dB
    """
    if not os.path.exists(original_file):
        raise FileNotFoundError(f"Original file not found: {original_file}")
    if not os.path.exists(compressed_file):
        raise FileNotFoundError(f"Compressed file not found: {compressed_file}")

    # Load audio files
    y_orig, sr_orig = librosa.load(original_file, sr=None)
    y_comp, sr_comp = librosa.load(compressed_file, sr=None)

    # Resample if needed
    if sr_orig != sr_comp:
        y_comp = librosa.resample(y_comp, orig_sr=sr_comp, target_sr=sr_orig)

    # Trim to same length
    min_len = min(len(y_orig), len(y_comp))
    y_orig = y_orig[:min_len]
    y_comp = y_comp[:min_len]

    # Calculate SNR
    noise = y_orig - y_comp
    signal_power = np.mean(y_orig ** 2)
    noise_power = np.mean(noise ** 2)

    if signal_power == 0:
        raise ValueError("Original signal has zero power")
    if noise_power == 0:
        return float('inf')  # Perfect reconstruction

    return 10 * np.log10(signal_power / noise_power)
