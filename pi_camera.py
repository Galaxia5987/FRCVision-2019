import time
from threading import Thread


class PICamera(Thread):
    def __init__(self, exposure=0, contrast=7, framerate=32, resolution=(480, 368)):
        from picamera import PiCamera
        from picamera.array import PiRGBArray
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.exposure_compensation = exposure
        self.camera.contrast = contrast
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.exit = False
        self.frame = None
        print(f'Contrast: {contrast} Exposure: {exposure} FPS: {framerate}')
        time.sleep(0.1)
        super().__init__(daemon=True)

    def run(self):
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            if self.exit:
                break
            self.frame = frame.array
            self.rawCapture.truncate(0)

    def release(self):
        self.exit = True

    def set_exposure(self, exposure):
        self.camera.exposure_compensation = exposure
