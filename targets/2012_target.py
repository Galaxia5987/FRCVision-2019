import cv2
import numpy as np

import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """The light reflectors target from FIRST Rebound Rumble."""

    def __init__(self):
        self.kernel_b = np.array([[0, 1, 0],
                                  [1, 1, 1],
                                  [0, 1, 0]], dtype=np.uint8)

    def find_contours(self, mask):
        img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy

    @staticmethod
    def filter_contours(contours, hierarchy):
        correct_contours = []
        for cnt in contours:
            solidity = utils.solidity(cnt)
            if 0.8 < solidity < 1:
                if cv2.contourArea(cnt) > 500:
                    correct_contours.append(cnt)

        return correct_contours

    @staticmethod
    def draw_contours(filtered_contours, original):
        if not filtered_contours:
            return
        for cnt in filtered_contours:
            print(utils.solidity(cnt))
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(original, [box], 0, (0, 0, 255), 2)
