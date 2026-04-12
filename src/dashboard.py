import os
import numpy as np
from src.encoder import encode_audio
from src.decoder import decode_audio
from src.metrics import compute_compression_ratio

def compute_compression_ratio(original_file, compressed_file, output_file):
    """
    Computes the compression ratio between the original and compressed audio files
    and stores the result in a specified file.

    Args:
        original_file (str): Path to the original audio file.
        compressed_file (str): Path to the compressed audio file.
        output_file (str): Path to store the compression ratio result.

    Returns:
        None
    """
    # Get the sizes of the files
    original_size = os.path.getsize(original_file)
    compressed_size = os.path.getsize(compressed_file)

    # Compute the compression ratio
    compression_ratio = original_size / compressed_size

    # Store the result
    with open(output_file, "w") as f:
        f.write(f"Original Size: {original_size} bytes\n")
        f.write(f"Compressed Size: {compressed_size} bytes\n")
        f.write(f"Compression Ratio: {compression_ratio:.2f}\n")

    print(f"Compression ratio computed and stored in {output_file}")

def compute_signal_to_noise_ratio(signal, noise):
    """
    Computes the Signal-to-Noise Ratio (SNR) in decibels (dB).

    Args:
        signal (numpy.ndarray): The original signal.
        noise (numpy.ndarray): The noise signal.

    Returns:
        float: The SNR value in decibels.
    """
    # Compute signal power
    signal_power = np.mean(np.square(signal))

    # Compute noise power
    noise_power = np.mean(np.square(noise))

    # Calculate SNR
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
        print("Error: Signal and noise must have the same length.")
        return False

    if np.any(noise == 0):
        print("Error: Noise contains zero values, which may lead to division by zero.")
        return False

    return True

def test_encoding_workflow():
    """
    Tests the encoding and decoding workflow for speech and music files.

    Returns:
        None
    """
    # File paths
    speech_file = "../data/speech.wav"
    music_file = "../data/music.wav"
    output_dir = "../output/encoded"
    decoded_dir = "../output/decoded"
    report_dir = "../output/reports"

    # Ensure output directories exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(decoded_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)

    # Bitrates to test
    bitrates = [64, 128, 256]

    # Test speech file
    for bitrate in bitrates:
        encoded_file = os.path.join(output_dir, f"speech_{bitrate}kbps.mp3")
        decoded_file = os.path.join(decoded_dir, f"speech_{bitrate}kbps_decoded.wav")
        report_file = os.path.join(report_dir, f"speech_{bitrate}kbps_report.txt")

        # Encode
        encode_audio(speech_file, output_dir, [bitrate])

        # Decode
        decode_audio(encoded_file, decoded_file)

        # Compute compression ratio
        compute_compression_ratio(speech_file, encoded_file, report_file)

    # Test music file
    for bitrate in bitrates:
        encoded_file = os.path.join(output_dir, f"music_{bitrate}kbps.mp3")
        decoded_file = os.path.join(decoded_dir, f"music_{bitrate}kbps_decoded.wav")
        report_file = os.path.join(report_dir, f"music_{bitrate}kbps_report.txt")

        # Encode
        encode_audio(music_file, output_dir, [bitrate])

        # Decode
        decode_audio(encoded_file, decoded_file)

        # Compute compression ratio
        compute_compression_ratio(music_file, encoded_file, report_file)

if __name__ == "__main__":
    test_encoding_workflow()

    # Example usage
    original_signal = np.random.normal(0, 1, 1000)  # Simulated original signal
    noise_signal = np.random.normal(0, 0.1, 1000)  # Simulated noise

    # Validate inputs
    if validate_snr(original_signal, noise_signal):
        # Compute SNR
        snr_value = compute_signal_to_noise_ratio(original_signal, noise_signal)
        print(f"Computed SNR: {snr_value:.2f} dB")