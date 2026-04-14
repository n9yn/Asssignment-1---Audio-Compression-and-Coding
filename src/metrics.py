import os
import numpy as np

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

def compare_snr(signal1, noise1, signal2, noise2):
    """
    Compares the Signal-to-Noise Ratio (SNR) of two audio signals.

    Args:
        signal1 (numpy.ndarray): The first signal.
        noise1 (numpy.ndarray): The noise corresponding to the first signal.
        signal2 (numpy.ndarray): The second signal.
        noise2 (numpy.ndarray): The noise corresponding to the second signal.

    Returns:
        tuple: SNR values for both signals.
    """
    def compute_snr(signal, noise):
        signal_power = np.mean(np.square(signal))
        noise_power = np.mean(np.square(noise))
        return 10 * np.log10(signal_power / noise_power)

    snr1 = compute_snr(signal1, noise1)
    snr2 = compute_snr(signal2, noise2)

    return snr1, snr2

if __name__ == "__main__":
    # Example usage
    original_audio_file = "../data/music.wav"  # Path to the original audio file
    compressed_audio_file = "../output/encoded/music_128kbps.mp3"  # Path to the compressed audio file
    result_file = "../output/reports/compression_ratio.txt"  # Path to store the result

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(result_file), exist_ok=True)

    # Compute and store the compression ratio
    compute_compression_ratio(original_audio_file, compressed_audio_file, result_file)

    # Example usage for SNR comparison
    signal1 = np.random.normal(0, 1, 1000)  # Simulated signal 1
    noise1 = np.random.normal(0, 0.1, 1000)  # Simulated noise 1
    signal2 = np.random.normal(0, 1, 1000)  # Simulated signal 2
    noise2 = np.random.normal(0, 0.2, 1000)  # Simulated noise 2

    snr1, snr2 = compare_snr(signal1, noise1, signal2, noise2)
    print(f"SNR of Signal 1: {snr1:.2f} dB")
    print(f"SNR of Signal 2: {snr2:.2f} dB")