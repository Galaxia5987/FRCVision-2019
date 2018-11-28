from file import File


class FileHSV:
    """HSV value handler that loads values from a file."""

    def __init__(self, name):
        """
        Instantiate a HSV value handler.
        :param name: Target name
        """
        self.file = File(name, {'H': (0, 255), 'S': (0, 255), 'V': (0, 255)}, 'hsv', 'json')
        self.hsv_values = self.file.load_file()

    def save_hsv_values(self):
        """Implement this method as a dry method because this handler doesn't save values."""
        pass

    def reload(self):
        """Reload the values from file."""
        self.hsv_values = self.file.load_file()

    def get_hsv(self) -> dict:
        """
        Get current HSV.

        This method is here to allow diversity, so we can use FileHSV and also Trackbars.
        :return: Cached HSV values
        """
        return self.hsv_values
