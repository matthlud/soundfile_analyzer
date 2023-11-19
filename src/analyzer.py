"""module docstring
"""
from mutagen.mp3 import MP3
# import logging
# import bokeh


class Analyzer:
    """class docstring
    """
    def __init__(self, filename) -> None:
        self.filename = filename

    def printMetaInfo(self) -> None:
        file = MP3(self.filename)
        print(f"Filename: {file.filename}")
        print(f"Length [s]: {file.info.length}")
        print(f"Bitrate: {file.info.bitrate}")
        print(f"Samplerate: {file.info.sample_rate}")
        print(f"Channels: {file.info.channels}")

    def visualizeSpectrogram(self) -> None:
        pass

    def visualizeAmplitude(self) -> None:
        pass

    def visualizeCurrentAmplitude(self) -> None:
        pass
