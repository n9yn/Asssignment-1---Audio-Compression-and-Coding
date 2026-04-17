import os
import tempfile
import numpy as np
from scipy import signal

def ensure_directories(*paths):
    """Create directories if they do not exist."""
    for path in paths:
        if path and not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

def save_uploaded_tempfile(uploaded_file, suffix=""):
    """Save a Streamlit uploaded file to a temporary local file."""
    suffix = suffix or os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        return tmp_file.name

def format_bytes(byte_count):
    """Format bytes into a human-readable string."""
    units = ["bytes", "KB", "MB", "GB"]
    byte_count = float(byte_count)

    for unit in units:
        if byte_count < 1024:
            if unit == "bytes":
                return f"{int(byte_count)} {unit}"
            return f"{byte_count:.2f} {unit}"
        if unit == "GB":
            return f"{byte_count:.2f} {unit}"
        byte_count /= 1024

    return f"{byte_count:.2f} GB"

def get_project_root():
    """Return the absolute path to the project root directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

def get_adaptive_sample_count(audio_length, sr, max_display_samples=5000):
    """
    Calculate adaptive number of samples to display based on audio length.
    
    Args:
        audio_length (int): Total number of audio samples
        sr (int): Sample rate
        max_display_samples (int): Maximum samples to show in visualization
        
    Returns:
        int: Number of samples to display
        int: Decimation factor (for efficient display)
    """
    duration = audio_length / sr
    
    # For short files (< 30 seconds), display everything
    if duration <= 30:
        return audio_length, 1
    
    # For medium files, show full waveform with decimation
    if duration <= 300:  # 5 minutes
        decimate_factor = max(1, audio_length // max_display_samples)
        return min(audio_length, max_display_samples * 2), decimate_factor
    
    # For long files, show first portion with decimation
    decimate_factor = max(1, audio_length // max_display_samples)
    return max_display_samples, decimate_factor

def downsample_audio_for_display(audio, decimate_factor):
    """
    Downsample audio for visualization.
    
    Args:
        audio (numpy.ndarray): Audio signal
        decimate_factor (int): Decimation factor
        
    Returns:
        numpy.ndarray: Downsampled audio
    """
    if decimate_factor <= 1:
        return audio
    return signal.decimate(audio, decimate_factor, zero_phase=True, ftype='iir', n=4)

def get_adaptive_spectrogram_params(audio_length, sr):
    """
    Calculate adaptive parameters for spectrogram computation.
    
    Args:
        audio_length (int): Total number of audio samples
        sr (int): Sample rate
        
    Returns:
        dict: Parameters including n_fft, noverlap, downsample_factor
    """
    duration = audio_length / sr
    
    # Default parameters for short audio
    default_nfft = 2048
    
    # Adjust based on duration
    if duration <= 30:  # Short files
        return {
            'n_fft': 2048,
            'noverlap': 1024,
            'downsample_factor': 1,
            'nperseg': 2048
        }
    elif duration <= 300:  # Medium files (up to 5 minutes)
        return {
            'n_fft': 4096,
            'noverlap': 2048,
            'downsample_factor': 1,
            'nperseg': 4096
        }
    else:  # Large files (> 5 minutes)
        # Downsample to keep computation reasonable
        downsample_factor = max(1, int(duration / 300))  # Target ~5 minute visualization
        return {
            'n_fft': 4096,
            'noverlap': 2048,
            'downsample_factor': downsample_factor,
            'nperseg': 4096
        }

def prepare_audio_for_spectrogram(audio, sr):
    """
    Prepare audio for efficient spectrogram computation.
    
    Args:
        audio (numpy.ndarray): Audio signal
        sr (int): Sample rate
        
    Returns:
        tuple: (prepared_audio, params, effective_sr)
    """
    params = get_adaptive_spectrogram_params(len(audio), sr)
    downsample_factor = params['downsample_factor']
    
    if downsample_factor > 1:
        prepared = signal.decimate(audio, downsample_factor, zero_phase=True, ftype='iir', n=4)
        effective_sr = sr // downsample_factor
    else:
        prepared = audio
        effective_sr = sr
    
    return prepared, params, effective_sr
