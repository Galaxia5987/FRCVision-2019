import math
import os
import socket
from typing import Union, List

import constants

import cv2
import numpy as np
from termcolor import colored


# A list of the real measurements of the cube in meters.
power_cube = constants.GAME_PIECE_SIZES['power_cube']


def index0(x):
    # An index function for sorting based on the first variable.
    return x[0]


def index00(x):
    # An index function for sorting based on the first variable of the first variable.
    return x[0][0]


def index1(x):
    # An index function for sorting based on the second variable.
    return x[1]


def index01(x):
    # An index function for sorting based on the second variable of the first variable.
    return x[0][1]


def aspect_ratio(cnt) -> float:
    """
    Calculate aspect ratio of given contour.
    :param cnt: A contour
    :return: Aspect ratio
    """
    x, y, w, h = cv2.boundingRect(cnt)
    return w / h


def rotated_aspect_ratio(cnt) -> float:
    """
    Calculate aspect ratio of given contour, based on a rotated rectangle instead of an upright one.
    :param cnt: A contour
    :return: Width / Height
    """
    return width(cnt)[0] / height(cnt)[0]


def reversed_rotated_aspect_ratio(cnt) -> float:
    """
    Calculate aspect ratio of given contour, based on a rotated rectangle instead of an upright one.
    :param cnt: A contour
    :return: Height / Width
    """
    return height(cnt)[0] / width(cnt)[0]


def height(cnt) -> (float, tuple, tuple):
    """
    Find the height of the box bounding the contour.
    :param cnt: A contour
    :return: Min area rectangle height
    """
    points = []
    for p in box(cnt):
        points.append(p)

    points.sort(key=index0)

    x1, y1 = points[0]
    x2, y2 = points[1]

    return math.hypot(abs(x1 - x2), abs(y1 - y2)), (x1, y1), (x2, y2)


def width(cnt) -> (float, tuple, tuple):
    """
    Find the weight of the box bounding the contour.
    :param cnt: A contour
    :return: Min area rectangle weight
    """
    points = []
    for p in box(cnt):
        points.append(p)

    points.sort(key=index1)

    x1, y1 = points[0]
    x2, y2 = points[1]

    return math.hypot(abs(x1 - x2), abs(y1 - y2)), (x1, y1), (x2, y2)


def box(cnt) -> np.array:
    """
    Return a list of the points of the minimum area rectangle bounding the contour.
    :param cnt: A contour
    :return: List of 4 points in an [x, y] format
    """
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    return np.int0(box)


def circle_area(radius: Union[float, int]) -> float:
    """
    Circle area calculation.
    :param radius:
    :return: Circle area
    """
    return radius ** 2 * math.pi


def circle_ratio(cnt) -> float:
    """
    Calculate ratio between a convex hull and a circle area.
    :param cnt: A contour
    :return: Circle ratio
    """
    _, radius = cv2.minEnclosingCircle(cnt)
    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    return hull_area / float(circle_area(radius))


def center(cnt) -> (int, int):
    """
    Find the center point of the contour.
    :param cnt: A contour
    :return: The center of the minimum enclosing circle
    """
    (x, y), radius = cv2.minEnclosingCircle(cnt)
    return int(x), int(y)


def hsv_mask(frame: np.array, hsv: np.array) -> np.array:
    """
    Generate HSV mask.
    :param frame:
    :param hsv:
    :return: HSV mask
    """
    hsv_colors = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([hsv['H'][0], hsv['S'][0], hsv['V'][0]])
    higher_hsv = np.array([hsv['H'][1], hsv['S'][1], hsv['V'][1]])
    mask = cv2.inRange(hsv_colors, lower_hsv, higher_hsv)
    return mask


def morphology(mask: np.array, kernel: np.array) -> np.array:
    """
    Most common morphology use.
    :param mask:
    :param kernel:
    :return: Mask after morphology
    """
    mask = opening_morphology(mask, kernel, kernel)
    mask = closing_morphology(mask, kernel, kernel)
    return mask


def opening_morphology(mask: np.array, kernel_e: np.array, kernel_d: np.array, itr=1) -> np.array:
    """
    Run opening morphology on given mask.
    :param mask:
    :param kernel_e: Kernel for eroding
    :param kernel_d: Kernel for dilating
    :param itr: Number of iterations
    :return:
    """
    mask = cv2.erode(mask, kernel_e, iterations=itr)
    mask = cv2.dilate(mask, kernel_d, iterations=itr)
    return mask


