import cv2
import numpy as np

import utils
import constants
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
            (a, b), radius = cv2.minEnclosingCircle(box)
            center = int(a), int(b)
            cv2.circle(original, center, int(radius), (0, 0, 255), 5)
            distance = utils.distance(constants.FOCAL['lifecam'], constants.TARGET_SIZE['2012']['closing_circle_radius'],radius )*100
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(original, str(int(distance)), (int(a), int(b+radius)), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
