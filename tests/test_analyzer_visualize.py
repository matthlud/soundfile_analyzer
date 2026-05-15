import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import soundfile as sf

sys.path.insert(0, os.path.abspath("src"))

from analyzer import Analyzer


def test_visualizations_create_images(tmp_path):
    sr = 22050
    t = np.linspace(0, 1, int(sr * 1.0), endpoint=False)
    s = np.sin(2 * np.pi * 440 * t) + 0.5 * np.sin(2 * np.pi * 5000 * t)
    fpath = tmp_path / "in.wav"
    sf.write(str(fpath), s, sr)
    a = Analyzer(str(fpath))
    out1 = str(tmp_path / "spec.png")
    out2 = str(tmp_path / "wave.png")
    out3 = str(tmp_path / "freq.png")
    p1 = a.visualize_spectrogram(start_sample=0, length=1024, out_path=out1)
    p2 = a.visualize_waveform(start_sample=0, length=1024, out_path=out2)
    p3 = a.visualize_frequency(start_sample=0, length=2048, out_path=out3)
    assert os.path.exists(p1) and os.path.getsize(p1) > 0
    assert os.path.exists(p2) and os.path.getsize(p2) > 0
    assert os.path.exists(p3) and os.path.getsize(p3) > 0
