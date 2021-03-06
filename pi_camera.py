import logging
import time
from threading import Thread


class PICamera(Thread):
    def __init__(self, exposure=0, contrast=7, framerate=32, resolution=(320, 240)):
        # Hacky fix picamera only being able to be installed on a raspberry pi
        from picamera import PiCamera
        from picamera.array import PiRGBArray
        # Initiate camera
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.exposure_compensation = exposure
        self.camera.contrast = contrast
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.exit = False
        self.frame = None
        logging.info(f'Contrast: {contrast} Exposure: {exposure} FPS: {framerate}')
        time.sleep(0.1)  # Sleep to let the camera warm up
        super().__init__(daemon=True)

    def run(self):
        """Implementation of Thread run method, stores frames in a class variable."""
        # picamera iterator
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            if self.exit:
                break
            self.frame = frame.array
            self.rawCapture.truncate(0)

    def release(self):
        """Release camera by exiting the loop."""
        self.exit = True

    def set_exposure(self, exposure: int):
        """
        Set the camera exposure compensation.
        :param exposure:
        """
        self.camera.exposure_compensation = exposure

    def get_resolution(self):
        return self.camera.resolution
