import time
from threading import Thread

from picamera import PiCamera
from picamera.array import PiRGBArray


class PICamera:
    def __init__(self, exposure, contrast=7, framerate=32):
        self.camera = PiCamera()
        self.camera.resolution = (480, 368)
        self.camera.framerate = framerate
        self.camera.exposure_compensation = exposure
        self.camera.contrast = contrast
        self.rawCapture = PiRGBArray(self.camera, size=(480, 368))
        self.exit = False
        self.frame = None
        print(f'Contrast: {contrast} Exposure: {exposure} FPS: {framerate}')
        time.sleep(0.1)
        Thread(target=self.loop).start()

    def loop(self):
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            if self.exit:
                break
            self.frame = frame.array
            self.rawCapture.truncate(0)

    def release(self):
        self.exit = True

    def set_exposure(self, exposure):
        self.camera.exposure = exposure
