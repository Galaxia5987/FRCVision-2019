import math

import cv2

import constants
import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """The Fuel ball from FIRST Steamworks."""

    def __init__(self, main):
        super().__init__(main)

    def create_mask(self, frame, hsv):
        mask = utils.hsv_mask(frame, hsv)
        mask = utils.morphology(mask, self.kernel_big)
        mask = utils.binary_thresh(mask, 127)
        mask = self.edge_detection(frame, mask)
        return mask

    def edge_detection(self, frame, mask):
        edge = utils.bitwise_and(frame, mask)
        edge = utils.canny_edge_detection(edge)
        edge = utils.binary_thresh(edge, 20)
        edge = utils.array8(edge)
        edge = utils.opening_morphology(edge, kernel_e=self.kernel_small, kernel_d=self.kernel_small)
        mask = utils.bitwise_not(mask, edge)
        mask = utils.closing_morphology(mask, kernel_d=self.kernel_medium, kernel_e=self.kernel_medium)
        return mask

    def find_contours(self, mask):
        img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy

    @staticmethod
    def filter_contours(contours, hierarchy):
        correct_contours = []

        if contours is not None:
            for cnt in contours:
                if len(cnt) < 50:
                    continue
                x, y, w, h = cv2.boundingRect(cnt)
                ratio = w / h
                area_circle_from_rect = math.pi * ((w / 2) ** 2)
                _, radius = cv2.minEnclosingCircle(cnt)

                area_circle = math.pi * (radius ** 2)

                area_ratio = area_circle / area_circle_from_rect

                if 0.75 < ratio < 1.25 and 0.75 < area_ratio < 1.25 and radius > 5:
                    correct_contours.append(cnt)

        return correct_contours

    @staticmethod
    def draw_contours(filtered_contours, original):
        for cnt in filtered_contours:
            (a, b), radius = cv2.minEnclosingCircle(cnt)
            center = (int(a), int(b))
            cv2.circle(original, center, int(radius), (255, 255, 0), 5)
            distance = utils.distance(constants.FOCAL_LENGTHS['lifecam'],
                                      constants.GAME_PIECE_SIZES['fuel']['diameter'],
                                      radius * 2)
            cv2.putText(original, str(int(distance * 100)), (int(a), int(b + 2 * radius)), cv2.FONT_HERSHEY_SIMPLEX, 2,
                        (0, 0, 0), 3)
