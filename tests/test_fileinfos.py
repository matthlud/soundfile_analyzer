import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from fileinfos import FileInfos


def test_fileinfos_on_existing_test_file():
    tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests"))
    filename = "You_Can_Do_It.wav"
    fi = FileInfos(tests_dir, filename)
    assert fi.exists()
    meta = fi.metadata()
    assert isinstance(meta, dict)
