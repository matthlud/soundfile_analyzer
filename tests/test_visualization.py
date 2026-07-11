import os, sys, shutil
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from visualization import Visualization


def test_visualizations_create_artifacts():
    tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests"))
    filename = os.path.join(tests_dir, "You_Can_Do_It.wav")
    viz = Visualization(filename)
    artifacts = os.path.abspath("artifacts")
    if os.path.exists(artifacts):
        shutil.rmtree(artifacts)
    viz.waveform()
    viz.spectrogram()
    viz.frequency()
    assert os.path.exists(os.path.join("artifacts", "waveform.png"))
    assert os.path.exists(os.path.join("artifacts", "spectrogram.png"))
    assert os.path.exists(os.path.join("artifacts", "frequency.png"))
    shutil.rmtree(artifacts)
