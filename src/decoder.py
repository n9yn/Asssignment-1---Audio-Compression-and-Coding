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

    Args:
        original_file (str): Path to the original audio file.
        decoded_file (str): Path to the decoded audio file.

    Returns:
        None
    """
    # Load both audio files
    original_audio = AudioSegment.from_file(original_file)
    decoded_audio = AudioSegment.from_file(decoded_file)

    # Compare the duration of the two audio files
    if len(original_audio) == len(decoded_audio):
        print("Audio quality verification passed: Durations match.")
    else:
        print("Audio quality verification failed: Durations do not match.")

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
    verify_audio_quality(original_audio_file, decoded_audio_file)