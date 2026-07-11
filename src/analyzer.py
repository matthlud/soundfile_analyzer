"""Analyzer utilities used by tests and the visualization wrapper.

This Analyzer provides a small, test-friendly API for reading audio via soundfile,
applying simple filters (bandpass/bandstop) and producing visualization images.
It intentionally avoids heavy application-level dependencies so unit tests run
quickly.
"""

from __future__ import annotations

import os
import random
from typing import Optional

import numpy as np
import soundfile as sf
from scipy.signal import butter, filtfilt, iirnotch
import matplotlib.pyplot as plt

try:
    from mutagen.mp3 import MP3
except Exception:  # pragma: no cover - metadata optional
    MP3 = None


def _safe_filtfilt(b, a, data):
    try:
        return filtfilt(b, a, data)
    except Exception:
        # fallback to causal filter when filtfilt fails (very short signals)
        from scipy.signal import lfilter

        return lfilter(b, a, data)


class Analyzer:
    """Small analyzer focused on tests' needs."""

    def __init__(self, filename: str) -> None:
        self.filename = filename
        try:
            data, sr = sf.read(self.filename, dtype="float32")
            samples = np.asarray(data, dtype=float)
            # convert multi-channel to mono
            if getattr(samples, "ndim", 1) > 1:
                samples = samples.mean(axis=1)
        except Exception:
            # fallback to librosa/audioread for problematic containers
            import librosa

            samples, sr = librosa.load(self.filename, sr=None)

        self.samples = samples
        self.sr = int(sr)
        self.random_number = self.__get_random_number()

    def print_meta_info(self) -> None:
        if MP3 is None:
            print("mutagen not available; cannot read MP3 metadata")
            return
        file = MP3(self.filename)
        print(f"Filename: {file.filename}")
        print(f"Length [s]: {getattr(file.info, 'length', None)}")
        print(f"Bitrate: {getattr(file.info, 'bitrate', None)}")
        print(f"Samplerate: {getattr(file.info, 'sample_rate', None)}")
        print(f"Channels: {getattr(file.info, 'channels', None)}")

    # --- simple filtering helpers ---
    def apply_bandpass(self, lowcut: float, highcut: float, order: int = 4, inplace: bool = False, out_path: Optional[str] = None):
        nyq = 0.5 * self.sr
        low = max(1e-6, min(lowcut / nyq, 0.9999))
        high = max(low + 1e-6, min(highcut / nyq, 0.9999))
        b, a = butter(order, [low, high], btype="band")
        filtered = _safe_filtfilt(b, a, self.samples)
        if inplace:
            self.samples = filtered
        if out_path:
            dirn = os.path.dirname(out_path)
            if dirn:
                os.makedirs(dirn, exist_ok=True)
            sf.write(out_path, filtered, self.sr)
        return filtered

    def apply_bandstop(self, lowcut: float, highcut: float, order: int = 4, inplace: bool = False, out_path: Optional[str] = None):
        nyq = 0.5 * self.sr
        low = max(1e-6, min(lowcut / nyq, 0.9999))
        high = max(low + 1e-6, min(highcut / nyq, 0.9999))
        b, a = butter(order, [low, high], btype="bandstop")
        filtered = _safe_filtfilt(b, a, self.samples)
        if inplace:
            self.samples = filtered
        if out_path:
            dirn = os.path.dirname(out_path)
            if dirn:
                os.makedirs(dirn, exist_ok=True)
            sf.write(out_path, filtered, self.sr)
        return filtered

    def save_samples(self, out_path: str, samples: Optional[np.ndarray] = None) -> None:
        samples = self.samples if samples is None else samples
        dirn = os.path.dirname(out_path)
        if dirn:
            os.makedirs(dirn, exist_ok=True)
        sf.write(out_path, samples, self.sr)

    def get_duration(self) -> float:
        return float(self.samples.size) / float(self.sr)

    # --- visualizations ---
    def visualize_spectrogram(self, start_sample: Optional[int] = None, length: int = 1000, out_path: Optional[str] = "./artifacts/spectrogram.png", figsize: tuple = (16, 10), dpi: int = 100) -> str:
        sample_array = self.samples
        if sample_array.size == 0:
            raise ValueError("No samples loaded")
        if start_sample is None:
            start = int(self.random_number)
        else:
            start = int(start_sample)
        start = max(0, start)
        start = min(start, max(0, sample_array.size - 1))
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
            os.makedirs("./artifacts", exist_ok=True)
            plt.savefig("./artifacts/spectrogram.png")
        plt.close()
        return out_path or "./artifacts/spectrogram.png"

    def visualize_waveform(self, start_sample: Optional[int] = None, length: int = 1000, out_path: Optional[str] = "./artifacts/waveform.png", figsize: tuple = (16, 10), dpi: int = 100) -> str:
        sample_array = self.samples
        if sample_array.size == 0:
            raise ValueError("No samples loaded")
        if start_sample is None:
            start = int(self.random_number)
        else:
            start = int(start_sample)
        start = max(0, start)
        start = min(start, max(0, sample_array.size - 1))
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
            os.makedirs("./artifacts", exist_ok=True)
            plt.savefig("./artifacts/waveform.png")
        plt.close()
        return out_path or "./artifacts/waveform.png"

    def visualize_frequency(self, start_sample: Optional[int] = None, length: int = 1000, out_path: Optional[str] = "./artifacts/frequency.png", figsize: tuple = (16, 10), dpi: int = 100) -> str:
        sample_array = self.samples
        if sample_array.size == 0:
            raise ValueError("No samples loaded")
        if start_sample is None:
            start = int(self.random_number)
        else:
            start = int(start_sample)
        start = max(0, start)
        start = min(start, max(0, sample_array.size - 1))
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
            os.makedirs("./artifacts", exist_ok=True)
            plt.savefig("./artifacts/frequency.png")
        plt.close()
        return out_path or "./artifacts/frequency.png"

    def __get_random_number(self) -> int:
        max_index = max(0, int(getattr(self, "samples", np.array([])).size) - 1)
        return random.randint(0, max_index)
