import math
import socket

import cv2
#import netifaces as ni
import numpy as np


def aspect_ratio(cnt):
    x, y, w, h = cv2.boundingRect(cnt)
    return w / h


def circle_area(radius):
    return radius ** 2 * math.pi


def circle_ratio(cnt):
    _, radius = cv2.minEnclosingCircle(cnt)
    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    return hull_area / float(circle_area(radius))


def hsv_mask(frame, hsv):
    hsv_colors = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([hsv['H'][0], hsv['S'][0], hsv['V'][0]])
    higher_hsv = np.array([hsv['H'][1], hsv['S'][1], hsv['V'][1]])
    mask = cv2.inRange(hsv_colors, lower_hsv, higher_hsv)
    return mask


def morphology(mask, kernel):
    mask = open(mask, kernel, kernel)
    mask = close(mask, kernel, kernel)
    return mask


def open(mask, kernel_e, kernel_d, itr=1):
    mask = cv2.erode(mask ,kernel_e, iterations=itr)
    mask = cv2.dilate(mask, kernel_d, iterations=itr)
    return mask


def close(mask, kernel_d, kernel_e, itr=1):
    mask = dilate(mask, kernel_d, itr)
    mask = erode(mask, kernel_e, itr)
    return mask


def dilate(mask, kernel, itr=1):
    return cv2.dilate(mask, kernel, iterations=itr)


def erode(mask, kernel, itr=1):
    return cv2.erode(mask, kernel, iterations=itr)


def bitwise_and(frame, mask):
    frame = frame.copy()
    return cv2.bitwise_and(frame, frame, mask=mask)


def bitwise_not(frame, mask):
    frame = frame.copy()
    return cv2.bitwise_not(frame, frame, mask=mask)


def binary_thresh(frame, thresh):
    return cv2.threshold(frame, thresh, 255, cv2.THRESH_BINARY)[1]


def edge_detection(frame):
    src = cv2.GaussianBlur(frame, (3, 3), 0)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(gray, 100, 225)


def contour_in_area(cnt1, cnt2):
    x1, y1, w1, h1 = cv2.boundingRect(cnt1)
    x2, y2, w2, h2 = cv2.boundingRect(cnt2)
    return x1 <= x2 <= x1 + w1 and y1 <= y2 <= y1 + h1


def calculate_fps(frame, current_time, last_time, avg):
    avg = (avg + (current_time - last_time)) / 2
    cv2.putText(frame, '{} FPS'.format(int(1 / avg)), (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    return avg


def solidity(cnt) -> float:
    hull = cv2.convexHull(cnt)
    area = cv2.contourArea(cnt)
    hull_area = cv2.contourArea(hull)
    return float(area) / hull_area


def get_ip():
    return socket.gethostbyname(socket.gethostname())
