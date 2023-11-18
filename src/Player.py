import vlc
import time

class Player:
    def __init__(self, filename) -> None:
        self.filename = filename

    def playForward(self) -> None:
        try:
            print(f"Playing file {self.filename}")
            player = vlc.MediaPlayer(self.filename)
            player.play()
            time.sleep(3)
            player.stop()
        except Exception as e:
            print(f"An error occurred: {e}")

    def playBackward(self) -> None:
        pass
