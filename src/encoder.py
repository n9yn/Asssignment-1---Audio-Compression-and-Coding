import os
import numpy as np
import soundfile as sf
import subprocess
import shutil

def encode_audio(input_file, output_dir, bitrates):
    """
    Encodes an audio file into multiple bitrates and saves the output files.

    Args:
        input_file (str): Path to the input audio file.
        output_dir (str): Directory to save the encoded audio files.
        bitrates (list): List of bitrates to encode the audio file to (e.g., [64, 128, 256]).

    Returns:
        list[str]: Paths to the encoded audio files.
    
    Raises:
        FileNotFoundError: If input file does not exist.
        ValueError: If bitrates list is empty or invalid.
    """
    # Input validation
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    if not bitrates or not isinstance(bitrates, (list, tuple)):
        raise ValueError("bitrates must be a non-empty list or tuple of integers")
    
    if not all(isinstance(b, (int, float)) and b > 0 for b in bitrates):
        raise ValueError("All bitrates must be positive numbers")
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    output_files = []
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # Check if FFmpeg is available
    ffmpeg_available = shutil.which('ffmpeg') is not None
    
    if not ffmpeg_available:
        print("Warning: FFmpeg not found. Using WAV format instead of MP3.")
        print("For actual compression, install FFmpeg: https://ffmpeg.org/download.html")
    
    try:
        # Encode the audio file to each specified bitrate
        for bitrate in bitrates:
            if ffmpeg_available:
                # Use FFmpeg for MP3 compression
                output_file = os.path.join(output_dir, f"{base_name}_{int(bitrate)}kbps.mp3")
                cmd = [
                    'ffmpeg',
                    '-i', input_file,
                    '-b:a', f'{int(bitrate)}k',
                    '-q:a', '9',  # Variable bitrate quality
                    '-y',  # Overwrite output file
                    output_file
                ]
                
                # Run FFmpeg command
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    raise RuntimeError(f"FFmpeg error: {result.stderr}")
                
                output_files.append(output_file)
                print(f"Encoded {input_file} to {int(bitrate)} kbps and saved as {output_file}")
            else:
                # Fallback: Load audio and save as WAV (no actual bitrate compression)
                data, samplerate = sf.read(input_file)
                output_file = os.path.join(output_dir, f"{base_name}_{int(bitrate)}kbps.wav")
                sf.write(output_file, data, samplerate, format='WAV', subtype='PCM_16')
                output_files.append(output_file)
                print(f"Saved {input_file} as WAV (no compression applied): {output_file}")
    
    except Exception as e:
        print(f"Error encoding audio: {str(e)}")
        raise
    
    return output_files

if __name__ == "__main__":
    # Updated example usage to test with a speech file
    input_audio_file = "../data/original/speech.wav"  # Path to the input speech audio file
    output_directory = "../output/encoded"  # Directory to save encoded files
    target_bitrates = [64, 128, 256]  # Bitrates to encode to

    encode_audio(input_audio_file, output_directory, target_bitrates)
