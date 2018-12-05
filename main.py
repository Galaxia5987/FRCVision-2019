import os
import time
import atexit
from importlib import import_module

import cv2
import numpy as np
from termcolor import colored

import nt_handler
import utils
from display import Display
from trackbars import Trackbars
from web import Web


class Main:
    def __init__(self):
        self.name = 'cube'
        self.display = Display()
        self.trackbars = Trackbars(self.name)
        self.web = Web(self)
        self.web.start_thread()  # Run web server
        self.nt = nt_handler.NT(self.name)
        self.stop = False
        atexit.register(self.nt.save_values)

        self.counter = 0

    def change_name(self, name):
        """
        Changes the name and starts a new loop.
        :param name:
        """
        if not os.path.isfile(f'targets/{name}.py'):
            print(colored('Target doesn\'t exist', 'red'))
            return
        print(f'Changing target to {name}')
        self.name = name
        self.trackbars.name = name
        self.trackbars.reload_trackbars()
        self.stop = True

    def loop(self):

        print(colored(f'\nStarting loop with target {self.name}', 'green'))
        self.stop = False
        # We dynamically load classes in order to provide a modular base
        target = import_module(f'targets.{self.name}').Target()
        # Timer for FPS counter
        timer = time.time()
        avg = 0
        while True:
            if self.counter != 3:
                self.counter += 1
            else:
                self.counter = 0
                frame = self.display.get_frame()
                if frame is None:
                    print(colored("Couldn't read from webcam", 'red'))
                    break

                # Separate frames for display purposes
                original = frame.copy()
                contour_image = frame.copy()

                # Target functions
                mask = target.create_mask(frame, self.trackbars.get_hsv())
                mask = target.edge_detection(frame, mask)
                contours = target.find_contours(mask)
                filtered_contours = target.filter_contours(contours)

                # Show FPS
                avg = utils.calculate_fps(contour_image, time.time(), timer, avg)
                timer = time.time()

                # Display
                cut_mask = utils.bitwise_and(original, mask)
                self.display.show_frame(cut_mask, 'mask')
                # Draw contours
                target.draw_contours(filtered_contours, contour_image)
                self.web.set_frame(contour_image)
                self.display.show_frame(contour_image, 'image')

                k = cv2.waitKey(1) & 0xFF  # large wait time to remove freezing
                if self.stop:
                    # If stop signal was sent we call loop again to start with new name
                    print(colored('Restarting...', 'yellow'))
                    self.loop()
                    break
                if k in (27, 113):
                    print(colored('Q pressed, stopping...', 'red'))
                    break


if __name__ == '__main__':
    Main().loop()
