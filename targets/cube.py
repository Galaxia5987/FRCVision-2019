import cv2
import numpy as np
import utils


class Target:
    def __init__(self, name):
        self.name = name
        self.kernel = np.array([[0, 1, 0],
                                [1, 1, 1],
                                [0, 1, 0]], dtype=np.uint8)

    def create_mask(self, frame, hsv):
        mask = utils.hsv_mask(frame, hsv)
        # create a cross kernel
        mask = utils.morphology(mask, self.kernel)
        mask = utils.binary_thresh(mask, 127)
        return mask

    @staticmethod
    def edge_detection(frame, mask):
        edge = utils.bitwise_and(frame, mask)
        edge = utils.edge_detection(edge)
        edge = utils.binary_thresh(edge, 20)
        edge = np.array(edge, dtype=np.uint8)
        return edge

    @staticmethod
    def find_contours(mask, edge):
        mask = utils.bitwise_not(mask, edge)
        img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    @staticmethod
    def filter_contours(contours):
        return contours

    @staticmethod
    def draw_contours(filtered_contours, original):
        for cnt in filtered_contours:
            if len(cnt) > 2 and cv2.contourArea(cnt) > 750 and utils.aspect_ratio(cnt) < 2.5:
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(original, [box], 0, (0, 0, 255), 2)

