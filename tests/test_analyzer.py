import os
import sys
import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.abspath("src"))

from analyzer import Analyzer


def test_apply_bandpass_and_save(tmp_path):
    sr = 22050
    t = np.linspace(0, 1, int(sr * 1.0), endpoint=False)
    s = np.sin(2 * np.pi * 400 * t) + np.sin(2 * np.pi * 3000 * t)
    fpath = tmp_path / "in.wav"
    sf.write(str(fpath), s, sr)
    a = Analyzer(str(fpath))
    out = a.apply_bandpass(300, 800, inplace=True, out_path=str(tmp_path / "out.wav"))
    assert (tmp_path / "out.wav").exists()
    assert abs(a.get_duration() - 1.0) < 0.02
