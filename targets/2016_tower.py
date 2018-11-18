import cv2
import numpy as np
import utils


class Target:
    def __init__(self, name):
        self.name = name
        self.kernel = np.array([[0, 1, 0],
                                [1, 1, 1],
                                [0, 1, 0]], dtype=np.uint8)

    @classmethod
    def filter_contours(cls, contours):
        # create a cross kernel
        mask = utils.morphology(mask, self.kernel)
        mask = cv2.threshold(mask, 127, 255, 0)[1]
        return mask

    @staticmethod
    def find_contours(mask):
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

        correct_contours = []
        for cnt in contours:
            solidity = utils.solidity(cnt)
            if 0.3 < solidity < 0.36:
                correct_contours.append(cnt)

        return correct_contours

    @classmethod
    def draw_contours(cls, filtered_contours, original):
        if not filtered_contours:
            return
        for cnt in filtered_contours:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(original, [box], 0, (0, 0, 255), 2)
