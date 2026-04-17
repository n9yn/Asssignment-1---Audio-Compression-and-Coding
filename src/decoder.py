import os
import simpleaudio as sa
import soundfile as sf
from pydub import AudioSegment
import librosa
import numpy as np

def decode_audio(input_file, output_file):
    """
    Decodes an audio file and saves it in WAV format.

    Args:
        input_file (str): Path to the encoded audio file.
        output_file (str): Path to save the decoded WAV file.

    Returns:
        str: The decoded WAV file path.
    """
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Load the encoded audio file
        data, samplerate = sf.read(input_file)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Save the audio file to WAV format
        sf.write(output_file, data, samplerate, format='WAV', subtype='PCM_16')
        print(f"Decoded {input_file} and saved as {output_file}")
        return output_file
    except Exception as e:
        print(f"Error decoding audio: {str(e)}")
        raise

def play_audio(file_path):
    """
    Plays an audio file. Supports WAV, MP3, and other formats.

    Args:
        file_path (str): Path to the audio file to play.

    Returns:
        None
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        # Check file format and convert if necessary
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext != '.wav':
            # Convert non-WAV files to WAV for playback
            temp_wav = os.path.splitext(file_path)[0] + '_temp.wav'
            audio = AudioSegment.from_file(file_path)
            audio.export(temp_wav, format='wav')
            file_path = temp_wav
        
        # Load and play the audio file
        wave_obj = sa.WaveObject.from_wave_file(file_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
        print(f"Playing {file_path}")
        
        # Clean up temporary file if created
        if file_ext != '.wav':
            os.unlink(temp_wav)
    except Exception as e:
        print(f"Error playing audio: {str(e)}")
        raise

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
    try:
        if not os.path.exists(original_file):
            raise FileNotFoundError(f"Original file not found: {original_file}")
        if not os.path.exists(decoded_file):
            raise FileNotFoundError(f"Decoded file not found: {decoded_file}")
        
        # Load both audio files
        original_audio = AudioSegment.from_file(original_file)
        decoded_audio = AudioSegment.from_file(decoded_file)
        
        # Check duration match
        duration_match = len(original_audio) == len(decoded_audio)
        
        # Compute SNR using librosa
        y_orig, sr_orig = librosa.load(original_file, sr=None)
        y_dec, sr_dec = librosa.load(decoded_file, sr=None)
        
        # Ensure same sample rate
        if sr_orig != sr_dec:
            y_dec = librosa.resample(y_dec, orig_sr=sr_dec, target_sr=sr_orig)
        
        # Pad shorter signal instead of truncating
        max_len = max(len(y_orig), len(y_dec))
        y_orig_padded = np.zeros(max_len)
        y_dec_padded = np.zeros(max_len)
        y_orig_padded[:len(y_orig)] = y_orig
        y_dec_padded[:len(y_dec)] = y_dec
        
        # Compute noise
        noise = y_orig_padded - y_dec_padded
        
        # Compute power
        signal_power = np.mean(y_orig_padded ** 2)
        noise_power = np.mean(noise ** 2)
        
        # Compute SNR with proper zero-checking
        if signal_power == 0 or noise_power == 0:
            snr = float('-inf') if noise_power > 0 else float('inf')
        else:
            snr = 10 * np.log10(signal_power / noise_power)
        
        print(f"Audio quality verification:")
        print(f"  Duration match: {duration_match}")
        print(f"  SNR: {snr:.2f} dB")
        
        return {
            "duration_match": duration_match,
            "snr": snr
        }
    except Exception as e:
        print(f"Error verifying audio quality: {str(e)}")
        raise

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
