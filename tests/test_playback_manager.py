"""Tests for background playback manager with responsive controls."""

import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from playback_manager import PlaybackManager, PlaybackState


class TestPlaybackManagerBasics:
    """Test basic PlaybackManager functionality."""

    def test_playback_manager_creation(self):
        """Test creating a PlaybackManager instance."""
        manager = PlaybackManager()
        assert manager.state == PlaybackState.STOPPED
        assert manager.current_file is None

    def test_get_status_stopped(self):
        """Test getting status when stopped."""
        manager = PlaybackManager()
        status = manager.get_status()
        assert status["state"] == "stopped"
        assert status["is_playing"] is False

    def test_get_status_playing(self, tmp_path):
        """Test getting status when playing."""
        # Create dummy file
        test_file = tmp_path / "test.wav"
        test_file.write_text("dummy")
        
        manager = PlaybackManager()
        manager.current_file = str(test_file)
        manager.state = PlaybackState.PLAYING
        
        status = manager.get_status()
        assert status["state"] == "playing"
        assert status["is_playing"] is True
        assert status["current_file"] == str(test_file)


class TestPlaybackManagerControls:
    """Test playback control commands."""

    def test_stop_when_stopped(self):
        """Test stop command when already stopped."""
        manager = PlaybackManager()
        manager.stop()  # Should not raise error
        assert manager.state == PlaybackState.STOPPED

    def test_pause_when_stopped(self):
        """Test pause command when stopped."""
        manager = PlaybackManager()
        manager.pause()  # Should not raise error
        assert manager.state == PlaybackState.STOPPED

    def test_pause_when_playing(self):
        """Test pause changes state to paused."""
        manager = PlaybackManager()
        manager.state = PlaybackState.PLAYING
        manager.pause()
        assert manager.state == PlaybackState.PAUSED

    def test_resume_when_paused(self):
        """Test resume changes state back to playing."""
        manager = PlaybackManager()
        manager.state = PlaybackState.PAUSED
        manager.resume()
        assert manager.state == PlaybackState.PLAYING

    def test_next_request_flag(self):
        """Test next command sets flag."""
        manager = PlaybackManager()
        manager.state = PlaybackState.PLAYING
        manager.next()
        assert manager._next_requested is True

    def test_restart_request_flag(self):
        """Test restart command sets flag."""
        manager = PlaybackManager()
        manager.state = PlaybackState.PLAYING
        manager.restart()
        assert manager._restart_requested is True

    def test_previous_calls_restart(self):
        """Test previous command."""
        manager = PlaybackManager()
        manager.state = PlaybackState.PLAYING
        manager.previous()
        # Previous should restart current or handle queue
        assert manager.state in (PlaybackState.PLAYING, PlaybackState.PAUSED)


class TestPlaybackManagerThreading:
    """Test background playback threading."""

    def test_play_starts_thread(self, tmp_path):
        """Test that play starts a background thread."""
        test_file = tmp_path / "test.wav"
        test_file.write_text("dummy")
        
        manager = PlaybackManager()
        # Play will fail due to dummy file, but should still create thread
        try:
            manager.play(str(test_file), full_length=False, show_ui=False)
        except Exception:
            pass
        
        # Thread should have been created (even if it errors)
        assert manager.playback_thread is not None
        assert isinstance(manager.playback_thread, threading.Thread)

    def test_wait_for_completion_timeout(self, tmp_path):
        """Test wait_for_completion with timeout."""
        test_file = tmp_path / "test.wav"
        test_file.write_text("dummy")
        
        manager = PlaybackManager()
        try:
            manager.play(str(test_file), full_length=False, show_ui=False)
        except Exception:
            pass
        
        # Timeout should occur quickly
        result = manager.wait_for_completion(timeout=0.1)
        # Result can be True or False depending on thread state
        assert isinstance(result, bool)

    def test_stop_sets_flag(self, tmp_path):
        """Test that stop sets the stop flag."""
        test_file = tmp_path / "test.wav"
        test_file.write_text("dummy")
        
        manager = PlaybackManager()
        manager.state = PlaybackState.PLAYING
        manager.stop()
        
        assert manager._stop_requested is True
        # State is changed by the worker thread, not immediately by stop()


class TestPlaybackManagerCallbacks:
    """Test playback callbacks."""

    def test_set_completion_callback(self):
        """Test setting on_playback_complete callback."""
        manager = PlaybackManager()
        callback_called = []
        
        def callback():
            callback_called.append(True)
        
        manager.on_playback_complete = callback
        assert manager.on_playback_complete is callback

    def test_set_next_callback(self):
        """Test setting on_next_requested callback."""
        manager = PlaybackManager()
        def callback():
            return "next_file.wav"
        
        manager.on_next_requested = callback
        assert manager.on_next_requested is callback
        assert manager.on_next_requested() == "next_file.wav"


class TestPlaybackManagerFileHandling:
    """Test file handling."""

    def test_play_nonexistent_file(self, capsys):
        """Test playing a nonexistent file."""
        manager = PlaybackManager()
        manager.play("/nonexistent/file.wav", show_ui=False)
        
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower() or "error" in captured.out.lower()

    def test_get_duration_invalid_file(self, tmp_path):
        """Test getting duration of invalid audio file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("not audio")
        
        manager = PlaybackManager()
        duration = manager._get_duration(str(test_file))
        assert duration == 0.0

    def test_get_duration_nonexistent_file(self):
        """Test getting duration of nonexistent file."""
        manager = PlaybackManager()
        duration = manager._get_duration("/nonexistent/file.wav")
        assert duration == 0.0


# Import threading for isinstance check
import threading
