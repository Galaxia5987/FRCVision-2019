import cv2

from cv_camera import CVCamera
from pi_camera import PICamera


class Display:
    def __init__(self, exposure=-6, port=0, provider="cv"):
        if provider == "pi":
            self.camera_provider = PICamera(exposure)
        else:
            self.camera_provider = CVCamera(port, exposure)

    def get_frame(self):
        return self.camera_provider.frame

    def change_exposure(self, new_exposure):
        self.camera_provider.set_exposure(new_exposure)

    def release(self):
        self.camera_provider.release()
        cv2.destroyAllWindows()

    @staticmethod
    def show_frame(frame, title='image'):
        cv2.imshow(title, frame)
