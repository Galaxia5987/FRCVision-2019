import argparse
import time
from importlib import import_module

import cv2
from termcolor import colored

import nt_handler
import utils
from display import Display
from file_hsv import FileHSV
from trackbars import Trackbars
from web import Web


def get_args():
    """
    Add command line arguments.
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser()
    # Add web server argument
    parser.add_argument('-no-web', action='store_false', default=True,
                        dest='web',
                        help='Disable web server UI')
    parser.add_argument('-networktables', '-nt', action='store_true', default=False,
                        dest='networktables',
                        help='Initiate network tables')
    # Add local ui argument
    parser.add_argument('-local', action='store_true', default=False,
                        dest='local',
                        help='Launch local UI')
    # Add raspberry pi argument
    parser.add_argument('-pi', action='store_true', default=False,
                        dest='pi',
                        help='Use PI Camera')
    # Add camera port argument
    parser.add_argument('-port', default=0, dest='port', help='Camera port', type=int)
    # Add target argument
    parser.add_argument('-target', default='example_target', dest='target', help='Target file', type=str)
    return parser.parse_args()


class Main:
    def __init__(self):
        self.results = get_args()
        self.name = self.results.target
        # Check if requested target exists
        if not utils.is_target(self.name):
            return
        self.display = Display(self.results.port, provider="pi" if self.results.pi else "cv")
        if self.results.local:
            self.hsv_handler = Trackbars(self.name)
        else:
            self.hsv_handler = FileHSV(self.name)
        if self.results.web:
            self.web = Web(self)
            self.web.start_thread()  # Run web server
        if self.results.networktables:
            self.nt = nt_handler.NT(self.name)
        self.stop = False

    def change_name(self, name):
        """
        Changes the name and starts a new loop.
        :param name:
        """
        if not utils.is_target(name):
            return
        print(f'Changing target to {name}')
        self.name = name
        self.hsv_handler.name = name
        self.hsv_handler.reload()
        self.stop = True

    def loop(self):
        # Check if requested target exists
        if not utils.is_target(self.name, False):
            return
        print(colored(f'Starting loop with target {self.name}', 'green'))
        self.stop = False
        # We dynamically load classes in order to provide a modular base
        target = import_module(f'targets.{self.name}').Target()
        self.display.change_exposure(target.exposure)
        # Timer for FPS counter
        timer = time.time()
        avg = 0
        while True:
            frame = self.display.get_frame()
            if frame is None:
                print(colored("Couldn't read from camera", 'red'))
                break
            # Separate frames for display purposes
            original = frame.copy()
            contour_image = frame.copy()
            # Target functions
            mask = target.create_mask(frame, self.hsv_handler.get_hsv())
            contours, hierarchy = target.find_contours(mask)
            filtered_contours = target.filter_contours(contours, hierarchy)
            # Draw contours
            target.draw_contours(filtered_contours, contour_image)
            # Find distance and angle
            distance, angle = target.measurements(original, filtered_contours)
            # Show FPS
            avg = utils.calculate_fps(contour_image, time.time(), timer, avg)
            timer = time.time()
            # Display
            if self.results.web:
                self.web.set_frame(contour_image)
            if self.results.local:
                self.display.show_frame(contour_image)
                self.display.show_frame(utils.bitwise_and(original, mask), title='mask')
            if self.results.networktables:
                if distance:
                    self.nt.set_item('cube_distance', distance)
                if angle:
                    self.nt.set_item('cube_angle', angle)
            if self.stop:
                # If stop signal was sent we call loop again to start with new name
                print(colored('Restarting...', 'yellow'))
                self.loop()
                break
            k = cv2.waitKey(1) & 0xFF  # large wait time to remove freezing
            if k in (27, 113):
                print(colored('Q pressed, stopping...', 'red'))
                self.display.release()
                break


if __name__ == '__main__':
    Main().loop()
