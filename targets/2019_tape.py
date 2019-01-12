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
        sorted_contours = sorted(filtered_contours, key=lambda cnt: cv2.minAreaRect(cnt)[1][0])
        last_angle = 0
        last_contour = None
        paired = []
        pairs = []
        for cnt in sorted_contours:
            if utils.np_array_in_list(cnt, paired):
                continue
            center, size, angle = cv2.minAreaRect(cnt)
            angle = utils.real_angle(angle, size)
            if last_angle and last_contour is not None:
                center2, size2, angle2 = cv2.minAreaRect(last_contour)
                angle2 = utils.real_angle(angle2, size)
                print(f'Angle: {angle}, Angle2: {angle2}')
                if angle2 < angle:
                    paired.extend([cnt, last_contour])
                    pairs.append((cnt, last_contour))
            last_angle = angle
            last_contour = cnt

        for pair in pairs:
            x, y, w, h = cv2.boundingRect(pair[0])
            x2, y2, w2, h2 = cv2.boundingRect(pair[1])
            cv2.rectangle(original, (x, y), (x2 + w2, y2 + h2), (0, 255, 0), 3)
