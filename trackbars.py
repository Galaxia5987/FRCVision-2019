import cv2

import utils


class Trackbars:
    def __init__(self, name):
        self.name = name
        self.create_trackbars()

    def callback(self, value):
        pass

    def save_to_file(self):
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

    @staticmethod
    def get_hsv():
        low_h = cv2.getTrackbarPos('lowH', 'HSV')
        high_h = cv2.getTrackbarPos('highH', 'HSV')
        low_s = cv2.getTrackbarPos('lowS', 'HSV')
        high_s = cv2.getTrackbarPos('highS', 'HSV')
        low_v = cv2.getTrackbarPos('lowV', 'HSV')
        high_v = cv2.getTrackbarPos('highV', 'HSV')
        return {"H": (low_h, high_h), "S": (low_s, high_s), "V": (low_v, high_v)}
