"""module docstring
"""
import random
from mutagen.mp3 import MP3
from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
# import logging
# import bokeh


class Analyzer:
    """class docstring
    """
    def __init__(self, filename) -> None:
        self.filename = filename
        self.__sample_array = self.__convert_sound_to_array()

    def print_meta_info(self) -> None:
        """function docstring
        """
        file: MP3 = MP3(self.filename)
        print(f"Filename: {file.filename}")
        print(f"Length [s]: {file.info.length}")
        print(f"Bitrate: {file.info.bitrate}")
        print(f"Samplerate: {file.info.sample_rate}")
        print(f"Channels: {file.info.channels}")

    def visualize_spectrogram(self) -> None:
        """function docstring
        """
        sample_array: np.array = self.__sample_array
        plt.figure(figsize=(16, 10))
        random_number = random.randint(0, self.__sample_array.size) 
        plt.specgram(sample_array[random_number:(random_number+1000)])
        plt.title(f"Sample {random_number} to {random_number+1000} of {self.filename}")
        plt.show()

    def visualize_waveform(self) -> None:
        """function docstring
        """
        sample_array: np.array = self.__sample_array
        plt.figure(figsize=(16, 10))
        random_number = random.randint(0, self.__sample_array.size) 
        plt.plot(sample_array[random_number:(random_number+1000)])
        plt.title(f"Sample {random_number} to {random_number+1000} of {self.filename}")
        plt.show()

    def visualize_amplitude(self) -> None:
        """function docstring
        """
        pass

    def visualize_current_amplitude(self) -> None:
        """function docstring
        """
        pass

    def __convert_sound_to_array(self) -> np.array:
        """MP3 to numpy array
        """
        # input_format = os.path.splitext(self.filename)[-1]
        info_container: AudioSegment = AudioSegment.from_file(self.filename)
        sound_array: np.array = np.array(info_container.get_array_of_samples())
        return sound_array
