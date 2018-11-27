import cv2
import numpy as np

import utils


class Target:
    def __init__(self, name):
        self.name = name
        self.kernel = np.array([[0, 1, 0],
                                [1, 1, 1],
                                [0, 1, 0]], dtype=np.uint8)

    def create_mask(self, frame, hsv):
        mask = utils.hsv_mask(frame, hsv)
        # create a cross kernel
        mask = utils.morphology(mask, self.kernel)
        mask = cv2.threshold(mask, 127, 255, 0)[1]
        return mask

    @staticmethod
    def find_contours(mask):
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy

    @staticmethod
    def filter_contours(contours, hierarchy):
        correct_contours = []

        if contours is not None:
            for cnt in contours:
                if 1000 < cv2.contourArea(cnt) < 10000:
                    correct_contours.append(cnt)

        return correct_contours

    @staticmethod
    def draw_contours(filtered_contours, original):
        cv2.drawContours(original, filtered_contours, -1, (255, 255, 0), 3)
