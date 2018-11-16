import json
import os


class File:
    """Handles reading and writing JSON files."""

    def __init__(self, default: function, folder: str):
        """
        :param default: Function providing default value
        :param folder: Folder to write files to
        """
        self.default = default
        self.folder = folder

    def get_filename(self, name: str):
        """
        Formats filename.
        :param name: Filename
        :return:
        """
        return f'{self.folder}/{name}.json'

    def save_file(self, name: str, data):
        """
        Saves file according to format.
        :param name:
        :param data:
        :return:
        """
        with open(self.get_filename(name), "w") as f:
            json.dump(data, f)

    def load_file(self, name: str):
        """
        Loads file from name.
        :param name:
        :return:
        """
        if not os.path.isfile(self.get_filename(name)):
            self.save_file(name, self.default(name))
        with open(self.get_filename(name), "r") as f:
            return json.load(f)
