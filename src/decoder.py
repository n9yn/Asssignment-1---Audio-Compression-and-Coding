import os
import soundfile as sf
import librosa
import numpy as np

def decode_audio(input_file, output_file):
    """
    Decode audio file to WAV format.

    Args:
        input_file (str): Path to encoded audio file
        output_file (str): Path for decoded WAV output

    Returns:
        str: Path to decoded file
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Load and save as WAV
    data, samplerate = sf.read(input_file)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    sf.write(output_file, data, samplerate, format='WAV', subtype='PCM_16')

    print(f"Decoded: {output_file}")
    return output_file

def verify_audio_quality(original_file, decoded_file):
    """
    Compare original and decoded audio quality.

    Args:
        original_file (str): Path to original audio
        decoded_file (str): Path to decoded audio

    Returns:
        dict: Quality metrics (snr, duration_match)
    """
    if not os.path.exists(original_file):
        raise FileNotFoundError(f"Original file not found: {original_file}")
    if not os.path.exists(decoded_file):
        raise FileNotFoundError(f"Decoded file not found: {decoded_file}")

    # Load audio files
    y_orig, sr_orig = librosa.load(original_file, sr=None)
    y_dec, sr_dec = librosa.load(decoded_file, sr=None)

    # Resample if needed
    if sr_orig != sr_dec:
        y_dec = librosa.resample(y_dec, orig_sr=sr_dec, target_sr=sr_orig)

    # Trim to same length
    min_len = min(len(y_orig), len(y_dec))
    y_orig = y_orig[:min_len]
    y_dec = y_dec[:min_len]

    # Calculate SNR
    noise = y_orig - y_dec
    signal_power = np.mean(y_orig ** 2)
    noise_power = np.mean(noise ** 2)

    if signal_power == 0 or noise_power == 0:
        snr = float('inf') if noise_power == 0 else float('-inf')
    else:
        snr = 10 * np.log10(signal_power / noise_power)

    return {
        "snr": snr,
        "duration_match": len(y_orig) == len(y_dec)
    }
