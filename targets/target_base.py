from abc import ABC, abstractmethod
from typing import Tuple, Optional

import cv2
import numpy as np

import utils


class TargetBase(ABC):
    """An abstract class representing a base target."""

    def __init__(self, main):
        self.kernel_small = np.array([1], dtype=np.uint8)
        self.kernel_medium = np.array([[1, 1],
                                       [1, 1]], dtype=np.uint8)
        self.kernel_big = np.array([[0, 1, 0],
                                    [1, 1, 1],
                                    [0, 1, 0]], dtype=np.uint8)
        self.exposure = -6
        self.main = main

    def create_mask(self, frame, hsv):
        """
        :param frame: the frame to process
        :param hsv: JSON file
        :return: the mask of the target
        """
        mask = utils.hsv_mask(frame, hsv)
        # create a cross kernel
        mask = utils.morphology(mask, self.kernel_big)
        mask = cv2.threshold(mask, 127, 255, 0)[1]
        return mask

    @staticmethod
    def find_contours(mask) -> tuple:
        """
        :param mask: mask of the target
        :return: list of contours in the mask
        """
        obj = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Hacky fix the difference opencv 4 and 3 until we can update everywhere
        if len(obj) == 2:
            return obj[0], obj[1]
        else:
            return obj[1], obj[2]

    @staticmethod
    def measurements(frame, cnt) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """
        Return the angle and distance from a single target.
        :param frame: The frame, used for angle measurement
        :param cnt: The contour of the target
        """
        return None, None, None

    @staticmethod
    @abstractmethod
    def filter_contours(contours: list, hierarchy):
        """
        Filter the contours of the target.
        :param hierarchy: contour hierarchy data
        :param contours: list of contours
        """
        pass

    @staticmethod
    @abstractmethod
    def draw_contours(filtered_contours: list, contour_image):
        """
        Draw the contours on the frame.
        :param filtered_contours: filtered contours of the mask
        :param contour_image: frame the contours were found it
        """
        pass
