from FileHandler import FileHandler
from Player import Player

sound_file = FileHandler(r"D:\Projekte\Coding\soundfile_analyzer", "You_Can_Do_It.mp3")
sound_file.printFiles()

player = Player(sound_file.path_filename)
player.playForward()
