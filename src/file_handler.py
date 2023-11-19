"""module docstring
"""
import os
# import logging


class FileHandler:
    """this is a class which does something
    """
    def __init__(self, dirs, files) -> None:
        self.files: str | list[str] = files
        self.dirs: str | list[str] = dirs
        self.path_filename: str | list[str] = os.path.join(self.dirs, self.files)

    def print_files(self) -> None:
        if self.files is [str]:
            for temp_file in self.files:
                print(temp_file)
        else:
            print(self.files)

    def read_files(self) -> None:
        # TODO add exception handler
        # TODO only accept correct files
        os.path.join(self.dirs, self.files)

    def save_files(self) -> None:
        pass

    def delete_files(self) -> None:
        pass

    def move_files(self) -> None:
        pass

    def copy_files(self) -> None:
        pass
