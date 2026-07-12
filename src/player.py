"""module docstring
"""
import time
import threading

# Import vlc lazily — not all environments have python-vlc installed
try:
    import vlc
except Exception:
    vlc = None

# Import librosa for duration calculation
try:
    import librosa
except ImportError:
    librosa = None

# Import playback UI
try:
    from .playback_ui import PlaybackDisplay
except ImportError:
    try:
        from playback_ui import PlaybackDisplay
    except ImportError:
        PlaybackDisplay = None


class Player:
    """class docstring
    """
    def __init__(self, filename) -> None:
        self.filename = filename

    def _get_duration(self) -> float:
        """Get audio duration in seconds."""
        if librosa is None:
            return 0.0
        try:
            y, sr = librosa.load(self.filename, sr=None)
            return len(y) / sr
        except Exception:
            return 0.0

    def play_forward(self, full_length: bool = True, show_ui: bool = True) -> None:
        """Play audio file.
        
        Args:
            full_length: If True, play entire file; if False, play for 3 seconds (demo mode)
            show_ui: If True, display fancy playback UI; if False, simple text output
        """
        if vlc is None:
            print("python-vlc is not installed; cannot play audio.")
            return
        try:
            # Calculate duration
            duration = self._get_duration() if full_length else 3.0

            # Show UI
            if show_ui and PlaybackDisplay:
                display = PlaybackDisplay(self.filename)
                display.print_now_playing()
            else:
                print(f"Playing file: {self.filename}")

            # Play audio
            player = vlc.MediaPlayer(self.filename)
            player.play()

            # Track playback with progress display
            if show_ui and PlaybackDisplay and duration > 0:
                display = PlaybackDisplay(self.filename)
                start_time = time.time()
                while time.time() - start_time < duration:
                    elapsed = time.time() - start_time
                    display.print_progress_bar(elapsed, duration)
                    time.sleep(0.1)
                display.print_playback_complete()
            else:
                time.sleep(duration)

            player.stop()
        except Exception as e:
            print(f"An error occurred: {e}")

    def play_backward(self) -> None:
        if vlc is None:
            print("python-vlc is not installed; cannot play audio.")
            return
        # Not implemented yet
        print("Backward playback not implemented")
