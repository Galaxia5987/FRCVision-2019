import cv2

import constants


class Display:
    def __init__(self, exposure=-6, port=0):
        self.camera = cv2.VideoCapture(port)
        self.camera.set(constants.CAMERA_CONTRAST, 7)
        self.camera.set(constants.CAMERA_EXPOSURE, exposure)
        print(f'Contrast: {self.camera.get(constants.CAMERA_CONTRAST)} Exposure: {self.camera.get(constants.CAMERA_EXPOSURE)} FPS: {self.camera.get(constants.CAMERA_FPS)}')

    def get_frame(self):
        return self.camera.read()[1]

    def change_exposure(self, new_exposure):
        self.camera.set(constants.CAMERA_EXPOSURE, new_exposure)

    @staticmethod
    def show_frame(frame, title='image'):
        cv2.imshow(title, frame)