def closing_morphology(mask: np.array, kernel_d: np.array, kernel_e: np.array, itr=1) -> np.array:
    """
    Runs closing morphology on given mask.
    :param mask:
    :param kernel_e: Kernel for eroding
    :param kernel_d: Kernel for dilating
    :param itr: Number of iterations
    :return:
    """
    mask = dilate(mask, kernel_d, itr)
    mask = erode(mask, kernel_e, itr)
    return mask


def dilate(mask: np.array, kernel: np.array, itr=1):
    """
    Run dilation on given mask.
    :param mask:
    :param kernel:
    :param itr: Number of iterations
    :return:
    """
    return cv2.dilate(mask, kernel, iterations=itr)


def erode(mask: np.array, kernel: np.array, itr=1):
    """
    Run erotion on given mask.
    :param mask:
    :param kernel:
    :param itr: Number of iterations
    :return:
    """
    return cv2.erode(mask, kernel, iterations=itr)


def bitwise_and(frame: np.array, mask: np.array):
    """
    Generates bitwise and for a frame and mask.
    :param frame:
    :param mask:
    :return: Frame with either black or white
    """
    frame = frame.copy()
    return cv2.bitwise_and(frame, frame, mask=mask)


def bitwise_not(frame: np.array, mask: np.array):
    """
    Generates bitwise not for a frame and mask.
    :param frame:
    :param mask:
    :return:
    """
    frame = frame.copy()
    return cv2.bitwise_not(frame, frame, mask=mask)


def bitwise_xor(frame: np.array, mask: np.array):
    """
    Generates bitwise xor for a frame and mask.
    :param frame:
    :param mask:
    :return:
    """
    frame = frame.copy()
    return cv2.bitwise_xor(frame, frame, mask=mask)


def binary_thresh(frame: np.array, thresh: int):
    """
    Creates binary threshold from given value to 255.
    :param frame:
    :param thresh: The lower limit of he binary threshold
    :return:
    """
    return cv2.threshold(frame, thresh, 255, cv2.THRESH_BINARY)[1]


def canny_edge_detection(frame: np.array, min_val=100, max_val=255):
    """
    Runs canny edge detection on a frame.
    :param frame:
    :param min_val: The minimum value above which edges will be ignores
    :param max_val: The maximum value below which edges will be ignored
    :return:
    """
    src = cv2.GaussianBlur(frame, (3, 3), 0)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(gray, min_val, max_val)


def calculate_fps(frame: np.array, current_time: float, last_time: float, avg: float) -> float:
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
    Calculate distance from given object.
    :param focal:
    :param object_width:
    :param object_width_pixels:
    :return: distance in meters
    """
    return (focal * object_width) / object_width_pixels


def array8(arr) -> np.array:
    """
    Turn array into a uint8 array.
    :return: A uint8 numpy array
    """
    return np.array(arr, dtype=np.uint8)


def approx_hull(cnt):
    """
    Lower the amount of points in a contour
    :param cnt:
    :return: A contours with less points
    """
    hull = cv2.convexHull(cnt)
    epsilon = 0.015 * cv2.arcLength(hull, True)
    return cv2.approxPolyDP(hull, epsilon, True)


def points(cnt) -> list:
    """
    Create a list of the approximated points in an [x, y] format
    :param cnt:
    :return: Approximated points
    """
    hullpoints = list(cv2.convexHull(approx_hull(cnt), returnPoints=True))
    hullpoints.sort(key=index00)

    points = []

    for p in hullpoints:
        new_p = (p[0][0], p[0][1])
        points.append(new_p)

    return points
  
  
def is_circle(cnt, minimum):
    """
    Checks the circle ratio and returns true if it meets the minimum.
    :param cnt:
    :param minimum:
    :return:
    """
    ratio = circle_ratio(cnt)
    return minimum <= ratio <= 1


def approx_vertices(cnt, ratio=0.07):
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, ratio * peri, True)
    return len(approx)


def is_triangle(cnt, ratio=0.07):
    """
    Returns if contour is approximately a triangle.
    :param ratio: Approx ratio
    :param cnt:
    :return:
    """
    return approx_vertices(cnt, ratio) == 3


def numpy_index(element, arrays: list):
    """
    Gets index of numpy array in a list.
    :param element:
    :param arrays:
    :return:
    """
    return [np.array_equal(element, x) for x in arrays].index(True)


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


def np_array_in_list(np_array: np.array, list_arrays: List[np.array]) -> bool:
    """
    Return whether a NumPy array is in a list of NumPy arrays.
    :param np_array: array to check
    :param list_arrays: list of arrays to check
    :return: whether a NumPy array is in a list of NumPy arrays
    """
    return next((True for elem in list_arrays if elem is np_array), False)
