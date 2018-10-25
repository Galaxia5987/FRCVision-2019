import cv2
import numpy as np

import utils


class Target:
    def __init__(self, name):
        self.name = name
        self.hsv = utils.load_file(name)
        self.kernel = np.array([[0, 1, 0],
                                [1, 1, 1],
                                [0, 1, 0]], dtype=np.uint8)

    def create_mask(self, frame):
        mask = utils.hsv_mask(frame, self.hsv)
        # create a cross kernel
        mask = utils.morphology(mask, self.kernel)
        _, mask = cv2.threshold(mask, 127, 255, 0)
        return mask

    def find_contours(self, mask):
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def filter_contours(self, contours):
        correct_contours = []

        if contours is not None:
            for cnt in contours:
                if 1000 < cv2.contourArea(cnt) < 10000:
                    correct_contours.append(cnt)

        return correct_contours

    def draw_contours(self, filtered_contours, original):
        cv2.drawContours(original, filtered_contours, -1, (255, 255, 0), 3)
