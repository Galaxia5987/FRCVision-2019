import cv2

import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """The cargo in the 2019."""

    def create_mask(self, frame, hsv):
        edge = self.edge_detection(frame)
        mask = utils.hsv_mask(frame, hsv)
        mask = utils.binary_thresh(mask, 127)

        mask = utils.bitwise_not(mask, edge)
        mask = utils.closing_morphology(mask, kernel_d=self.kernel_medium, kernel_e=self.kernel_medium, itr=3)

        return mask

    def edge_detection(self, frame):
        edge = utils.canny_edge_detection(frame)
        edge = utils.binary_thresh(edge, 127)
        edge = utils.array8(edge)
        edge = utils.opening_morphology(edge, kernel_e=self.kernel_small, kernel_d=self.kernel_small, itr=3)

        return edge

    @staticmethod
    def filter_contours(contours, hierarchy):
        correct_contours = []
        all_children = []
        if contours:
            for cnt in contours:
                if cv2.contourArea(cnt) < 200:
                    continue
                if utils.is_circle(cnt, 0.7):
                    all_children.extend(utils.get_children(cnt, contours, hierarchy))
                    correct_contours.append(cnt)
        for cnt in all_children:
            try:
                correct_contours.remove(cnt)
            except ValueError:
                continue
        return correct_contours

    @staticmethod
    def draw_contours(filtered_contours, original):
        if filtered_contours:
            for cnt in filtered_contours:
                (a, b), radius = cv2.minEnclosingCircle(cnt)
                center = int(a), int(b)
                cv2.circle(original, center, int(radius), (0, 255, 0), 5)
