import cv2

from targets.target_base import TargetBase


class Target(TargetBase):
    """An example target."""

    @staticmethod
    def filter_contours(contours, hierarchy):
        correct_contours = []

        if contours is not None:
            for cnt in contours:
                if 1000 < cv2.contourArea(cnt) < 10000:
                    correct_contours.append(cnt)

        return correct_contours

    @staticmethod
    def draw_contours(filtered_contours, original):
        if not filtered_contours:
            return
        cv2.drawContours(original, filtered_contours, -1, (255, 255, 0), 3)
