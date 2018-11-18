import cv2

from targets.target_base import TargetBase


class ExampleTarget(TargetBase):

    @classmethod
    def filter_contours(cls, contours):
        correct_contours = []

        if contours is not None:
            for cnt in contours:
                if 1000 < cv2.contourArea(cnt) < 10000:
                    correct_contours.append(cnt)

        return correct_contours

    @classmethod
    def draw_contours(cls, filtered_contours, original):
        cv2.drawContours(original, filtered_contours, -1, (255, 255, 0), 3)
