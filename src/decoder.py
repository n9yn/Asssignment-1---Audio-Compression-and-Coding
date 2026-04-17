import os
import simpleaudio as sa
from pydub import AudioSegment

def decode_audio(input_file, output_file):
    """
    Decodes an audio file and saves it in WAV format.

    Args:
        input_file (str): Path to the encoded audio file.
        output_file (str): Path to save the decoded WAV file.

    Returns:
        None
    """
    # Load the encoded audio file
    audio = AudioSegment.from_file(input_file)

    # Export the audio file to WAV format
    audio.export(output_file, format="wav")
    print(f"Decoded {input_file} and saved as {output_file}")

def play_audio(file_path):
    """
    Plays an audio file.

    Args:
        file_path (str): Path to the audio file to play.

    Returns:
        None
    """
    # Load the audio file
    wave_obj = sa.WaveObject.from_wave_file(file_path)

    # Play the audio file
    play_obj = wave_obj.play()
    play_obj.wait_done()
    print(f"Playing {file_path}")

def verify_audio_quality(original_file, decoded_file):
    """
    Verifies the quality of the decoded audio by comparing it to the original.
    Computes SNR and checks duration match.

    Args:
        original_file (str): Path to the original audio file.
        decoded_file (str): Path to the decoded audio file.

    Returns:
        dict: Dictionary containing quality metrics.
    """
    # Load both audio files
    original_audio = AudioSegment.from_file(original_file)
    decoded_audio = AudioSegment.from_file(decoded_file)

    # Check duration match
    duration_match = len(original_audio) == len(decoded_audio)
    
    # Compute SNR using librosa
    import librosa
    import numpy as np
    
    y_orig, sr_orig = librosa.load(original_file, sr=None)
    y_dec, sr_dec = librosa.load(decoded_file, sr=None)
    
    # Ensure same sample rate
    if sr_orig != sr_dec:
        y_dec = librosa.resample(y_dec, orig_sr=sr_dec, target_sr=sr_orig)
    
    # Trim to the same length
    min_len = min(len(y_orig), len(y_dec))
    y_orig = y_orig[:min_len]
    y_dec = y_dec[:min_len]
    
    # Compute noise
    noise = y_orig - y_dec
    
    # Compute power
    signal_power = np.mean(y_orig ** 2)
    noise_power = np.mean(noise ** 2)
    
    # Compute SNR
    if noise_power == 0:
        snr = float('inf')
    else:
        snr = 10 * np.log10(signal_power / noise_power)
    
    print(f"Audio quality verification:")
    print(f"  Duration match: {duration_match}")
    print(f"  SNR: {snr:.2f} dB")
    
    return {
        "duration_match": duration_match,
        "snr": snr
    }

if __name__ == "__main__":
    # Example usage
    encoded_audio_file = "../output/encoded/music_128kbps.mp3"  # Path to the encoded audio file
    decoded_audio_file = "../output/decoded/music_decoded.wav"  # Path to save the decoded WAV file
    original_audio_file = "../data/music.wav"  # Path to the original audio file

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(decoded_audio_file), exist_ok=True)

    # Decode the audio
    decode_audio(encoded_audio_file, decoded_audio_file)

    # Play the decoded audio
    play_audio(decoded_audio_file)

    # Verify the audio quality
    quality_metrics = verify_audio_quality(original_audio_file, decoded_audio_file)
    print(f"Quality check: {quality_metrics}")