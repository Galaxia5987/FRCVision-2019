import cv2
import numpy as np
import utils


class Target:
    def __init__(self, name):
        self.name = name
        self.kernel_s = np.array([1], dtype=np.uint8)
        self.kernel_m = np.array([[1, 1],
                                  [1, 1]], dtype=np.uint8)
        self.kernel_b = np.array([[0, 1, 0],
                                  [1, 1, 1],
                                  [0, 1, 0]], dtype=np.uint8)

    def create_mask(self, frame, hsv):
        mask = utils.hsv_mask(frame, hsv)
        # create a cross kernel
        mask = utils.morphology(mask, self.kernel_b)
        mask = utils.binary_thresh(mask, 127)
        return mask

    def edge_detection(self, frame, mask):
        edge = utils.bitwise_and(frame, mask)
        edge = utils.canny_edge_detection(edge)
        edge = utils.binary_thresh(edge, 20)
        edge = np.array(edge, dtype=np.uint8)
        edge = utils.open(edge, kernel_e=self.kernel_s, kernel_d=self.kernel_s)
        mask = utils.bitwise_not(mask, edge)
        mask = utils.close(mask, kernel_d=self.kernel_m, kernel_e=self.kernel_m)
        return mask

    def find_contours(self, mask):
        img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    @staticmethod
    def filter_contours(contours):
        for cnt in contours:
            if utils.rectangularity(cnt) > 0.85:
                ratio = utils.aspect_ratio(cnt)




        return contours

    @staticmethod
    def draw_contours(filtered_contours, original):
        for cnt in filtered_contours:
            if len(cnt) > 2 and cv2.contourArea(cnt) > 750 and utils.aspect_ratio(cnt) < 2.5:
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(original, [box], 0, (0, 0, 255), 2)

