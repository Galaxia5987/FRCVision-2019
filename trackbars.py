import json
import os

import cv2

import utils
from display import Display


class Trackbars:
    def __init__(self, file):
        self.default = {"H": (0, 255), "S": (0, 255), "V": (0, 255)}
        self.file = file
        self.create_trackbars()

    def get_filename(self):
        return "hsv/{}.json".format(self.file)

    def load_file(self):
        if not os.path.isfile(self.get_filename()):
            return self.default
        with open(self.get_filename(), "r") as f:
            return json.load(f)

    def save_file(self, value):
        with open(self.get_filename(), "w") as f:
            json.dump(self.get_hsv(), f)

    def create_trackbars(self):
        cv2.namedWindow("HSV")

        hsv = self.load_file()
        # create trackbars for color change
        cv2.createTrackbar('lowH', 'HSV', hsv['H'][0], 179, self.save_file)
        cv2.createTrackbar('highH', 'HSV', hsv['H'][1], 179, self.save_file)

        cv2.createTrackbar('lowS', 'HSV', hsv['S'][0], 255, self.save_file)
        cv2.createTrackbar('highS', 'HSV', hsv['S'][1], 255, self.save_file)

        cv2.createTrackbar('lowV', 'HSV', hsv['V'][0], 255, self.save_file)
        cv2.createTrackbar('highV', 'HSV', hsv['V'][1], 255, self.save_file)

    def get_hsv(self):
        lowH = cv2.getTrackbarPos('lowH', 'HSV')
        highH = cv2.getTrackbarPos('highH', 'HSV')
        lowS = cv2.getTrackbarPos('lowS', 'HSV')
        highS = cv2.getTrackbarPos('highS', 'HSV')
        lowV = cv2.getTrackbarPos('lowV', 'HSV')
        highV = cv2.getTrackbarPos('highV', 'HSV')
        return {"H": (lowH, highH), "S": (lowS, highS), "V": (lowV, highV)}


def run(target):
    display = Display()
    trackbars = Trackbars(target)
    while True:
        frame = display.get_frame()
        mask = utils.mask(frame, trackbars.get_hsv())
        frame = cv2.bitwise_and(frame, frame, mask=mask)
        display.show_frame(frame)
        k = cv2.waitKey(100) & 0xFF  # Wait time to remove freezing
        if k in (27, 113):
            break


if __name__ == "__main__":
    run("test")
