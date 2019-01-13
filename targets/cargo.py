import cv2

import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """The cargo in the 2019."""

    @staticmethod
    def filter_contours(contours, hierarchy):
        correct_contours = []
        all_children = []
        if contours:
            for cnt in contours:
                if cv2.contourArea(cnt) < 200:
                    continue
                if utils.is_circle(cnt, 0.7):
                    all_children.extend(utils.get_children(cnt, contours, hierarchy))
                    correct_contours.append(cnt)
        for cnt in all_children:
            try:
                correct_contours.remove(cnt)
            except ValueError:
                continue
        return correct_contours

    @staticmethod
    def draw_contours(filtered_contours, original):
        if filtered_contours:
            for cnt in filtered_contours:
                (a, b), radius = cv2.minEnclosingCircle(cnt)
                center = int(a), int(b)
                cv2.circle(original, center, int(radius), (0, 255, 0), 5)
