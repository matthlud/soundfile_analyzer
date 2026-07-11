import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import numpy as np
from filters import LowpassFilter, NotchFilter


def band_energy(sig, sr, lowf, highf):
    fft = np.fft.rfft(sig)
    freqs = np.fft.rfftfreq(sig.size, 1 / sr)
    mask = (freqs >= lowf) & (freqs <= highf)
    return np.abs(fft[mask]).sum()


def test_lowpass_reduces_high_band():
    sr = 44100
    t = np.linspace(0, 1, sr, endpoint=False)
    low = np.sin(2 * np.pi * 100 * t)
    high = 0.5 * np.sin(2 * np.pi * 5000 * t)
    sig = low + high
    lp = LowpassFilter(cutoff_hz=1000, sr=sr)
    out = lp.apply(sig)
    before = band_energy(sig, sr, 2000, 8000)
    after = band_energy(out, sr, 2000, 8000)
    assert out.shape == sig.shape
    assert after < before * 0.6


def test_notch_reduces_center_frequency():
    sr = 44100
    t = np.linspace(0, 1, sr, endpoint=False)
    target_freq = 440
    sig = np.sin(2 * np.pi * target_freq * t) + 0.1 * np.random.randn(sr)
    notch = NotchFilter(freq_hz=target_freq, sr=sr, q=30)
    out = notch.apply(sig)
    before = band_energy(sig, sr, 400, 480)
    after = band_energy(out, sr, 400, 480)
    assert after < before * 0.7

