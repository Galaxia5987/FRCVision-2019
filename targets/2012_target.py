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

    @staticmethod
    def filter_contours(contours, hierarchy):
        correct_contours = []
        for cnt in contours:
            if cv2.contourArea(cnt) > 250:
                children = utils.get_children(cnt, contours, hierarchy)
                if len(children) >= 1:
                    for c in children:
                        area = cv2.contourArea(cnt)
                        children_area = cv2.contourArea(c)
                        ratio = children_area/area
                        if 0.57 < ratio < 0.73:
                            correct_contours.append(cnt)
                else:
                    solidity = utils.solidity(cnt)
                    if 0.15 < solidity < 0.45:
                        correct_contours.append(cnt)
                        print(utils.solidity(cnt))

        return correct_contours

    @staticmethod
    def draw_contours(filtered_contours, original):
        if not filtered_contours:
            return
        for cnt in filtered_contours:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(original, [box], 0, (255, 0, 255), 7)
