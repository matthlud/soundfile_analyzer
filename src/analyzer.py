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

    def apply_bandpass(self, lowcut: float, highcut: float, order: int = 4, inplace: bool = False, out_path: str | None = None):
        """Apply a bandpass Butterworth filter between lowcut and highcut (Hz)."""
        base = Filter(self.samples, self.sr)
        filtered = base._butter_filter((lowcut, highcut), btype='band', order=order)
        if inplace:
            self.samples = filtered
        if out_path:
            dirn = os.path.dirname(out_path)
            if dirn:
                os.makedirs(dirn, exist_ok=True)
            sf.write(out_path, filtered, self.sr)
        return filtered

    def apply_bandstop(self, lowcut: float, highcut: float, order: int = 4, inplace: bool = False, out_path: str | None = None):
        """Apply a band-stop (bandstop) Butterworth filter between lowcut and highcut (Hz)."""
        base = Filter(self.samples, self.sr)
        filtered = base._butter_filter((lowcut, highcut), btype='bandstop', order=order)
        if inplace:
            self.samples = filtered
        if out_path:
            dirn = os.path.dirname(out_path)
            if dirn:
                os.makedirs(dirn, exist_ok=True)
            sf.write(out_path, filtered, self.sr)
        return filtered

    def save_samples(self, out_path: str, samples: np.ndarray | None = None) -> None:
        """Save samples (or self.samples) to out_path using soundfile."""
        samples = self.samples if samples is None else samples
        dirn = os.path.dirname(out_path)
        if dirn:
            os.makedirs(dirn, exist_ok=True)
        sf.write(out_path, samples, self.sr)

    def get_duration(self) -> float:
        """Return duration of current samples in seconds."""
        return float(self.samples.size) / float(self.sr)

    def visualize_spectrogram(self, start_sample: int | None = None, length: int = 1000, out_path: str | None = "./artifacts/spectrogram.png", figsize: tuple = (16, 10), dpi: int = 100) -> str:
        """Create and save a spectrogram visualization of the audio.

        Allows specifying start_sample and length (number of samples). Returns the path
        to the saved image.
        """
        sample_array: np.array = self.samples
        if sample_array.size == 0:
            raise ValueError("No samples loaded")

        if start_sample is None:
            start = int(self.random_number)
        else:
            start = int(start_sample)
        if start < 0:
            start = 0
        if start > max(0, sample_array.size - 1):
            start = max(0, sample_array.size - 1)
        end = int(min(sample_array.size, start + max(1, int(length))))
        seg = sample_array[start:end]
        if seg.size == 0:
            seg = sample_array
            start = 0
            end = sample_array.size

        plt.figure(figsize=figsize, dpi=dpi)
        plt.specgram(seg, Fs=self.sr)
        plt.title(f"Sample {start} to {end} of {self.filename}")
        if out_path:
            dirn = os.path.dirname(out_path)
            if dirn:
                os.makedirs(dirn, exist_ok=True)
            plt.savefig(out_path)
        else:
            plt.savefig("./artifacts/spectrogram.png")
        plt.close()
        return out_path or "./artifacts/spectrogram.png"

    def visualize_waveform(self, start_sample: int | None = None, length: int = 1000, out_path: str | None = "./artifacts/waveform.png", figsize: tuple = (16, 10), dpi: int = 100) -> str:
        """Create and save a waveform visualization of the audio.

        Allows specifying start_sample and length (number of samples). Returns the path
        to the saved image.
        """
        sample_array: np.array = self.samples
        if sample_array.size == 0:
            raise ValueError("No samples loaded")

        if start_sample is None:
            start = int(self.random_number)
        else:
            start = int(start_sample)
        if start < 0:
            start = 0
        if start > max(0, sample_array.size - 1):
            start = max(0, sample_array.size - 1)
        end = int(min(sample_array.size, start + max(1, int(length))))
        seg = sample_array[start:end]
        if seg.size == 0:
            seg = sample_array
            start = 0
            end = sample_array.size

        plt.figure(figsize=figsize, dpi=dpi)
        plt.plot(seg)
        plt.title(f"Sample {start} to {end} of {self.filename}")
        if out_path:
            dirn = os.path.dirname(out_path)
            if dirn:
                os.makedirs(dirn, exist_ok=True)
            plt.savefig(out_path)
        else:
            plt.savefig("./artifacts/waveform.png")
        plt.close()
        return out_path or "./artifacts/waveform.png"

    def visualize_frequency(self, start_sample: int | None = None, length: int = 1000, out_path: str | None = "./artifacts/frequency.png", figsize: tuple = (16, 10), dpi: int = 100) -> str:
        """Create a frequency domain visualization of the audio.

        Allows specifying start_sample and length (number of samples). Returns the path
        to the saved image.
        """
        sample_array: np.array = self.samples
        if sample_array.size == 0:
            raise ValueError("No samples loaded")

        if start_sample is None:
            start = int(self.random_number)
        else:
            start = int(start_sample)
        if start < 0:
            start = 0
        if start > max(0, sample_array.size - 1):
            start = max(0, sample_array.size - 1)
        end = int(min(sample_array.size, start + max(1, int(length))))
        seg = sample_array[start:end]
        if seg.size == 0:
            seg = sample_array
            start = 0
            end = sample_array.size

        plt.figure(figsize=figsize, dpi=dpi)
        plt.magnitude_spectrum(seg, Fs=self.sr)
        plt.title(f"Sample {start} to {end} of {self.filename}")
        if out_path:
            dirn = os.path.dirname(out_path)
            if dirn:
                os.makedirs(dirn, exist_ok=True)
            plt.savefig(out_path)
        else:
            plt.savefig("./artifacts/frequency.png")
        plt.close()
        return out_path or "./artifacts/frequency.png"

    def __get_random_number(self) -> int:
        """Generate a random integer within the range of the audio sample size.

        Returns:
            A random integer between 0 and the size of the audio sample.
        """
        return random.randint(0, self.samples.size)
