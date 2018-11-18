import cv2
import numpy as np
import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """Class representing the Tower light reflectors target from FIRST Stronghold."""

    @classmethod
    def filter_contours(cls, contours):
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
