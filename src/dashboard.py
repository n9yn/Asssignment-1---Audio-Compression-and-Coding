import os
import numpy as np
from src.encoder import encode_audio
from src.decoder import decode_audio
from src.metrics import compute_compression_ratio, compare_snr
from src.visualization import compare_waveforms, compare_spectrograms

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

def compare_speech_vs_music():
    """
    Compares speech and music audio files based on SNR, waveform, and spectrogram.

    Returns:
        None
    """
    # File paths
    speech_file = "../data/speech.wav"
    music_file = "../data/music.wav"

    # Simulated signals and noise for demonstration
    speech_signal = np.random.normal(0, 1, 1000)
    speech_noise = np.random.normal(0, 0.1, 1000)
    music_signal = np.random.normal(0, 1, 1000)
    music_noise = np.random.normal(0, 0.2, 1000)

    # Compare SNR
    snr_speech, snr_music = compare_snr(speech_signal, speech_noise, music_signal, music_noise)
    print(f"SNR for Speech: {snr_speech:.2f} dB")
    print(f"SNR for Music: {snr_music:.2f} dB")

    # Compare waveforms
    compare_waveforms(speech_signal, music_signal, ["Speech", "Music"])

    # Compare spectrograms
    sample_rate = 44100
    compare_spectrograms(speech_signal, music_signal, ["Speech", "Music"], sample_rate)

if __name__ == "__main__":
    test_encoding_workflow()
    compare_speech_vs_music()