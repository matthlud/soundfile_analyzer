import os
import FileHandler
#import Player
import vlc
import time


sound_file = FileHandler.FileHandler(r"D:\Projekte\Coding\soundfile_analyzer", "You_Can_Do_It.mp3")

sound_file.printFiles()


play_audio_file(sound_file.path_filename)
