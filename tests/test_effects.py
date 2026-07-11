import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import numpy as np
import pytest
from effects import Fader, Reverb


def _rms(sig: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.asarray(sig) ** 2)))


def test_fader_changes_rms():
    sr = 44100
    t = np.linspace(0, 1, sr, endpoint=False)
    sig = np.sin(2 * np.pi * 440 * t)
    f = Fader(0.5)
    out = f.apply(sig, sr)
    assert out.shape == sig.shape
    assert _rms(out) == pytest.approx(0.5 * _rms(sig), rel=1e-2)


def test_reverb_impulse_tail():
    sr = 44100
    sig = np.zeros(sr)
    sig[0] = 1.0
    r = Reverb(delay_ms=10, decay=0.5, repeats=3)
    out = r.apply(sig, sr)
    delay_samples = int(sr * (10 / 1000.0))
    assert out.shape == sig.shape
    assert out[0] == pytest.approx(1.0, rel=1e-6)
    assert out[delay_samples] > 0.0
