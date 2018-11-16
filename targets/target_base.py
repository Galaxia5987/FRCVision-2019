from abc import ABC, abstractmethod

import cv2
import numpy as np

import utils


class TargetBase(ABC):
    """An abstract class representing a base target."""

    def __init__(self):
        """Instantiate a target."""
        self.kernel = np.array([[0, 1, 0],
                                [1, 1, 1],
                                [0, 1, 0]], dtype=np.uint8)

    def create_mask(self, frame, hsv):
        """
        :param frame: the frame to process
        :param hsv: JSON file
        :return: the mask of the target
        """
        mask = utils.hsv_mask(frame, hsv)
        # create a cross kernel
        mask = utils.morphology(mask, self.kernel)
        mask = cv2.threshold(mask, 127, 255, 0)[1]
        return mask

    @staticmethod
    def find_contours(mask) -> list:
        """
        :param mask: mask of the target
        :return: list of contours in the mask
        """
        return cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

    @staticmethod
    @abstractmethod
    def filter_contours(contours: list):
        """
        Filter the contours of the target.
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
