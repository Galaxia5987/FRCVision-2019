import cv2

import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """An example target."""

    @staticmethod
    def filter_contours(contours, hierarchy):
        filtered_contours = []
        for cnt in contours:
            if cv2.contourArea(cnt) < 50:
                return
            children = utils.get_children(cnt, contours, hierarchy)
            for child in children:
                if utils.is_circle(child, 0.5):
                    filtered_contours.append(cnt)
        return filtered_contours

    @staticmethod
    def draw_contours(filtered_contours, original):
        cv2.drawContours(original, filtered_contours, -1, (255, 255, 0), 3)
