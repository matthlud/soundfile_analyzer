"""module docstring
"""
from file_handler import FileHandler
from player import Player
from analyzer import Analyzer

sound_file = FileHandler(r"D:\Projekte\Coding\soundfile_analyzer\tests", "You_Can_Do_It.mp3")
sound_file.printFiles()

audio_info = Analyzer(sound_file.path_filename)
audio_info.printMetaInfo()

# player = Player(sound_file.path_filename)
# player.playForward()
