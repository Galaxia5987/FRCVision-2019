import os

import cv2
from termcolor import colored


class Display:
    def __init__(self, provider):
        self.codec = cv2.VideoWriter_fourcc(*'XVID')
        self.record = False
        self.out = None
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
        if self.out:
            self.out.release()
        self.camera_provider.release()
        cv2.destroyAllWindows()

    def start_recording(self, title):
        if not os.path.isdir('recordings'):
            os.makedirs('recordings')
        self.record = True
        self.out = cv2.VideoWriter(f'recordings/{title}.avi', self.codec, 30.0, (640, 480))

    def stop_recording(self):
        if self.out:
            colored('Releasing video recorder', 'green')
            self.out.release()

    def show_frame(self, frame, title='image'):
        """
        Show frame to screen.
        :param frame: OpenCV frame
        :param title: Window title
        """

        cv2.imshow(title, frame)
        if self.record and title == 'contour image' and self.out:
            self.out.write(frame)
