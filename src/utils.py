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
    Returns a segment that preserves waveform detail while being efficient.
    
    Args:
        audio_length (int): Total number of audio samples
        sr (int): Sample rate
        max_display_samples (int): Maximum samples to show in visualization
        
    Returns:
        int: Start index for the segment
        int: Number of samples to display
        int: Decimation factor (for efficient display)
    """
    duration = audio_length / sr
    
    # For short files (< 60 seconds), display everything
    if duration <= 60:
        return 0, audio_length, 1
    
    # For medium files, show full waveform with decimation
    if duration <= 300:  # 5 minutes
        decimate_factor = max(1, audio_length // max_display_samples)
        return 0, audio_length, decimate_factor
    
    # For long files, show first 60 seconds with reasonable decimation
    # For 60s segments, use higher display resolution (20k-40k samples)
    segment_duration = 60  # seconds
    segment_samples = segment_duration * sr
    
    # Use higher max_display_samples for 60-second segments to preserve detail
    display_max = max(20000, max_display_samples * 4)
    decimate_factor = max(1, segment_samples // display_max)
    
    return 0, segment_samples, decimate_factor

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
    For very large files, limits the duration to keep computation fast.
    
    Args:
        audio_length (int): Total number of audio samples
        sr (int): Sample rate
        
    Returns:
        dict: Parameters including n_fft, noverlap, downsample_factor, max_samples
    """
    duration = audio_length / sr
    
    # Default parameters for short audio
    if duration <= 30:  # Short files
        return {
            'n_fft': 2048,
            'noverlap': 1024,
            'downsample_factor': 1,
            'nperseg': 2048,
            'max_samples': audio_length,  # Use entire audio
            'max_duration': duration
        }
    elif duration <= 300:  # Medium files (up to 5 minutes)
        return {
            'n_fft': 2048,
            'noverlap': 1024,
            'downsample_factor': 1,
            'nperseg': 2048,
            'max_samples': audio_length,
            'max_duration': duration
        }
    elif duration <= 1800:  # Large files (5-30 minutes)
        # Show first 60 seconds to keep computation reasonable
        max_duration = 60  # seconds
        max_samples = max_duration * sr
        return {
            'n_fft': 2048,
            'noverlap': 512,
            'downsample_factor': 2,  # 2x downsample for faster computation
            'nperseg': 2048,
            'max_samples': max_samples,
            'max_duration': max_duration
        }
    else:  # Very large files (> 30 minutes)
        # Show first 60 seconds with moderate downsampling
        max_duration = 60  # seconds
        max_samples = max_duration * sr
        return {
            'n_fft': 1024,
            'noverlap': 256,
            'downsample_factor': 2,  # 2x downsample for fast computation
            'nperseg': 1024,
            'max_samples': max_samples,
            'max_duration': max_duration
        }

def prepare_audio_for_spectrogram(audio, sr):
    """
    Prepare audio for efficient spectrogram computation.
    Limits duration for large files and applies downsampling.
    
    Args:
        audio (numpy.ndarray): Audio signal
        sr (int): Sample rate
        
    Returns:
        tuple: (prepared_audio, params, effective_sr)
    """
    params = get_adaptive_spectrogram_params(len(audio), sr)
    
    # First, limit to max_samples if needed
    max_samples = params['max_samples']
    if len(audio) > max_samples:
        audio_limited = audio[:max_samples]
    else:
        audio_limited = audio
    
    # Then downsample if needed
    downsample_factor = params['downsample_factor']
    
    if downsample_factor > 1:
        prepared = signal.decimate(audio_limited, downsample_factor, zero_phase=True, ftype='iir', n=4)
        effective_sr = sr // downsample_factor
    else:
        prepared = audio_limited
        effective_sr = sr
    
    return prepared, params, effective_sr
