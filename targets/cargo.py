import cv2
import utils

from targets.target_base import TargetBase


class Target(TargetBase):
    """The cargo in the 2019."""

    @staticmethod
    def filter_contours(contours, hierarchy):
        correct_contours = []

        if contours:
            for cnt in contours:
                if utils.is_circle(cnt, 0.85):
                    correct_contours.append(cnt)

        return correct_contours

    @staticmethod
    def draw_contours(filtered_contours, original):
        if filtered_contours:
            for cnt in filtered_contours:
                cv2.drawContours(original, cnt, -1, (255, 255, 0), -1)
                cv2.circle(original, utils.center(cnt), int(utils.width(cnt)[0] / 2), (0, 255, 0), -1)
