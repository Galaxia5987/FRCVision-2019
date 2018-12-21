import cv2


class Display:
    def __init__(self, provider):
        self.camera_provider = provider
        self.camera_provider.start()

    def get_frame(self):
        """
        Return the most current frame from the camera provider.
        :return: Latest frame
        """
        return self.camera_provider.frame

    def change_exposure(self, new_exposure: int):
        """
        Change the exposure through the camera provider.
        :param new_exposure: New exposure to set
        """
        self.camera_provider.set_exposure(new_exposure)

    def release(self):
        """Release the camera and destroys windows."""
        self.camera_provider.release()
        cv2.destroyAllWindows()

    @staticmethod
    def show_frame(frame, title='image'):
        """
        Show frame to screen.
        :param frame: OpenCV frame
        :param title: Window title
        """
        cv2.imshow(title, frame)
