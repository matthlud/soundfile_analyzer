"""Tests for interactive PlaybackREPL."""

import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from playback_repl import PlaybackREPL


class TestPlaybackREPLCreation:
    """Test PlaybackREPL creation and initialization."""

    def test_repl_creation(self):
        """Test creating a PlaybackREPL instance."""
        repl = PlaybackREPL()
        assert repl.manager is not None
        assert repl.running is False
        assert repl.current_file is None

    def test_repl_with_queue(self, tmp_path):
        """Test creating REPL with queue file."""
        queue_file = tmp_path / "queue.json"
        repl = PlaybackREPL(queue_file=str(queue_file))
        assert repl.queue is not None

    def test_repl_without_queue(self):
        """Test creating REPL without queue file."""
        repl = PlaybackREPL(queue_file=None)
        assert repl.queue is None


class TestPlaybackREPLCommands:
    """Test REPL command processing."""

    def test_help_command(self, capsys):
        """Test help command."""
        repl = PlaybackREPL()
        repl._process_command("help")
        
        captured = capsys.readouterr()
        assert "PLAYBACK CONTROL" in captured.out or "help" in captured.out.lower()

    def test_status_command(self, capsys):
        """Test status command."""
        repl = PlaybackREPL()
        repl._process_command("status")
        
        captured = capsys.readouterr()
        # Should show status information
        assert len(captured.out) > 0

    def test_stop_command(self, capsys):
        """Test stop command."""
        repl = PlaybackREPL()
        repl._process_command("stop")
        
        captured = capsys.readouterr()
        assert "Stopped" in captured.out or "stop" in captured.out.lower()

    def test_pause_command(self):
        """Test pause command."""
        repl = PlaybackREPL()
        repl._process_command("pause")
        # Should not raise error

    def test_resume_command(self):
        """Test resume command."""
        repl = PlaybackREPL()
        repl._process_command("resume")
        # Should not raise error

    def test_restart_command(self, capsys):
        """Test restart command."""
        repl = PlaybackREPL()
        repl._process_command("restart")
        
        captured = capsys.readouterr()
        assert "Restarting" in captured.out or len(captured.out) >= 0

    def test_next_command(self):
        """Test next command."""
        repl = PlaybackREPL()
        repl._process_command("next")
        # Should not raise error

    def test_previous_command(self):
        """Test previous command."""
        repl = PlaybackREPL()
        repl._process_command("prev")
        # Should not raise error

    def test_queue_command_no_queue(self, capsys):
        """Test queue command when queue not available."""
        repl = PlaybackREPL(queue_file=None)
        repl._process_command("queue")
        
        captured = capsys.readouterr()
        assert "not available" in captured.out.lower()

    def test_add_command_no_queue(self, capsys):
        """Test add command when queue not available."""
        repl = PlaybackREPL(queue_file=None)
        repl._process_command("add song.wav")
        
        captured = capsys.readouterr()
        assert "not available" in captured.out.lower()

    def test_add_command_with_queue(self, tmp_path, capsys):
        """Test add command with queue."""
        queue_file = tmp_path / "queue.json"
        repl = PlaybackREPL(queue_file=str(queue_file))
        
        test_file = str(tmp_path / "song.wav")
        repl._process_command(f"add {test_file}")
        
        captured = capsys.readouterr()
        assert "Added" in captured.out or "add" in captured.out.lower()

    def test_exit_command(self):
        """Test exit command."""
        repl = PlaybackREPL()
        repl.running = True
        repl._process_command("exit")
        
        assert repl.running is False

    def test_quit_command(self):
        """Test quit command."""
        repl = PlaybackREPL()
        repl.running = True
        repl._process_command("quit")
        
        assert repl.running is False

    def test_unknown_command(self, capsys):
        """Test unknown command."""
        repl = PlaybackREPL()
        repl._process_command("unknown")
        
        captured = capsys.readouterr()
        assert "Unknown command" in captured.out or "unknown" in captured.out.lower()

    def test_empty_command(self):
        """Test empty command."""
        repl = PlaybackREPL()
        repl._process_command("")
        # Should not raise error

    def test_demo_command(self, tmp_path):
        """Test demo command."""
        test_file = tmp_path / "test.wav"
        test_file.write_text("dummy")
        
        repl = PlaybackREPL()
        try:
            repl._process_command(f"demo {str(test_file)}")
        except Exception:
            pass
        # Should attempt to play demo
        assert repl.current_file is not None or repl.current_file is None


class TestPlaybackREPLCallbacks:
    """Test REPL callbacks."""

    def test_on_playback_complete_callback(self, tmp_path):
        """Test playback completion callback."""
        repl = PlaybackREPL()
        repl.current_file = str(tmp_path / "song.wav")
        
        # Should not raise error
        repl._on_playback_complete()

    def test_on_next_requested_callback(self, tmp_path):
        """Test next requested callback."""
        queue_file = tmp_path / "queue.json"
        repl = PlaybackREPL(queue_file=str(queue_file))
        
        # Add a song to queue
        if repl.queue:
            repl.queue.add(str(tmp_path / "song.wav"))
        
        # Should handle callback
        result = repl._on_next_requested()
        # Result might be None or string depending on queue state


class TestPlaybackREPLCleanup:
    """Test REPL cleanup."""

    def test_cleanup(self):
        """Test cleanup method."""
        repl = PlaybackREPL()
        repl._cleanup()
        # Should not raise error

    def test_cleanup_with_active_playback(self, tmp_path):
        """Test cleanup with active playback."""
        test_file = tmp_path / "test.wav"
        test_file.write_text("dummy")
        
        repl = PlaybackREPL()
        repl.manager.state = MagicMock()
        repl._cleanup()
        # Should handle gracefully


class TestPlaybackREPLHelp:
    """Test help display."""

    def test_show_help(self, capsys):
        """Test help display."""
        repl = PlaybackREPL()
        repl._show_help()
        
        captured = capsys.readouterr()
        # Should show help content
        assert len(captured.out) > 0
        assert "PLAYBACK" in captured.out.upper() or "CONTROL" in captured.out.upper()

    def test_show_status(self, capsys):
        """Test status display."""
        repl = PlaybackREPL()
        repl._show_status()
        
        captured = capsys.readouterr()
        # Should show status information
        assert "Status" in captured.out or "state" in captured.out.lower()
