import time
from importlib import import_module
from threading import Thread

import cv2

import argparse

import utils
from display import Display
from trackbars import Trackbars

parser = argparse.ArgumentParser()
# Add ui argument
parser.add_argument('-ui', action='store_true', default=False,
                    dest='ui',
                    help='Launch the user interface')
# Add stream argument
parser.add_argument('-web', action='store_true', default=False,
                    dest='web',
                    help='Run web server')
# Add local argument
parser.add_argument('-local', action='store_true', default=False,
                    dest='local',
                    help='Set a local to true')

parser.add_argument('-port', default=0, type=int) # Add camera port argument

parser.add_argument('-target', default='target', type=str) # Add target argument

results = parser.parse_args()

display = Display(results.port)

def loop():
    name = results.target
    target = import_module(f'targets.{name}').Target(name)

    trackbars = Trackbars(name)
    timer = time.time()
    avg = 0
    while True:
        frame = display.get_frame()
        # Separate frames for display purposes
        original = frame.copy()
        contour_image = frame.copy()
        # Target functions
        mask = target.create_mask(frame, trackbars.get_hsv())
        contours = target.find_contours(mask)
        filtered_contours = target.filter_contours(contours)
        # Draw contours
        target.draw_contours(filtered_contours, contour_image)
        # Show FPS
        avg = utils.calculate_fps(contour_image, time.time(), timer, avg)
        timer = time.time()
        #
        if results.local:
            display.show_frame(contour_image)
            display.show_frame(utils.bitwise_mask(original, mask), title="mask")
        if results.web:
            display.set_frame(contour_image)

        k = cv2.waitKey(1) & 0xFF  # large wait time to remove freezing
        if k in (27, 113):
            break

if results.stream:
    # Run web server
    Thread(target=display.run_app, daemon=True).start()
    # Print out ip and port for ease of use
    print("Web server: http://{}:{}".format(utils.get_ip(), 5987))

# Run main vision loop
loop()
