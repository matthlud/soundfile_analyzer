"""Filter module

Provides a base Filter class and concrete filter implementations:
- Lowpass
- Highpass
- Notch (band-stop)

These classes operate on a numpy sample array and a sample rate (Hz).
"""
from typing import Tuple, Union

import numpy as np
from scipy.signal import butter, filtfilt, iirnotch


class Filter:
    """Base filter class.

    Args:
        samples: 1-D array-like audio samples
        sr: sample rate in Hz
    """

    def __init__(self, samples: Union[np.ndarray, list, tuple], sr: int) -> None:
        self.samples = np.asarray(samples, dtype=float)
        self.sr = int(sr)

    def apply(self) -> np.ndarray:
        """Return filtered samples. Base implementation returns input unchanged."""
        return self.samples

    def _butter_filter(self, cutoff: Union[float, Tuple[float, float]], btype: str = "low", order: int = 4) -> np.ndarray:
        """Apply a Butterworth filter and return the filtered signal.

        cutoff may be a single frequency (for low/high) or a (low, high) tuple for band filters.
        """
        nyq = 0.5 * self.sr
        if isinstance(cutoff, tuple):
            Wn = [c / nyq for c in cutoff]
        else:
            Wn = float(cutoff) / nyq
        b, a = butter(order, Wn, btype=btype)
        return filtfilt(b, a, self.samples)


class Lowpass(Filter):
    """Simple lowpass filter using a Butterworth design."""

    def __init__(self, samples, sr: int, cutoff: float, order: int = 4) -> None:
        super().__init__(samples, sr)
        self.cutoff = float(cutoff)
        self.order = int(order)

    def apply(self) -> np.ndarray:
        return self._butter_filter(self.cutoff, btype="low", order=self.order)


class Highpass(Filter):
    """Simple highpass filter using a Butterworth design."""

    def __init__(self, samples, sr: int, cutoff: float, order: int = 4) -> None:
        super().__init__(samples, sr)
        self.cutoff = float(cutoff)
        self.order = int(order)

    def apply(self) -> np.ndarray:
        return self._butter_filter(self.cutoff, btype="high", order=self.order)


class Notch(Filter):
    """Notch (band-stop) filter centered on ``center_freq``.

    Uses scipy.signal.iirnotch when available (supports ``fs`` kwarg in newer scipy).
    """

    def __init__(self, samples, sr: int, center_freq: float, Q: float = 30.0) -> None:
        super().__init__(samples, sr)
        self.center_freq = float(center_freq)
        self.Q = float(Q)

    def apply(self) -> np.ndarray:
        # Prefer the 'fs' argument (w0 in Hz) if available; fall back to normalized freq.
        try:
            b, a = iirnotch(self.center_freq, self.Q, fs=self.sr)
        except TypeError:
            # older scipy: expects w0 normalized to Nyquist (0..1)
            w0 = self.center_freq / (self.sr / 2)
            b, a = iirnotch(w0, self.Q)
        return filtfilt(b, a, self.samples)


__all__ = ["Filter", "Lowpass", "Highpass", "Notch"]
