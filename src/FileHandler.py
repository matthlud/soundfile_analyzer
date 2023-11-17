import os
import pathlib
import sys
import logging


class FileHandler:
    def __init__(self, filename, path) -> None:
        self.filename: str = filename
        self.path: pathlib.Path = path

    def readFile(self) -> None:
        pass

    def saveFile(self) -> None:
        pass

    def deleteFile(self) -> None:
        pass

    def moveFile(self) -> None:
        pass

    def copyFile(self) -> None:
        pass
