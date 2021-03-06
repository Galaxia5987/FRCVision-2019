import json
import os
from typing import Callable


class File:
    """Handles reading and writing files."""

    def __init__(self, name: str, default, folder: str, extension):
        """
        Instantiate a file.
        :param name: The name of the target
        :param default: Default value
        :param folder: Folder to write files to
        """
        self.name = name
        self.default = default
        self.folder = folder
        self.extension = extension

    def get_filename(self) -> str:
        """
        Format filename.
        :return: The filename in a folder/name.extension format
        """
        return f'{self.folder}/{self.name}.{self.extension}'

    def save_file(self, data):
        """
        Save file according to format.
        :param data: The data to save to the file
        """
        with open(self.get_filename(), 'w') as f:
            json.dump(data, f)

    def load_file(self):
        """
        Load file from name.
        :return: The data from the file
        """
        if not os.path.isfile(self.get_filename()):
            if isinstance(self.default, Callable):
                self.save_file(self.default(self.name))
            else:
                self.save_file(self.default)
        with open(self.get_filename(), 'r') as f:
            return json.load(f)
