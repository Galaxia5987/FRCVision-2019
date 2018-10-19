import cv2
import numpy as np

def aspect_ratio(cnt):
    rect = cv2.minAreaRect(cnt)
    width = rect[1][0]
    height = rect[1][1]
    return width / height


def mask(frame, hsv):
    hsv_colors = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([hsv["H"][0], hsv["S"][0], hsv["V"][0]])
    higher_hsv = np.array([hsv["H"][1], hsv["S"][1], hsv["V"][1]])
    mask = cv2.inRange(hsv_colors, lower_hsv, higher_hsv)
    return mask
