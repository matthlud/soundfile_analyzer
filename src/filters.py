"""Filter classes for audio processing.

Provides a simple base Filter and concrete implementations: Lowpass, Highpass, Notch.
Uses scipy.signal internally.
"""
from __future__ import annotations

import numpy as np
from scipy.signal import butter, filtfilt, iirnotch, lfilter


class Filter:
    """Base filter class."""

    def __init__(self, sr: int, order: int = 4):
        self.sr = int(sr)
        self.order = int(order)

    def apply(self, samples: np.ndarray) -> np.ndarray:
        raise NotImplementedError


def _safe_filtfilt(b, a, data):
    try:
        return filtfilt(b, a, data)
    except Exception:
        # fallback to causal filter if zero-phase fails (very short signals)
        return lfilter(b, a, data)


class LowpassFilter(Filter):
    def __init__(self, cutoff_hz: float, sr: int, order: int = 4):
        super().__init__(sr, order)
        self.cutoff = float(cutoff_hz)

    def apply(self, samples: np.ndarray) -> np.ndarray:
        x = np.asarray(samples, dtype=float)
        nyq = 0.5 * self.sr
        normal_cutoff = max(min(self.cutoff / nyq, 0.9999), 1e-6)
        b, a = butter(self.order, normal_cutoff, btype="low", analog=False)
        return _safe_filtfilt(b, a, x)


class HighpassFilter(Filter):
    def __init__(self, cutoff_hz: float, sr: int, order: int = 4):
        super().__init__(sr, order)
        self.cutoff = float(cutoff_hz)

    def apply(self, samples: np.ndarray) -> np.ndarray:
        x = np.asarray(samples, dtype=float)
        nyq = 0.5 * self.sr
        normal_cutoff = max(min(self.cutoff / nyq, 0.9999), 1e-6)
        b, a = butter(self.order, normal_cutoff, btype="high", analog=False)
        return _safe_filtfilt(b, a, x)


class NotchFilter(Filter):
    def __init__(self, freq_hz: float, sr: int, q: float = 30):
        super().__init__(sr, order=2)
        self.freq = float(freq_hz)
        self.q = float(q)

    def apply(self, samples: np.ndarray) -> np.ndarray:
        x = np.asarray(samples, dtype=float)
        w0 = self.freq / (0.5 * self.sr)
        b, a = iirnotch(w0, self.q)
        return _safe_filtfilt(b, a, x)
