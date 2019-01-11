import math

import cv2
import numpy as np

import constants
import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """Power cube from the 2018 mission."""

    def __init__(self):
        super().__init__()
        self.correction = 25

    def create_mask(self, frame, hsv):
        mask = utils.hsv_mask(frame, hsv)
        mask = utils.morphology(mask, self.kernel_big)
        mask = utils.binary_thresh(mask, 127)
        mask = self.edge_detection(frame, mask)
        mask = self.separate_cubes(mask)

        return mask

    def edge_detection(self, frame, mask):
        edge = utils.bitwise_and(frame, mask)
        edge = utils.canny_edge_detection(edge, min_val=100, max_val=125)
        edge = utils.binary_thresh(edge, 127)
        edge = utils.array8(edge)
        edge = utils.dilate(edge, self.kernel_small, itr=3)
        edge = utils.opening_morphology(edge, kernel_e=self.kernel_small, kernel_d=self.kernel_small, itr=3)
        mask = utils.bitwise_not(mask, edge)
        mask = utils.erode(mask, self.kernel_medium, itr=3)
        mask = utils.closing_morphology(mask, kernel_d=self.kernel_medium, kernel_e=self.kernel_medium, itr=3)

        return mask

    def separate_cubes(self, mask):
        contours = self.find_contours(mask)[0]
        total_areas = []

        for cnt in contours:
            cnt = utils.approx_hull(cnt)
            area = cv2.contourArea(cnt)
            total_areas.append(area)
            avg_area = sum(total_areas) / len(total_areas)
            if len(cnt) > 3 and area > 100 and area / avg_area >= 1.5:
                aspect_ratio = utils.rotated_aspect_ratio(cnt)
                reversed_aspect_ratio = utils.reversed_rotated_aspect_ratio(cnt)
                if 3 > reversed_aspect_ratio >= 0.7 or 3 > aspect_ratio >= 0.7:
                    side = max(utils.width(cnt), utils.height(cnt), key=utils.index0)[0]
                    (x1, y1), (x2, y2) = min(utils.width(cnt), utils.height(cnt), key=utils.index0)[1:]
                    cubes = round(max(aspect_ratio / (utils.power_cube['width'] / utils.power_cube['height']),
                                      reversed_aspect_ratio) / (utils.power_cube['height'] / utils.power_cube['width']))
                    single_cube = side / cubes
                    vertical = 0
                    horizontal = 0
                    if utils.width(cnt) >= utils.height(cnt):
                        vertical = 1
                    else:
                        horizontal = 1
                    for i in range(1, cubes + 1):
                        cv2.line(mask,
                                 (int(x2 + single_cube * vertical * i), int(y2 + single_cube * horizontal * i)),
                                 (int(x1 + single_cube * vertical * i), int(y1 + single_cube * horizontal * i)),
                                 (0, 0, 0), thickness=15)

        return mask

    @staticmethod
    def filter_contours(contours, hierarchy):
        filtered_contours = []

        if contours:
            total_areas = []
            for cnt in contours:
                area = cv2.contourArea(cnt)
                total_areas.append(area)
                avg_area = sum(total_areas) / len(total_areas)
                if len(cnt) > 2 and area > 750 and 0.2 < utils.rotated_aspect_ratio(cnt) and 4 <= len(
                        utils.points(cnt)) <= 6 and area / avg_area >= 1.25:
                    filtered_contours.append(cnt)

        return filtered_contours

    @staticmethod
    def measurements(original, contours):
        if not contours:
            return None, None
        distances = []
        for cnt in contours:
            points = utils.box(cnt)
            if not points.any():
                return None, None

            avg_real_heights = sum(utils.power_cube.values()) / len(utils.power_cube)

            heights = []
            for i, point in enumerate(points):
                x = point[0] - points[i - 1][0]
                y = point[1] - points[i - 1][1]
                height = math.hypot(x, y)
                heights.append(height)

            if len(points) == 5:
                max_height = max(heights)
                half_height = max_height / 2
                heights.remove(max_height)
                heights.extend([half_height] * 2)

            avg_heights = sum(heights) / len(heights)

            distances.append((avg_real_heights * constants.FOCAL_LENGTHS['lifecam']) / avg_heights)

        min_distance = min(distances)
        chosen_one = contours[distances.index(min_distance)]
        angle = utils.angle(constants.FOCAL_LENGTHS['lifecam'], utils.center(chosen_one)[0], original)

        return min_distance, angle, chosen_one

    @staticmethod
    def draw_contours(filtered_contours, original):
        if filtered_contours:
            for cnt in filtered_contours:
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                approx = utils.approx_hull(cnt)
                cv2.drawContours(original, [approx], 0, (255, 0, 0), 2)

                cv2.drawContours(original, [box], 0, (0, 0, 255), 2)

                points = utils.points(cnt)
                for point in points:
                    cv2.circle(original, point, 5, (0, 255, 0), -1)
                    cv2.putText(original, str(points.index(point)), (point[0] + 5, point[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 0))
