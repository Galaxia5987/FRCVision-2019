import time
from importlib import import_module

import cv2

import utils
from display import Display
from trackbars import Trackbars
from web import Web


class Main:
    def __init__(self):
        self.name = "example_target"
        self.display = Display()
        self.trackbars = Trackbars(self.name)
        self.web = Web(self)
        # Run web server
        self.web.start_thread()
        # Run main vision loop
        self.stop = False

    def change_name(self, name):
        print(f'Changing target to {name}')
        self.name = name
        self.trackbars.name = name
        self.trackbars.reload_trackbars()
        self.stop = True

    def loop(self):
        print(f'Starting loop with target {self.name}')
        self.stop = False
        target = import_module(f'targets.{self.name}').Target(self.name)
        timer = time.time()
        avg = 0
        while True:
            frame = self.display.get_frame()
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
            self.web.set_frame(contour_image)
            self.display.show_frame(contour_image)
            self.display.show_frame(utils.bitwise_mask(original, mask), title="mask")
            k = cv2.waitKey(1) & 0xFF  # large wait time to remove freezing
            if self.stop:
                print("Restarting...")
                self.loop()
                break
            if k in (27, 113):
                print("Q pressed, stopping...")
                break


if __name__ == "__main__":
    main = Main()
    main.loop()
