import cv2

import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """Hatch panel ye mum."""

    @staticmethod
    def _is_correct(cnt):
        if cv2.contourArea(cnt) < 200:
            return False
        return utils.is_circle(cnt, 0.6)

    def filter_contours(self, contours, hierarchy):
        return [cnt for cnt in contours if self._is_correct(cnt)]

    @staticmethod
    def draw_contours(filtered_contours, original):
        if not filtered_contours:
            return
        cv2.drawContours(original, filtered_contours, -1, (255, 255, 0), 3)
