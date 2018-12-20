import cv2


class Display:
    def __init__(self, provider):
        self.camera_provider = provider
        self.camera_provider.start()

    def get_frame(self):
        """
        Returns the most current frame from the camera provider.
        :return:
        """
        return self.camera_provider.frame

    def change_exposure(self, new_exposure):
        """
        Changes the exposure through the camera provider.
        :param new_exposure:
        :return:
        """
        self.camera_provider.set_exposure(new_exposure)

    def release(self):
        """
        Releases the camera and destroys windows.
        :return:
        """
        self.camera_provider.release()
        cv2.destroyAllWindows()

    @staticmethod
    def show_frame(frame, title='image'):
        """
        Shows frame to screen.
        :param frame:
        :param title:
        :return:
        """
        cv2.imshow(title, frame)
