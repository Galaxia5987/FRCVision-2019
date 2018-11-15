import json
import os


class File:
    def __init__(self, default, folder):
        self.default = default
        self.folder = folder

    def get_filename(self, name):
        return f'{self.folder}/{name}.json'

    def save_file(self, name, data):
        with open(self.get_filename(name), "w") as f:
            json.dump(data, f)

    def load_file(self, name):
        if not os.path.isfile(self.get_filename(name)):
            self.save_file(name, self.default(name))
        with open(self.get_filename(name), "r") as f:
            return json.load(f)
