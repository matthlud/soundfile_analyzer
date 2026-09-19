import os
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fileinfos import FileInfos


def test_fileinfos_on_existing_test_file(tmp_path):
    filename = tmp_path / "fixture.wav"
    samples = (np.zeros(4410, dtype=np.int16)).tobytes()

    with wave.open(str(filename), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)
        wav_file.writeframes(samples)

    fi = FileInfos(str(tmp_path), filename.name)
    assert fi.exists()
    assert fi.size() == filename.stat().st_size
    meta = fi.metadata()
    assert isinstance(meta, dict)
