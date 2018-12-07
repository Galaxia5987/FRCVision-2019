import cv2
import numpy as np

import constants
import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """The Gear from FIRST Steamworks."""

    def __init__(self):
        super().__init__()
        self.kernel_s = np.array([1], dtype=np.uint8)

        self.kernel_m = np.array([[1, 1],
                                  [1, 1]], dtype=np.uint8)
        self.kernel_b = np.array([[0, 1, 0],
                                  [1, 1, 1],
                                  [0, 1, 0]], dtype=np.uint8)

    def create_mask(self, frame, hsv):
        mask = utils.hsv_mask(frame, hsv)
        mask = utils.morphology(mask, self.kernel_b)
        mask = utils.binary_thresh(mask, 127)
        mask = self.edge_detection(frame, mask)
        return mask

    def edge_detection(self, frame, mask):
        edge = utils.bitwise_and(frame, mask)
        edge = utils.canny_edge_detection(edge)
        edge = utils.binary_thresh(edge, 20)
        edge = utils.array8(edge)
        edge = utils.opening_morphology(edge, kernel_e=self.kernel_s, kernel_d=self.kernel_s)
        mask = utils.bitwise_not(mask, edge)
        mask = utils.closing_morphology(mask, kernel_d=self.kernel_m, kernel_e=self.kernel_m)
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
                for tr in triangles:
                    if cv2.contourArea(tr) / cv2.contourArea(cnt) >= 0.04:
                        filtered_contours.append(cnt)
        return filtered_contours

    @staticmethod
    def draw_contours(filtered_contours, original):
        if not filtered_contours:
            return
        for cnt in filtered_contours:
            (a, b), radius = cv2.minEnclosingCircle(cnt)
            distance = utils.distance(constants.FOCAL['lifecam'], constants.GAME_PIECE_SIZE['gear']['diameter'],
                                      radius * 2) * 100
            angle = utils.angle(constants.FOCAL['lifecam'], a, original)
            print(f'Distance: {distance}')
            print(f'Angle: {angle}')
            center = (int(a), int(b))
            cv2.circle(original, center, int(radius), (255, 255, 0), 5)
