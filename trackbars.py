import cv2

import utils
from display import Display


class Trackbars:
    def __init__(self, name):
        self.name = name
        self.create_trackbars()

    def callback(self, value):
        utils.save_file(self.name, self.get_hsv())

    def create_trackbars(self):
        cv2.namedWindow("HSV")

        hsv = utils.load_file(self.name)
        # create trackbars for color change
        cv2.createTrackbar('lowH', 'HSV', hsv['H'][0], 179, self.callback)
        cv2.createTrackbar('highH', 'HSV', hsv['H'][1], 179, self.callback)

        cv2.createTrackbar('lowS', 'HSV', hsv['S'][0], 255, self.callback)
        cv2.createTrackbar('highS', 'HSV', hsv['S'][1], 255, self.callback)

        cv2.createTrackbar('lowV', 'HSV', hsv['V'][0], 255, self.callback)
        cv2.createTrackbar('highV', 'HSV', hsv['V'][1], 255, self.callback)

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
        mask = utils.hsv_mask(frame, trackbars.get_hsv())
        frame = cv2.bitwise_and(frame, frame, mask=mask)
        display.show_frame(frame)
        k = cv2.waitKey(1) & 0xFF  # Wait time to remove freezing
        if k in (27, 113):
            break


if __name__ == "__main__":
    run("power_cube")
