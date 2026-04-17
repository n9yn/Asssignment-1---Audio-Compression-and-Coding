import os
from pydub import AudioSegment

# Set the path to the ffmpeg executable
AudioSegment.converter = "C:/path/to/ffmpeg/bin/ffmpeg.exe"

def encode_audio(input_file, output_dir, bitrates):
    """
    Encodes an audio file into multiple bitrates and saves the output files.

    Args:
        input_file (str): Path to the input audio file.
        output_dir (str): Directory to save the encoded audio files.
        bitrates (list): List of bitrates to encode the audio file to (e.g., [64, 128, 256]).

    Returns:
        list[str]: Paths to the encoded audio files.
    """
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    output_files = []

    # Encode the audio file to each specified bitrate
    for bitrate in bitrates:
        output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_{bitrate}kbps.mp3")
        audio.export(output_file, format="mp3", bitrate=f"{bitrate}k")
        output_files.append(output_file)
        print(f"Encoded {input_file} to {bitrate} kbps and saved as {output_file}")

    return output_files

if __name__ == "__main__":
    # Updated example usage to test with a speech file
    input_audio_file = "../data/original/speech.wav"  # Path to the input speech audio file
    output_directory = "../output/encoded"  # Directory to save encoded files
    target_bitrates = [64, 128, 256]  # Bitrates to encode to

    encode_audio(input_audio_file, output_directory, target_bitrates)