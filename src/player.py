"""module docstring
"""
import time
import vlc


class Player:
    """class docstring
    """
    def __init__(self, filename) -> None:
        self.filename = filename

    def play_forward(self) -> None:
        try:
            print(f"Playing file: {self.filename}")
            player = vlc.MediaPlayer(self.filename)
            player.play()
            time.sleep(3)
            player.stop()
        except Exception as e:
            print(f"An error occurred: {e}")

    def play_backward(self) -> None:
        pass
