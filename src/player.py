"""module docstring
"""
import time

# Import vlc lazily — not all environments have python-vlc installed
try:
    import vlc
except Exception:
    vlc = None


class Player:
    """class docstring
    """
    def __init__(self, filename) -> None:
        self.filename = filename

    def play_forward(self) -> None:
        if vlc is None:
            print("python-vlc is not installed; cannot play audio.")
            return
        try:
            print(f"Playing file: {self.filename}")
            player = vlc.MediaPlayer(self.filename)
            player.play()
            time.sleep(3)
            player.stop()
        except Exception as e:
            print(f"An error occurred: {e}")

    def play_backward(self) -> None:
        if vlc is None:
            print("python-vlc is not installed; cannot play audio.")
            return
        # Not implemented yet
        print("Backward playback not implemented")
