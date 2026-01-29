"""module docstring
"""
from file_handler import FileHandler
from hardware_info import HardwareInfo
from player import Player
from analyzer import Analyzer

sound_file = FileHandler(r"D:\Projekte\Coding\soundfile_analyzer\tests", "You_Can_Do_It.wav")
sound_file.print_files()

info = HardwareInfo()
info.display_info()

audio_info = Analyzer(sound_file.path_filename)
audio_info.print_meta_info()
# audio_info.visualize_waveform()
# audio_info.visualize_spectrogram()

player = Player(sound_file.path_filename)
player.play_forward()
