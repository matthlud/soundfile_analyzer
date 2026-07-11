import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from queue import PlaybackQueue


def test_queue_persistence(tmp_path):
    storage = tmp_path / "queue.json"
    q = PlaybackQueue(str(storage))
    q.clear()
    assert q.list() == []
    q.add("a.wav")
    q.add("b.wav")
    assert q.list() == ["a.wav", "b.wav"]
    n = q.next()
    assert n == "a.wav"
    assert q.list() == ["b.wav"]
    q.clear()
    assert q.list() == []
