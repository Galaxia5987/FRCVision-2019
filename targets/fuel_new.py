import cv2

import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """A better version of recognition of the Fuel ball from FIRST Steamworks."""

    @staticmethod
    def is_circle(cnt, minimum):
        """
        Checks the circle ratio and returns true if it meets the minimum
        :param cnt:
        :param minimum:
        :return:
        """
        ratio = utils.circle_ratio(cnt)
        return minimum <= ratio <= 1

    def first_pass(self, contours):
        """
        First pass detection.
        :param contours:
        :return:
        """
        return [cnt for cnt in contours if cv2.contourArea(cnt) > 3_000 and self.is_circle(cnt, 0.8)]

    def filter_contours(self, contours, hierarchy):
        filtered_circles = self.first_pass(contours)
        final_contours = []
        filtered_children = []
        for cnt in filtered_circles:
            children = utils.get_children(cnt, contours, hierarchy)
            for c in children:
                if cv2.contourArea(c) > 300 and self.is_circle(c, 0.5):
                    circle_radius = cv2.minEnclosingCircle(c)[1]
                    filtered_radius = cv2.minEnclosingCircle(cnt)[1]
                    ratio = utils.circle_area(circle_radius) / utils.circle_area(filtered_radius)
                    if ratio >= 0.01:
                        final_contours.append(cnt)
                        filtered_children.append(c)
        return [final_contours, filtered_children]

    @staticmethod
    def draw_contours(filtered_contours, original):
        if not filtered_contours:
            return
        for cnt in filtered_contours[0]:
            (a, b), radius = cv2.minEnclosingCircle(cnt)
            center = (int(a), int(b))
            cv2.circle(original, center, int(radius), (255, 255, 0), 5)
        for child in filtered_contours[1]:
            (a, b), radius = cv2.minEnclosingCircle(child)
            center = int(a), int(b)
            cv2.circle(original, center, int(radius), (0, 0, 255), 5)
