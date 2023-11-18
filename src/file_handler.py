import os
import pathlib
# import logging


class FileHandler:
    """this is a class which does something
    """
    def __init__(self, dirs, files) -> None:
        self.files: str | [str] = files
        self.dirs: pathlib.Path | [pathlib.Path] = dirs
        self.path_filename: str | [str] = os.path.join(self.dirs, self.files)

    def printFiles(self) -> None:
        if self.files is [str]:
            for temp_file in self.files:
                print(temp_file)
        else:
            print(self.files)

    def readFiles(self) -> None:
        # TODO add exception handler
        # TODO only accept correct files
        os.path.join(self.dirs, self.files)

    def saveFiles(self) -> None:
        pass

    def deleteFiles(self) -> None:
        pass

    def moveFiles(self) -> None:
        pass

    def copyFiles(self) -> None:
        pass
