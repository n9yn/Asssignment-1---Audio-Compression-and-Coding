import os

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

if __name__ == "__main__":
    # Example usage
    original_audio_file = "../data/music.wav"  # Path to the original audio file
    compressed_audio_file = "../output/encoded/music_128kbps.mp3"  # Path to the compressed audio file
    result_file = "../output/reports/compression_ratio.txt"  # Path to store the result

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(result_file), exist_ok=True)

    # Compute and store the compression ratio
    compute_compression_ratio(original_audio_file, compressed_audio_file, result_file)