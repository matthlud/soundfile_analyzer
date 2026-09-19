import os
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from visualization import Visualization


def test_visualizations_create_artifacts(tmp_path, monkeypatch):
    filename = tmp_path / "fixture.wav"

    sample_rate = 44100
    duration = 1
    samples = (
        0.5
        * np.sin(2 * np.pi * 440 * np.arange(sample_rate * duration) / sample_rate)
        * np.iinfo(np.int16).max
    ).astype(np.int16)

    with wave.open(str(filename), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(samples.tobytes())

    monkeypatch.chdir(tmp_path)
    viz = Visualization(str(filename))
    viz.waveform()
    viz.spectrogram()
    viz.frequency()

    assert (tmp_path / "artifacts" / "waveform.png").exists()
    assert (tmp_path / "artifacts" / "spectrogram.png").exists()
    assert (tmp_path / "artifacts" / "frequency.png").exists()
