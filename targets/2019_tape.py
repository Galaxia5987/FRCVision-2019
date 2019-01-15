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
    def _is_correct(cnt):
        if cv2.contourArea(cnt) < 100:
            return False
        if 0.15 < utils.solidity(cnt) < 0.45:
            return True
        approx = utils.approx_poly(cnt)
        return approx > 1

    def filter_contours(self, contours, hierarchy):
        return [cnt for cnt in contours if self._is_correct(cnt)]

    @staticmethod
    def draw_contours(filtered_contours, original):
        if not filtered_contours:
            return
        for cnt in filtered_contours:
            rect = cv2.minAreaRect(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.putText(original, str(int(rect[2])), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 1,
                        cv2.LINE_AA)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(original, [box], 0, (0, 0, 255), 2)
        sorted_contours = sorted(filtered_contours, key=lambda cnt: cv2.boundingRect(cnt)[0])
        already_paired = []
        pairs = []
        for last_contour, cnt in zip(sorted_contours, sorted_contours[1:]):
            if utils.np_array_in_list(cnt, already_paired):
                continue
            center, size, angle = cv2.minAreaRect(cnt)
            center2, size2, angle2 = cv2.minAreaRect(last_contour)
            delta = abs(angle2 - angle)
            if angle2 < angle and delta > 30:
                already_paired.extend([cnt, last_contour])
                pairs.append((cnt, last_contour))

        for first, second in pairs:
            x, y, w, h = cv2.boundingRect(first)
            x2, y2, w2, h2 = cv2.boundingRect(second)
            cv2.rectangle(original, (x + w, y + h), (x2, y2), (0, 255, 0), 3)
