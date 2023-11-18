import vlc
import time

class Player:
    def __init__(self) -> None:
        self.file_name = None

    def playForward(self) -> None:
        try:
            print("Playing file {file_name}".format(file_name=self.file_name))
            player = vlc.MediaPlayer(self.file_name)
            player.play()
            time.sleep(10)
            player.stop()
        except Exception as e:
            print(f"An error occurred: {e}")

    def playBackward(self) -> None:
        pass
