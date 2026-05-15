"""module docstring"""

import random
from mutagen.mp3 import MP3

import librosa
import numpy as np

# from scipy.io import wavfile
import soundfile as sf
import os
import matplotlib.pyplot as plt
from filter import Filter, Lowpass, Highpass, Notch


class Analyzer:
    """class docstring"""

    def __init__(self, filename) -> None:
        """Initialize the Analyzer with an audio file.

        Args:
            filename: Path to the audio file to analyze.
        """
        self.filename = filename
        self.samples, self.sr = librosa.load(self.filename, sr=None)
        self.random_number = self.__get_random_number()

    def print_meta_info(self) -> None:
        """Print metadata information about the audio file.

        Displays filename, length, bitrate, sample rate, and number of channels.
        """
        file: MP3 = MP3(self.filename)
        print(f"Filename: {file.filename}")
        print(f"Length [s]: {file.info.length}")
        print(f"Bitrate: {file.info.bitrate}")
        print(f"Samplerate: {file.info.sample_rate}")
        print(f"Channels: {file.info.channels}")

    # --- Filter application helpers ---
    def apply_filter(self, filter_obj, inplace: bool = False, out_path: str | None = None):
        """Apply a Filter object to the current samples.

        Args:
            filter_obj: instance of Filter (must implement apply())
            inplace: if True, replace self.samples with filtered result
            out_path: optional path to save filtered audio (WAV)

        Returns:
            Filtered numpy array of samples
        """
        filtered = filter_obj.apply()
        if inplace:
            self.samples = filtered
        if out_path:
            dirn = os.path.dirname(out_path)
            if dirn:
                os.makedirs(dirn, exist_ok=True)
            sf.write(out_path, filtered, self.sr)
        return filtered

    def apply_lowpass(self, cutoff: float, order: int = 4, inplace: bool = False, out_path: str | None = None):
        """Apply a Lowpass filter and return filtered samples."""
        filt = Lowpass(self.samples, self.sr, cutoff, order)
        return self.apply_filter(filt, inplace=inplace, out_path=out_path)

    def apply_highpass(self, cutoff: float, order: int = 4, inplace: bool = False, out_path: str | None = None):
        """Apply a Highpass filter and return filtered samples."""
        filt = Highpass(self.samples, self.sr, cutoff, order)
        return self.apply_filter(filt, inplace=inplace, out_path=out_path)

    def apply_notch(self, center_freq: float, Q: float = 30.0, inplace: bool = False, out_path: str | None = None):
        """Apply a Notch filter and return filtered samples."""
        filt = Notch(self.samples, self.sr, center_freq, Q)
        return self.apply_filter(filt, inplace=inplace, out_path=out_path)

    def visualize_spectrogram(self) -> None:
        """Create and save a spectrogram visualization of the audio.

        Generates a random 1000-sample window from the audio and saves the
        spectrogram as './artifacts/spectrogram.png'.
        """
        sample_array: np.array = self.samples
        plt.figure(figsize=(16, 10))
        plt.specgram(sample_array[self.random_number : (self.random_number + 1000)])
        plt.title(
            f"Sample {self.random_number} to {self.random_number+1000} of {self.filename}"
        )
        plt.savefig("./artifacts/spectrogram.png")
        plt.close()

    def visualize_waveform(self) -> None:
        """Create and save a waveform visualization of the audio.

        Generates a random 1000-sample window from the audio and saves the
        waveform plot as './artifacts/waveform.png'.
        """
        sample_array: np.array = self.samples
        plt.figure(figsize=(16, 10))
        plt.plot(sample_array[self.random_number : (self.random_number + 1000)])
        plt.title(
            f"Sample {self.random_number} to {self.random_number+1000} of {self.filename}"
        )
        plt.savefig("./artifacts/waveform.png")
        plt.close()

    def visualize_frequency(self) -> None:
        """Create a frequency domain visualization of the audio.

        Generates a random 1000-sample window from the audio and saves the
        frequency spectrum plot as './artifacts/frequency.png'.
        """
        sample_array: np.array = self.samples
        plt.figure(figsize=(16, 10))
        plt.magnitude_spectrum(
            sample_array[self.random_number : (self.random_number + 1000)], Fs=self.sr
        )
        plt.title(
            f"Sample {self.random_number} to {self.random_number+1000} of {self.filename}"
        )
        plt.savefig("./artifacts/frequency.png")
        plt.close()

    def __get_random_number(self) -> int:
        """Generate a random integer within the range of the audio sample size.

        Returns:
            A random integer between 0 and the size of the audio sample.
        """
        return random.randint(0, self.samples.size)
