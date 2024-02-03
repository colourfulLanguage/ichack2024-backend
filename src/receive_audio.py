"""
File for implementation for receiving websocket audio
"""
import numpy as np
from scipy.signal import find_peaks

from utils import note_frequencies, closest_value


def handle_audio(data):
    print("Received audio")
    print(data)
    note = find_most_prevalent_note(data)
    return note


def find_most_prevalent_note(audio_bytes):
    """
    Analyzes a series of audio bytes to find the most prevalent note.

    Args:
      audio_bytes: A byte array representing audio data.

    Returns:
      The frequency of the most prevalent note, or None if no clear peak is found.
    """

    # Convert bytes to audio samples (assuming 16-bit signed integer format)
    audio_samples = np.frombuffer(audio_bytes, dtype=np.int16)

    # Calculate the Fast Fourier Transform (FFT)
    fft = np.fft.fft(audio_samples)

    # Find the peak frequencies
    frequencies = np.fft.fftfreq(len(audio_samples), d=1.0 / 44100)  # Assuming 44100 Hz sampling rate
    peaks, _ = find_peaks(np.abs(fft), prominence=max(np.abs(fft)) * 0.1)  # Adjust prominence threshold as needed

    # If no clear peak is found, return None
    if len(peaks) == 0:
        return None

    # Find the most prevalent peak frequency
    most_prevalent_freq = frequencies[peaks[np.argmax(np.abs(fft[peaks]))]]
    note = closest_value(note_frequencies, most_prevalent_freq)

    return {"freq": most_prevalent_freq, "note": note}


if __name__ == '__main__':

    # Example usage
    audio_bytes = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"  # Replace with actual audio data
    most_prevalent_note = find_most_prevalent_note(audio_bytes)

    if most_prevalent_note is not None:
      print(f"Most prevalent note: {most_prevalent_note:.2f} Hz")
    else:
      print("No clear peak found in the audio data.")
