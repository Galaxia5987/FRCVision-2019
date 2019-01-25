import math

import cv2
import numpy as np

import constants
import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """The 2019 Slanted light reflection tape."""

    def __init__(self, main):
        super().__init__(main)
        self.exposure = -20

    def measurements(self, original, contours):
        pairs = self.get_pairs(contours)
        if not pairs:
            return None, None, None
        pair = pairs[0]
        x, y, w, h = cv2.boundingRect(pair[0])
        x2, y2, w2, h2 = cv2.boundingRect(pair[1])

        center = ((x + w) + x2) / 2
        angle = utils.angle(constants.FOCAL_LENGTHS['realsense'], center, original)
        distance = None
        field_angle = None

        if self.main.results.camera == 'realsense':
            distances = []
            avg_distances = []
            for tape in pair:
                for point in tape:
                    distances.append(self.main.display.camera_provider.get_distance(point[0][0], point[0][1]))
                avg_distances.append(np.median(distances))
                distances = []
            distance1 = avg_distances[0]
            distance2 = avg_distances[1]
            if distance1 and distance2:
                distance = (distance1 + distance2) / 2
                close_distance = min(distance1, distance2)
                tape_distance = constants.TARGET_SIZES['2019']['distance'] / 2

                top = distance ** 2 + tape_distance ** 2 - close_distance ** 2
                bottom = 2 * distance * tape_distance

                if utils.is_legal_traingle(distance, close_distance, tape_distance):
                    alpha = math.acos(top / bottom) * (180 / math.pi)
                    field_angle = 90 - alpha

        cv2.putText(original, str(int(angle)), (x + w, y + h), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 1,
                    cv2.LINE_AA)
        if distance:
            cv2.putText(original, str(int(distance * 100)), (x2, y2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 1,
                        cv2.LINE_AA)

        if field_angle:
            cv2.putText(original, str(int(field_angle)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 1,
                        cv2.LINE_AA)

        return angle, distance, field_angle

    @staticmethod
    def _is_correct(cnt):
        if cv2.contourArea(cnt) < 100:
            return False
        if 0.15 < utils.solidity(cnt) < 0.45:
            return True
        approx = utils.approx_poly(cnt)
        return approx > 1

    def filter_contours(self, contours, hierarchy):
        return [cnt for cnt in contours if self._is_correct(cnt)]

    @staticmethod
    def get_pairs(filtered_contours):
        sorted_contours = sorted(filtered_contours, key=lambda cnt: cv2.boundingRect(cnt)[0])
        already_paired = []
        pairs = []
        for last_cnt, cnt in zip(sorted_contours, sorted_contours[1:]):
            if utils.np_array_in_list(cnt, already_paired):
                continue
            center, size, angle = cv2.minAreaRect(cnt)
            center2, size2, angle2 = cv2.minAreaRect(last_cnt)
            delta = abs(angle2 - angle)
            if angle2 < angle and delta > 30:
                already_paired.extend([cnt, last_cnt])
                pairs.append((cnt, last_cnt))
        return pairs

    def draw_contours(self, filtered_contours, original):
        if not filtered_contours:
            return
        for cnt in filtered_contours:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(original, [box], 0, (0, 0, 255), 2)

        pairs = self.get_pairs(filtered_contours)

        for first, second in pairs:
            x, y, w, h = cv2.boundingRect(first)
            x2, y2, w2, h2 = cv2.boundingRect(second)
            cv2.rectangle(original, (x + w, y + h), (x2, y2), (0, 255, 0), 3)
