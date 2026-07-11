"""Simple DJ effects: Fader (gain) and Reverb (basic delay-based reverb).

Effects implement a small, testable interface: apply(samples, sr=None) -> np.ndarray
"""
from __future__ import annotations

import numpy as np


class Effect:
    def apply(self, samples: np.ndarray, sr: int | None = None) -> np.ndarray:
        raise NotImplementedError


class Fader(Effect):
    """Simple gain multiplier. Useful as a volume/fader control."""

    def __init__(self, gain: float = 1.0) -> None:
        self.gain = float(gain)

    def apply(self, samples: np.ndarray, sr: int | None = None) -> np.ndarray:
        x = np.asarray(samples, dtype=float)
        return x * self.gain


class Reverb(Effect):
    """Basic delay-based reverb: sums delayed, decayed copies of the signal.

    Parameters:
    - delay_ms: delay between echoes in milliseconds
    - decay: multiplicative decay per repeat (0 < decay < 1)
    - repeats: number of delayed repeats to add
    """

    def __init__(self, delay_ms: float = 50.0, decay: float = 0.5, repeats: int = 5) -> None:
        self.delay_ms = float(delay_ms)
        self.decay = float(decay)
        self.repeats = int(repeats)

    def apply(self, samples: np.ndarray, sr: int | None = None) -> np.ndarray:
        if sr is None:
            raise ValueError("sample rate (sr) is required for Reverb")
        x = np.asarray(samples, dtype=float)
        out = x.copy()
        delay_samples = max(1, int(sr * (self.delay_ms / 1000.0)))
        for i in range(1, self.repeats + 1):
            att = self.decay ** i
            shift = delay_samples * i
            if shift >= x.size:
                break
            delayed = np.zeros_like(x)
            delayed[shift:] = x[:-shift]
            out = out + att * delayed
        return out
