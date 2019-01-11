import os

import cv2
from termcolor import colored


class Display:
    def __init__(self, provider):
        self.codec = cv2.VideoWriter_fourcc(*'XVID')
        self.is_recording = False
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
        print(colored(f'Starting recording with title {title}', 'green'))
        if not os.path.isdir('recordings'):
            os.makedirs('recordings')
        self.is_recording = True
        self.out = cv2.VideoWriter(f'recordings/{title}.avi', self.codec, 30.0, self.camera_provider.get_resolution())

    def stop_recording(self):
        if self.out:
            print(colored('Releasing video recorder', 'yellow'))
            self.out.release()

    def process_frame(self, frame, title: str, show: bool):
        """
        Show and or record frame.
        :param frame: OpenCV frame
        :param title: Window title
        :param show: Show or don't show to display
        :return:
        """
        if show:
            cv2.imshow(title, frame)
        if self.is_recording and title == 'contour image' and self.out:
            self.out.write(frame)


