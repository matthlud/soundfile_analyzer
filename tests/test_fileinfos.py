import os
import sys

sys.path.insert(0, os.path.abspath("src"))

from fileinfos import Fileinfos


def test_fileinfos_existing_file():
    here = os.path.dirname(__file__)
    sample = os.path.join(here, "You_Can_Do_It.wav")
    fi = Fileinfos(sample)
    assert fi.exists()
    assert fi.get_size_bytes() is not None and fi.get_size_bytes() > 0
    assert fi.get_duration() is not None and fi.get_duration() > 0
    assert fi.get_samplerate() is not None and fi.get_samplerate() > 0
    assert fi.get_channels() is not None and fi.get_channels() >= 1
    assert isinstance(fi.as_dict(), dict)


def test_fileinfos_nonexistent():
    fi = Fileinfos("/no/such/file/hopefully_does_not_exist.wav")
    assert not fi.exists()
    assert fi.get_size_bytes() is None
    assert fi.get_duration() is None
    assert fi.as_dict()["exists"] is False
