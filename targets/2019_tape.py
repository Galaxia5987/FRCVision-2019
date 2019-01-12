import cv2
import numpy as np

import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """The 2019 Slanted light reflection tape."""

    def __init__(self):
        super().__init__()
        self.exposure = -20

    @staticmethod
    def filter_contours(contours, hierarchy):
        correct_contours = []
        for cnt in contours:
            if cv2.contourArea(cnt) < 100: continue
            if 0.15 < utils.solidity(cnt) < 0.45:
                correct_contours.append(cnt)
            else:
                approx = utils.approx_poly(cnt)
                if approx > 1:
                    correct_contours.append(cnt)
        return correct_contours

    @staticmethod
    def draw_contours(filtered_contours, original):
        if not filtered_contours:
            return
        for cnt in filtered_contours:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(original, [box], 0, (0, 0, 255), 2)
