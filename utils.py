import json
import math
import os
import socket

import cv2
import numpy as np


# Default value for value files
def default_value(name, folder):
    if folder == 'hsv':
        return {"H": (0, 255), "S": (0, 255), "V": (0, 255)}
    elif folder == 'values':
        return {name + "_name": name}
    else:
        print("[Default value] This should happen")


def get_filename(name, folder):
    return "{}/{}.json".format(folder, name)


def save_file(name, folder, data):
    with open(get_filename(name, folder), "w") as f:
        json.dump(data, f)


def load_file(name, folder):
    if not os.path.isfile(get_filename(name, folder)):
        save_file(name, folder, default_value(name, folder))
    with open(get_filename(name, folder), "r") as f:
        return json.load(f)


def aspect_ratio(width, height):
    return width / height


def circle_area(radius):
    return radius ** 2 * math.pi


def circle_ratio(cnt):
    _, radius = cv2.minEnclosingCircle(cnt)
    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    return hull_area / float(circle_area(radius))


def hsv_mask(frame, hsv):
    hsv_colors = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([hsv["H"][0], hsv["S"][0], hsv["V"][0]])
    higher_hsv = np.array([hsv["H"][1], hsv["S"][1], hsv["V"][1]])
    mask = cv2.inRange(hsv_colors, lower_hsv, higher_hsv)
    return mask


def morphology(mask, kernel):
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask


def bitwise_mask(frame, mask):
    frame = frame.copy()
    return cv2.bitwise_and(frame, frame, mask=mask)


def contour_in_area(cnt1, cnt2):
    x1, y1, w1, h1 = cv2.boundingRect(cnt1)
    x2, y2, w2, h2 = cv2.boundingRect(cnt2)
    return x1 <= x2 <= x1 + w1 and y1 <= y2 <= y1 + h1


def calculate_fps(frame, current_time, last_time, avg):
    avg = (avg + (current_time - last_time)) / 2
    cv2.putText(frame, "{} FPS".format(int(1 / avg)), (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    return avg


def get_ip():
    return socket.gethostbyname(socket.gethostname())
