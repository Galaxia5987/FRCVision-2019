import cv2
import numpy as np

import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """The Tower light reflectors target from FIRST Stronghold."""

    @staticmethod
    def filter_contours(contours, hierarchy):
        correct_contours = []
        for cnt in contours:
            solidity = utils.aspect_ratio(cnt)
            if 0.3 < solidity < 0.36:
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
