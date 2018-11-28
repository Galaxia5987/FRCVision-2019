import math
import os
import socket

import cv2
import numpy as np
from termcolor import colored


def aspect_ratio(width, height):
    """
    Calculate aspect ratio.
    :param width:
    :param height:
    :return: Aspect ratio
    """
    return width / height


def circle_area(radius):
    """
    Circle area calculation.
    :param radius:
    :return: Circle area
    """
    return radius ** 2 * math.pi


def circle_ratio(cnt):
    """
    Calculates ratio between a convex hull and a circle area.
    :param cnt:
    :return: Circle ratio
    """
    _, radius = cv2.minEnclosingCircle(cnt)
    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    return hull_area / float(circle_area(radius))


def hsv_mask(frame, hsv):
    """
    Generates HSV mask.
    :param frame:
    :param hsv:
    :return: HSV mask
    """
    hsv_colors = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([hsv['H'][0], hsv['S'][0], hsv['V'][0]])
    higher_hsv = np.array([hsv['H'][1], hsv['S'][1], hsv['V'][1]])
    mask = cv2.inRange(hsv_colors, lower_hsv, higher_hsv)
    return mask


def morphology(mask, kernel):
    """
    Most common morphology use.
    :param mask:
    :param kernel:
    :return: Mask after morphology
    """
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask


def bitwise_mask(frame, mask):
    """
    Generates bitwise and for a frame and mask.
    :param frame:
    :param mask:
    :return: Frame with either black or white
    """
    frame = frame.copy()
    return cv2.bitwise_and(frame, frame, mask=mask)


def calculate_fps(frame, current_time, last_time, avg):
    """
    Calculates current FPS.
    :param frame:
    :param current_time:
    :param last_time:
    :param avg:
    :return: AVG FPS
    """
    avg = (avg + (current_time - last_time)) / 2
    cv2.putText(frame, '{} FPS'.format(int(1 / avg)), (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    return avg


def solidity(cnt) -> float:
    """
    Calculates solidity of a contour.
    :param cnt:
    :return: Solidity ratio
    """
    hull = cv2.convexHull(cnt)
    area = cv2.contourArea(cnt)
    hull_area = cv2.contourArea(hull)
    return float(area) / hull_area


def get_children(contour, contours, hierarchy):
    """
    Returns child contours of a specific contour.
    :param contour:
    :param contours:
    :param hierarchy:
    :return: List of children contours
    """
    hierarchy = hierarchy[0]
    index = contours.index(contour)
    return [child for child, h in zip(contours, hierarchy) if h[3] == index]


def get_ip() -> str:
    """
    Returns local IP that can be used to access the web UI.
    :return: IP address
    """
    return socket.gethostbyname(socket.gethostname())


def is_target(name: str, message: bool = True) -> bool:
    """
    Checks if a target exists or not if not, print a message.
    :param message: Boolean if a message should be printed
    :param name: Name of target
    :return: Boolean if target exists or not
    """
    if not os.path.isfile(f'targets/{name}.py'):
        if message:
            print(colored('Target doesn\'t exist', 'red'))
        return False
    return True
