import logging

import cv2

import constants
import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """The Gear from FIRST Steamworks."""

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

    @staticmethod
    def filter_contours(contours, hierarchy):
        filtered_contours = []
        for cnt in contours:
            if cv2.contourArea(cnt) < 1_000:
                continue
            triangles = []
            circles = []
            for child in utils.get_children(cnt, contours, hierarchy):
                if cv2.contourArea(child) < 200:
                    continue
                if utils.is_circle(child, 0.7):
                    circles.append(child)
                if utils.is_triangle(child):
                    triangles.append(child)
            if len(triangles) > 3 and circles:
                for triangle in triangles:
                    if cv2.contourArea(triangle) / cv2.contourArea(cnt) >= 0.04:
                        filtered_contours.append(cnt)
        return filtered_contours

    @staticmethod
    def draw_contours(filtered_contours, original):
        if not filtered_contours:
            return
        for cnt in filtered_contours:
            (a, b), radius = cv2.minEnclosingCircle(cnt)
            distance = utils.distance(constants.FOCAL_LENGTHS['lifecam'],
                                      constants.GAME_PIECE_SIZES['gear']['diameter'],
                                      radius * 2) * 100
            angle = utils.angle(constants.FOCAL_LENGTHS['lifecam'], a, original)
            logging.debug(f'Distance: {distance}')
            logging.debug(f'Angle: {angle}')
            center = int(a), int(b)
            cv2.circle(original, center, int(radius), (255, 255, 0), 5)
