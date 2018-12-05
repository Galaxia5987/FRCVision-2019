import math
import os
import socket

import cv2
import numpy as np
from termcolor import colored


def aspect_ratio(cnt):
    """
    Calculate aspect ratio of given contour.
    :param cnt:
    :return: Aspect ratio
    """
    x, y, w, h = cv2.boundingRect(cnt)
    return w / h


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
    mask = opening_morphology(mask, kernel, kernel)
    mask = closing_morphology(mask, kernel, kernel)
    return mask


def opening_morphology(mask, kernel_e, kernel_d, itr=1):
    """
    Runs opening morphology on given mask.
    :param mask:
    :param kernel_e:
    :param kernel_d:
    :param itr:
    :return:
    """
    mask = cv2.erode(mask, kernel_e, iterations=itr)
    mask = cv2.dilate(mask, kernel_d, iterations=itr)
    return mask


def closing_morphology(mask, kernel_d, kernel_e, itr=1):
    """
    Runs closing morphology on given mask.
    :param mask:
    :param kernel_d:
    :param kernel_e:
    :param itr:
    :return:
    """
    mask = dilate(mask, kernel_d, itr)
    mask = erode(mask, kernel_e, itr)
    return mask


def dilate(mask, kernel, itr=1):
    """
    Run dilation on given mask.
    :param mask:
    :param kernel:
    :param itr:
    :return:
    """
    return cv2.dilate(mask, kernel, iterations=itr)


def erode(mask, kernel, itr=1):
    """
    Run erotion on given mask.
    :param mask:
    :param kernel:
    :param itr:
    :return:
    """
    return cv2.erode(mask, kernel, iterations=itr)


def bitwise_and(frame, mask):
    """
    Generates bitwise and for a frame and mask.
    :param frame:
    :param mask:
    :return: Frame with either black or white
    """
    frame = frame.copy()
    return cv2.bitwise_and(frame, frame, mask=mask)


def bitwise_not(frame, mask):
    """
    Generates bitwise not for a frame and mask.
    :param frame:
    :param mask:
    :return:
    """
    frame = frame.copy()
    return cv2.bitwise_not(frame, frame, mask=mask)


def bitwise_xor(frame, mask):
    """
    Generates bitwise xor for a frame and mask.
    :param frame:
    :param mask:
    :return:
    """
    frame = frame.copy()
    return cv2.bitwise_xor(frame, frame, mask=mask)


def binary_thresh(frame, thresh):
    """
    Creates binary threshold from given value to 255.
    :param frame:
    :param thresh:
    :return:
    """
    return cv2.threshold(frame, thresh, 255, cv2.THRESH_BINARY)[1]


def canny_edge_detection(frame):
    """
    Runs canny edge detection on a frame.
    :param frame:
    :return:
    """
    src = cv2.GaussianBlur(frame, (3, 3), 0)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(gray, 100, 225)


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
    index = numpy_index(contour, contours)
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


def distance(focal, object_width, object_width_pixels):
    """
    Calculates distance, works for most objects.
    :param focal:
    :param object_width:
    :param object_width_pixels:
    :return: distance in meters
    """
    return (focal * object_width) / object_width_pixels


def array8(arr):
    """
    Turns array into a uint8 array.
    :return:
    """
    return np.array(arr, dtype=np.uint8)


def is_circle(cnt, minimum):
    """
    Checks the circle ratio and returns true if it meets the minimum.
    :param cnt:
    :param minimum:
    :return:
    """
    ratio = circle_ratio(cnt)
    return minimum <= ratio <= 1


def is_triangle(cnt):
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.07 * peri, True)
    return len(approx) == 3


def numpy_index(element, l):
    return [np.array_equal(element, x) for x in l].index(True)


def angle(focal, xtarget, frame):
    """
    Calculates angle, works for most targets.
    :param focal: Focal length of desired camera
    :param xtarget: a of min enclosing circle
    :param frame: video frame
    :return: angle in degrees
    """
    xframe = frame.shape[1] / 2
    return math.atan2((xtarget - xframe), focal) * (180 / math.pi)
