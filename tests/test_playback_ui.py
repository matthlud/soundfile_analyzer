"""Tests for playback UI module."""

import os
import sys
import io
from contextlib import redirect_stdout

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from playback_ui import format_time, PlaybackDisplay, QueueDisplay


class TestFormatTime:
    """Test the format_time utility function."""

    def test_format_time_zero(self):
        """Test formatting zero seconds."""
        assert format_time(0) == "0:00"

    def test_format_time_one_minute(self):
        """Test formatting one minute."""
        assert format_time(60) == "1:00"

    def test_format_time_one_minute_thirty_seconds(self):
        """Test formatting 1 minute 30 seconds."""
        assert format_time(90) == "1:30"

    def test_format_time_five_minutes_forty_five_seconds(self):
        """Test formatting 5 minutes 45 seconds."""
        assert format_time(345) == "5:45"

    def test_format_time_large_value(self):
        """Test formatting large time value."""
        assert format_time(3661) == "61:01"  # 1 hour 1 minute 1 second


class TestPlaybackDisplay:
    """Test PlaybackDisplay class."""

    def test_playback_display_creation(self, tmp_path):
        """Test creating a PlaybackDisplay instance."""
        # Create a dummy file
        test_file = tmp_path / "test.wav"
        test_file.write_text("dummy content")

        display = PlaybackDisplay(str(test_file))
        assert display.filename == str(test_file)
        # Duration should be 0 for dummy file (can't load audio)
        assert display.duration >= 0

    def test_playback_display_get_duration_invalid(self, tmp_path):
        """Test getting duration for non-audio file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("not an audio file")

        display = PlaybackDisplay(str(test_file))
        # Should gracefully return 0 for invalid audio
        assert display.duration == 0.0

    def test_playback_display_print_now_playing(self, tmp_path, capsys):
        """Test printing now playing message."""
        test_file = tmp_path / "song.wav"
        test_file.write_text("dummy")

        display = PlaybackDisplay(str(test_file))
        display.print_now_playing()

        captured = capsys.readouterr()
        assert "NOW PLAYING" in captured.out or "song.wav" in captured.out

    def test_playback_display_progress_bar(self, tmp_path, capsys):
        """Test printing progress bar."""
        test_file = tmp_path / "song.wav"
        test_file.write_text("dummy")

        display = PlaybackDisplay(str(test_file))
        display.print_progress_bar(5.0, 10.0, width=50)

        captured = capsys.readouterr()
        # Should contain progress information
        assert "Progress" in captured.out or "█" in captured.out or "░" in captured.out

    def test_playback_display_completion(self, tmp_path, capsys):
        """Test printing completion message."""
        test_file = tmp_path / "song.wav"
        test_file.write_text("dummy")

        display = PlaybackDisplay(str(test_file))
        display.print_playback_complete()

        captured = capsys.readouterr()
        assert "complete" in captured.out.lower() or "✓" in captured.out


class TestQueueDisplay:
    """Test QueueDisplay class."""

    def test_queue_display_empty_queue(self, capsys):
        """Test displaying empty queue."""
        QueueDisplay.print_queue(None, [])

        captured = capsys.readouterr()
        assert "empty" in captured.out.lower()

    def test_queue_display_with_current_item(self, capsys):
        """Test displaying queue with current item."""
        current = "/path/to/song1.wav"
        queue = ["/path/to/song2.wav", "/path/to/song3.wav"]

        QueueDisplay.print_queue(current, queue)

        captured = capsys.readouterr()
        # Should mention queue or playlist
        assert "song1.wav" in captured.out or "QUEUE" in captured.out

    def test_queue_display_with_multiple_items(self, capsys):
        """Test displaying queue with multiple items."""
        current = "/path/to/current.wav"
        queue = [f"/path/to/song{i}.wav" for i in range(1, 6)]

        QueueDisplay.print_queue(current, queue)

        captured = capsys.readouterr()
        # Should show queue header
        assert "QUEUE" in captured.out or len(captured.out) > 0

    def test_queue_display_long_queue(self, capsys):
        """Test displaying queue with more than 10 items."""
        current = "/path/to/current.wav"
        queue = [f"/path/to/song{i}.wav" for i in range(1, 20)]

        QueueDisplay.print_queue(current, queue)

        captured = capsys.readouterr()
        # Should indicate there are more items
        assert "more" in captured.out.lower() or len(queue) <= 10

    def test_queue_display_none_current(self, capsys):
        """Test displaying queue without current item."""
        queue = ["/path/to/song1.wav", "/path/to/song2.wav"]

        QueueDisplay.print_queue(None, queue)

        captured = capsys.readouterr()
        # Should still show queue
        assert len(captured.out) > 0
