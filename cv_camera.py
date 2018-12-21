from threading import Thread

import cv2

import constants


class CVCamera(Thread):
    def __init__(self, port, exposure=0, contrast=7):
        # Start video capture on desired port
        self.camera = cv2.VideoCapture(port)
        self.camera.set(constants.CAMERA_CONTRAST, contrast)
        self.set_exposure(exposure)
        self.exit = False
        self.frame = None
        print(f'Contrast: {contrast} Exposure: {exposure} FPS: {self.camera.get(constants.CAMERA_FPS)}')
        super().__init__(daemon=True)  # Init thread

    def run(self):
        """
        Implementation of Thread run method, stores frames in a class variable.
        :return:
        """
        while True:
            if self.exit:
                break
            self.frame = self.camera.read()[1]

    def release(self):
        """
        Releases the camera and loop.
        :return:
        """
        self.exit = True
        self.camera.release()

    def set_exposure(self, exposure):
        """
        Sets the camera exposure.
        :param exposure:
        :return:
        """
        self.camera.set(constants.CAMERA_EXPOSURE, exposure)
