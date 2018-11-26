from file import File


class FileHSV:
    def __init__(self, name):
        self.file = File(name, lambda x: {'H': (0, 255), 'S': (0, 255), 'V': (0, 255)}, 'hsv', 'json')
        self.hsv = self.file.load_file()

    def reload(self):
        self.hsv = self.file.load_file()

    def get_hsv(self):
        return self.hsv
