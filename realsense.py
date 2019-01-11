from threading import Thread

import numpy

import pyrealsense2 as rs


class Realsense(Thread):
    def __init__(self):
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.pipeline = rs.pipeline()
        self.pipeline.start(config)
        self.exit = False
        self.frame = None
        self.depth_frame = None
        super().__init__(daemon=True)  # Init thread

    def run(self):
        """Implementation of Thread run method, stores frames in a class variable."""
        while True:
            if self.exit:
                break
            frames = self.pipeline.wait_for_frames()
            self.depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            self.frame = numpy.asanyarray(color_frame.get_data())

    def release(self):
        """Release the camera and loop."""
        self.exit = True
        self.pipeline.stop()

    def get_resolution(self):
        return 640, 480

    def get_distance(self, width, height):
        return self.depth_frame(width, height)
