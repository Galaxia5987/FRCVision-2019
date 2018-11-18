import math

import cv2

import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """CLass representing the Fuel ball from FIRST Steamworks."""

    @classmethod
    def filter_contours(cls, contours):
        correct_contours = []

        if contours is not None:
            for cnt in contours:
                if len(cnt) < 50:
                    continue
                x, y, w, h = cv2.boundingRect(cnt)
                ratio = utils.aspect_ratio(w, h)
                area_circle_from_rect = math.pi * ((w / 2) ** 2)
                _, radius = cv2.minEnclosingCircle(cnt)

                area_circle = math.pi * (radius ** 2)

                area_ratio = area_circle / area_circle_from_rect

                if 0.75 < ratio < 1.25 and 0.75 < area_ratio < 1.25 and radius > 5:
                    correct_contours.append(cnt)

        return correct_contours

    @classmethod
    def draw_contours(cls, filtered_contours, original):
        for cnt in filtered_contours:
            (a, b), radius = cv2.minEnclosingCircle(cnt)
            center = (int(a), int(b))
            cv2.circle(original, center, int(radius), (255, 255, 0), 5)
