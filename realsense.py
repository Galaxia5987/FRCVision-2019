from threading import Thread

import numpy

import pyrealsense2 as rs


class Realsense():
    def __init__(self):
        config = rs.config()
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
        self.pipeline = rs.pipeline()
        self.pipeline.start(config)
        self.exit = False
        self.depth_frame = None

    @property
    def frame(self):
        frames = self.pipeline.wait_for_frames()
        self.depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        return numpy.asanyarray(color_frame.get_data())

    def start(self):
        """Implementation of Thread run method, stores frames in a class variable."""
        pass

    def release(self):
        """Release the camera and loop."""
        self.exit = True
        self.pipeline.stop()

    def get_resolution(self):
        return 640, 480

    def get_distance(self, width, height):
        return self.depth_frame(width, height)
