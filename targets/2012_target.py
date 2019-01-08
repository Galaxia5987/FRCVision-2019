import cv2
import numpy as np

import constants
import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """The light reflectors target from FIRST Rebound Rumble."""

    def __init__(self):
        super().__init__()
        self.exposure = -20

    @staticmethod
    def create_mask(frame, hsv):
        mask = utils.hsv_mask(frame, hsv)
        # create a cross kernel
        mask = utils.morphology(mask, np.array([[0, 1, 0],
                                                [1, 1, 1],
                                                [0, 1, 0]], dtype=np.uint8))
        mask = cv2.threshold(mask, 250, 255, 0)[1]
        return mask

    @staticmethod
    def filter_contours(contours, hierarchy):
        correct_contours = []
        all_children = []
        for cnt in contours:
            if utils.np_array_in_list(cnt, all_children):
                continue
            if cv2.contourArea(cnt) > 250:
                children = utils.get_children(cnt, contours, hierarchy)
                all_children.extend(children)
                if children:
                    for c in children:
                        area = cv2.contourArea(cnt)
                        children_area = cv2.contourArea(c)
                        ratio = children_area / area
                        if 0.57 < ratio < 0.73:
                            correct_contours.append(cnt)
                elif 0.15 < utils.solidity(cnt) < 0.45:
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
            cv2.drawContours(original, [box], 0, (255, 0, 255), 7)
            (a, b), radius = cv2.minEnclosingCircle(box)
            center = int(a), int(b)
            cv2.circle(original, center, int(radius), (0, 0, 255), 5)
            rect = cv2.minAreaRect(cnt)
            distance = utils.distance(constants.FOCAL_LENGTHS['lifecam'],
                                      constants.TARGET_SIZES['2012']['width'], max(rect[1][0], rect[1][1])) * 100 * 1.05
            angle = utils.angle(constants.FOCAL_LENGTHS['lifecam'], int(a), original)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(original, str(int(distance)), (int(a), int(b + radius)), font, 2, (255, 255, 255), 2,
                        cv2.LINE_AA)
