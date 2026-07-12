import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from playback_queue import PlaybackQueue


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


def test_queue_current(tmp_path):
    """Test getting current item without removing it."""
    storage = tmp_path / "queue.json"
    q = PlaybackQueue(str(storage))
    q.clear()
    
    assert q.current() is None
    
    q.add("song1.wav")
    assert q.current() == "song1.wav"
    
    q.add("song2.wav")
    assert q.current() == "song1.wav"
    
    q.next()
    assert q.current() == "song2.wav"


def test_queue_list_returns_copy(tmp_path):
    """Test that list() returns independent copy."""
    storage = tmp_path / "queue.json"
    q = PlaybackQueue(str(storage))
    q.clear()
    
    q.add("song1.wav")
    q.add("song2.wav")
    
    list1 = q.list()
    list1.append("song3.wav")
    
    # Original queue should not be affected
    assert q.list() == ["song1.wav", "song2.wav"]


def test_queue_multiple_adds(tmp_path):
    """Test adding multiple items to queue."""
    storage = tmp_path / "queue.json"
    q = PlaybackQueue(str(storage))
    q.clear()
    
    files = ["a.wav", "b.wav", "c.wav", "d.wav", "e.wav"]
    for f in files:
        q.add(f)
    
    assert q.list() == files
    assert len(q.list()) == 5


def test_queue_clear_empty_queue(tmp_path):
    """Test clearing an empty queue."""
    storage = tmp_path / "queue.json"
    q = PlaybackQueue(str(storage))
    q.clear()
    q.clear()  # Should not raise error
    assert q.list() == []


def test_queue_persistence_across_instances(tmp_path):
    """Test that queue persists across different instances."""
    storage = tmp_path / "queue.json"
    
    # First instance
    q1 = PlaybackQueue(str(storage))
    q1.clear()
    q1.add("song1.wav")
    q1.add("song2.wav")
    
    # Second instance should load the same queue
    q2 = PlaybackQueue(str(storage))
    assert q2.list() == ["song1.wav", "song2.wav"]
    
    # Modifications should persist
    q2.next()
    q3 = PlaybackQueue(str(storage))
    assert q3.list() == ["song2.wav"]

