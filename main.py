import time
from importlib import import_module
from threading import Thread

import cv2

import nt
import utils
from display import Display
from trackbars import Trackbars

display = Display()


def loop():
    # call the target
    name = "target"
    target = import_module(f'targets.{name}').Target(name)
    # create the network table and add values to it
    table = nt.nt_table()
    nt.load_values(table, name)
    # create HSV trackbars
    trackbars = Trackbars(name)
    # timer for FPS display
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
        # Display
        display.set_frame(contour_image)
        display.show_frame(contour_image)
        display.show_frame(utils.bitwise_mask(original, mask), title="mask")
        k = cv2.waitKey(1) & 0xFF  # large wait time to remove freezing
        if k in (27, 113):
            # save the values for the target and clear the table of their entries
            nt.save_values(name)
            nt.clear_table()
            break


if __name__ == "__main__":
    # Run web server
    Thread(target=display.run_app, daemon=True).start()
    # Print out ip and port for ease of use
    print("Web server: http://{}:{}".format(utils.get_ip(), 5987))
    # Run main vision loop
    loop()
