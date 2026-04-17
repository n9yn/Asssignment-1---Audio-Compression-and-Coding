import os
import subprocess
import shutil

def encode_audio(input_file, output_dir, bitrates):
    """
    Encode audio file to multiple MP3 bitrates using FFmpeg.

    Args:
        input_file (str): Path to input audio file
        output_dir (str): Output directory for encoded files
        bitrates (list): List of bitrates in kbps

    Returns:
        list: Paths to encoded files

    Raises:
        RuntimeError: If FFmpeg fails or is not available
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    if not shutil.which('ffmpeg'):
        raise RuntimeError("FFmpeg not found. Install from https://ffmpeg.org/download.html")

    os.makedirs(output_dir, exist_ok=True)

    output_files = []
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    for bitrate in bitrates:
        output_file = os.path.join(output_dir, f"{base_name}_{bitrate}kbps.mp3")

        cmd = [
            'ffmpeg', '-y', '-i', input_file,
            '-b:a', f'{bitrate}k', output_file
        ]

        result = subprocess.run(
            cmd, capture_output=True, text=True,
            stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
        )

        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg encoding failed for {bitrate} kbps")

        output_files.append(output_file)
        print(f"Encoded to {bitrate} kbps: {output_file}")

    return output_files
