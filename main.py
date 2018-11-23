import os
import time
import atexit
from importlib import import_module

import cv2
from termcolor import colored

import argparse

import nt_handler
import utils
from display import Display
from trackbars import Trackbars
from web import Web

parser = argparse.ArgumentParser()

# Add web server argument
parser.add_argument('-web', action='store_true', default=False,
                    dest='web',
                    help='Runs web server')
# Add local argument
parser.add_argument('-local', action='store_true', default=False,
                    dest='local',
                    help='Runs local UI')
class Main:
    def __init__(self):
        self.name = 'example_target'
        self.display = Display()
        self.trackbars = Trackbars(self.name)
        self.web = Web(self)
        self.web.start_thread()  # Run web server
        self.nt = nt_handler.NT(self.name)
        self.stop = False
        atexit.register(self.nt.save_values)

# Add network tables argument
parser.add_argument('-nt', action='store_true', default=False,
                    dest='nt',
                    help='Runs network tables')

parser.add_argument('-port', default=0, type=int) # Add camera port argument

parser.add_argument('-target', default='target', type=str) # Add target argument

results = parser.parse_args()

display = Display(results.port)

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
        target = import_module(f'targets.{self.name}').Target(self.name)
        # Timer for FPS counter
        timer = time.time()
        avg = 0
        while True:
            frame = self.display.get_frame()
            if frame is None:
                print(colored("Couldn't read from webcam", 'red'))
                break
            # Separate frames for display purposes
            original = frame.copy()
            contour_image = frame.copy()
            # Target functions
            mask = target.create_mask(frame, self.trackbars.get_hsv())
            contours = target.find_contours(mask)
            filtered_contours = target.filter_contours(contours)
            # Draw contours
            target.draw_contours(filtered_contours, contour_image)
            # Show FPS
            avg = utils.calculate_fps(contour_image, time.time(), timer, avg)
            timer = time.time()
            # Display
            if results.local:
                self.display.show_frame(contour_image)
                self.display.show_frame(utils.bitwise_mask(original, mask), title='mask')
            if results.web:
                self.web.set_frame(contour_image)
            if self.stop:
                # If stop signal was sent we call loop again to start with new name
                print(colored('Restarting...', 'yellow'))
                self.loop()
                break
            if k in (27, 113):
                print(colored('Q pressed, stopping...', 'red'))
                break
            k = cv2.waitKey(1) & 0xFF  # large wait time to remove freezing

if results.stream:
    # Run web server
    Thread(target=display.run_app, daemon=True).start()
    # Print out ip and port for ease of use
    print("Web server: http://{}:{}".format(utils.get_ip(), 5987))

if __name__ == '__main__':
    Main().loop()
