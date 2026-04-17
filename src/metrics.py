import os
import numpy as np
import librosa

def compute_compression_ratio(original_file, compressed_file, output_file):
    """
    Computes the compression ratio between the original and compressed audio files
    and stores the result in a specified file.

    Args:
        original_file (str): Path to the original audio file.
        compressed_file (str): Path to the compressed audio file.
        output_file (str): Path to store the compression ratio result.

    Returns:
        float: The compression ratio.
    
    Raises:
        FileNotFoundError: If input files do not exist.
    """
    # Validate input files
    if not os.path.exists(original_file):
        raise FileNotFoundError(f"Original file not found: {original_file}")
    if not os.path.exists(compressed_file):
        raise FileNotFoundError(f"Compressed file not found: {compressed_file}")
    
    try:
        # Get the sizes of the files
        original_size = os.path.getsize(original_file)
        compressed_size = os.path.getsize(compressed_file)
        
        # Validate sizes
        if compressed_size == 0:
            raise ValueError("Compressed file is empty")
        
        # Compute the compression ratio
        compression_ratio = original_size / compressed_size
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Store the result
        with open(output_file, "w") as f:
            f.write(f"Original Size: {original_size} bytes\n")
            f.write(f"Compressed Size: {compressed_size} bytes\n")
            f.write(f"Compression Ratio: {compression_ratio:.2f}\n")
        
        print(f"Compression ratio computed and stored in {output_file}")
        return compression_ratio
    except Exception as e:
        print(f"Error computing compression ratio: {str(e)}")
        raise

def compute_snr(original_file, compressed_file):
    """
    Computes the Signal-to-Noise Ratio (SNR) between the original and compressed audio files.

    Args:
        original_file (str): Path to the original audio file.
        compressed_file (str): Path to the compressed audio file.

    Returns:
        float: The SNR value in dB.
    
    Raises:
        FileNotFoundError: If input files do not exist.
    """
    # Validate input files
    if not os.path.exists(original_file):
        raise FileNotFoundError(f"Original file not found: {original_file}")
    if not os.path.exists(compressed_file):
        raise FileNotFoundError(f"Compressed file not found: {compressed_file}")
    
    try:
        # Load the audio files
        y_orig, sr_orig = librosa.load(original_file, sr=None)
        y_comp, sr_comp = librosa.load(compressed_file, sr=None)
        
        # Ensure same sample rate
        if sr_orig != sr_comp:
            y_comp = librosa.resample(y_comp, orig_sr=sr_comp, target_sr=sr_orig)
        
        # Pad shorter signal instead of truncating to preserve information
        max_len = max(len(y_orig), len(y_comp))
        y_orig_padded = np.zeros(max_len)
        y_comp_padded = np.zeros(max_len)
        y_orig_padded[:len(y_orig)] = y_orig
        y_comp_padded[:len(y_comp)] = y_comp
        
        # Compute noise as difference
        noise = y_orig_padded - y_comp_padded
        
        # Compute power
        signal_power = np.mean(y_orig_padded ** 2)
        noise_power = np.mean(noise ** 2)
        
        # Avoid division by zero with proper checks
        if signal_power == 0:
            raise ValueError("Original signal has zero power")
        if noise_power == 0:
            return float('inf')  # Perfect reconstruction
        
        # Compute SNR
        snr = 10 * np.log10(signal_power / noise_power)
        return snr
    except Exception as e:
        print(f"Error computing SNR: {str(e)}")
        raise

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
    
    Raises:
        ValueError: If signal lengths don't match noise lengths or invalid inputs.
    """
    # Input validation
    if len(signal1) != len(noise1):
        raise ValueError("signal1 and noise1 must have the same length")
    if len(signal2) != len(noise2):
        raise ValueError("signal2 and noise2 must have the same length")
    
    def compute_snr_internal(signal, noise):
        """Compute SNR for a single signal-noise pair with proper zero-checking."""
        if len(signal) == 0 or len(noise) == 0:
            raise ValueError("Signal and noise arrays cannot be empty")
        
        signal_power = np.mean(np.square(signal))
        noise_power = np.mean(np.square(noise))
        
        # Proper zero-checking
        if signal_power == 0:
            raise ValueError("Signal power is zero")
        if noise_power == 0:
            return float('inf')  # Perfect reconstruction
        
        return 10 * np.log10(signal_power / noise_power)
    
    try:
        snr1 = compute_snr_internal(signal1, noise1)
        snr2 = compute_snr_internal(signal2, noise2)
        return snr1, snr2
    except Exception as e:
        print(f"Error comparing SNR: {str(e)}")
        raise

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
