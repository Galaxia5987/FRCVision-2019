import cv2

from targets.target_base import TargetBase


class ExampleTarget(TargetBase):
    @staticmethod
    def filter_contours(contours):
        correct_contours = []

        if contours is not None:
            for cnt in contours:
                if 1000 < cv2.contourArea(cnt) < 10000:
                    correct_contours.append(cnt)

        return correct_contours

    @staticmethod
    def draw_contours(filtered_contours, original):
        cv2.drawContours(original, filtered_contours, -1, (255, 255, 0), 3)
