import os
import sys
import numpy as np

sys.path.insert(0, os.path.abspath("src"))

from filter import Lowpass, Highpass, Notch


def gen_signal(sr=44100, dur=1.0):
    t = np.linspace(0, dur, int(sr * dur), endpoint=False)
    s = np.sin(2 * np.pi * 500 * t) + 0.5 * np.sin(2 * np.pi * 8000 * t)
    return s, sr


def band_energy(samples, sr, fmin, fmax):
    X = np.fft.rfft(samples)
    freqs = np.fft.rfftfreq(samples.size, 1 / sr)
    idx = np.where((freqs >= fmin) & (freqs <= fmax))[0]
    return np.sum(np.abs(X[idx]) ** 2)


def test_lowpass_attenuates_high_freq():
    s, sr = gen_signal()
    lp = Lowpass(s, sr, 2000, order=6)
    out = lp.apply()
    high_before = band_energy(s, sr, 4000, 10000)
    high_after = band_energy(out, sr, 4000, 10000)
    assert high_after < high_before * 0.4


def test_highpass_attenuates_low_freq():
    s, sr = gen_signal()
    hp = Highpass(s, sr, 1000, order=6)
    out = hp.apply()
    low_before = band_energy(s, sr, 0, 1000)
    low_after = band_energy(out, sr, 0, 1000)
    assert low_after < low_before * 0.6


def test_notch_reduces_center_frequency():
    s, sr = gen_signal()
    t = np.linspace(0, 1, int(sr * 1.0), endpoint=False)
    s2 = np.sin(2 * np.pi * 2000 * t) * 1.0 + s * 0.1
    notch = Notch(s2, sr, 2000, Q=30.0)
    out = notch.apply()
    center_before = band_energy(s2, sr, 1900, 2100)
    center_after = band_energy(out, sr, 1900, 2100)
    assert center_after < center_before * 0.35
