from file import File


class FileHSV:
    """HSV value handler that loads values from a file."""
    def __init__(self, name):
        self.file = File(name, {'H': (0, 255), 'S': (0, 255), 'V': (0, 255)}, 'hsv', 'json')
        self.hsv = self.file.load_file()

    def reload(self):
        """
        Reload the values from file.
        :return:
        """
        self.hsv = self.file.load_file()

    def get_hsv(self):
        """
        Returns the cached HSV values.
        :return:
        """
        return self.hsv
