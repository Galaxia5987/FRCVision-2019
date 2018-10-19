import cv2


class Target:
    def __init__(self, name):
        self.name = name

    def filter_contours(self, contours):
        correct_contours = []

        if contours is not None:
            for cnt in contours:
                if 10 < cv2.contourArea(cnt) < 1000:
                    correct_contours.append(cnt)

        return correct_contours

    def pre_processing(self, frame):
        return frame
