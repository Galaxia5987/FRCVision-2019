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
            if cv2.contourArea(cnt) < 100:
                continue
            if utils.approx_poly(cnt, ratio=0.08) != 4:
                continue
            center, size, angle = cv2.minAreaRect(cnt)
            ratio = min(size[0], size[1]) / max(size[0], size[1])
            if 0.2 < ratio < 0.5:
                if size[0] < size[1]:
                    print(angle)
                else:
                    print(angle + 90)

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
