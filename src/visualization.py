import matplotlib.pyplot as plt
import numpy as np

def compare_waveforms(signal1, signal2, labels):
    """
    Compares the waveforms of two audio signals.

    Args:
        signal1 (numpy.ndarray): The first signal.
        signal2 (numpy.ndarray): The second signal.
        labels (list): Labels for the signals.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))

    # Plot signal 1
    plt.subplot(2, 1, 1)
    plt.plot(signal1, label=labels[0])
    plt.title(f"Waveform of {labels[0]}")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.legend()

    # Plot signal 2
    plt.subplot(2, 1, 2)
    plt.plot(signal2, label=labels[1])
    plt.title(f"Waveform of {labels[1]}")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.legend()

    plt.tight_layout()
    plt.show()

def compare_spectrograms(signal1, signal2, labels, sample_rate):
    """
    Compares the spectrograms of two audio signals.

    Args:
        signal1 (numpy.ndarray): The first signal.
        signal2 (numpy.ndarray): The second signal.
        labels (list): Labels for the signals.
        sample_rate (int): Sampling rate of the signals.

    Returns:
        None
    """
    plt.figure(figsize=(12, 8))

    # Plot spectrogram for signal 1
    plt.subplot(2, 1, 1)
    plt.specgram(signal1, Fs=sample_rate, cmap="viridis")
    plt.title(f"Spectrogram of {labels[0]}")
    plt.xlabel("Time")
    plt.ylabel("Frequency")

    # Plot spectrogram for signal 2
    plt.subplot(2, 1, 2)
    plt.specgram(signal2, Fs=sample_rate, cmap="viridis")
    plt.title(f"Spectrogram of {labels[1]}")
    plt.xlabel("Time")
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Example usage
    signal1 = np.sin(2 * np.pi * np.linspace(0, 1, 1000))  # Simulated sine wave
    signal2 = np.sin(2 * np.pi * np.linspace(0, 1, 1000) + np.pi / 4)  # Phase-shifted sine wave

    compare_waveforms(signal1, signal2, ["Signal 1", "Signal 2"])

    sample_rate = 44100
    t = np.linspace(0, 1, sample_rate)
    signal1 = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
    signal2 = np.sin(2 * np.pi * 880 * t)  # 880 Hz sine wave

    compare_spectrograms(signal1, signal2, ["Signal 1", "Signal 2"], sample_rate)
