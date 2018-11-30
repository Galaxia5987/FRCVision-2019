import cv2
import numpy as np

import utils
import constants

class Target:
    def __init__(self, name):
        self.name = name
        self.kernel = np.array([[0, 1, 0],
                                [1, 1, 1],
                                [0, 1, 0]], dtype=np.uint8)

    def create_mask(self, frame, hsv):
        mask = utils.hsv_mask(frame, hsv)
        # create a cross kernel
        mask = utils.morphology(mask, self.kernel)
        mask = cv2.threshold(mask, 127, 255, 0)[1]
        return mask

    @staticmethod
    def find_contours(mask):
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def is_circle(self, cnt, minimum):
        ratio = utils.circle_ratio(cnt)
        if minimum <= ratio <= 1:
            return True
        return False

    def find_circles(self, contours):
        circles = []
        for cnt in contours:
            if self.is_circle(cnt, 0.5):
                circles.append(cnt)
        return circles

    def size_filtering(self, contours):
        correct_contours = []
        for cnt in contours:
            if cv2.contourArea(cnt) > 3_000 and self.is_circle(cnt, 0.8):
                correct_contours.append(cnt)
        return correct_contours

    def filter_contours(self, contours):
        if not contours:
            return
        circles = self.find_circles(contours)
        if not circles:
            return
        filtered_circles = self.size_filtering(circles)
        if not filtered_circles:
            return
        final_contours = []
        for circle in circles:
            for filtered_circle in filtered_circles:
                if filtered_circle is circle:
                    continue
                if utils.contour_in_area(filtered_circle, circle):
                    if cv2.contourArea(circle) > 300:
                        _, circle_radius = cv2.minEnclosingCircle(circle)
                        _, filtered_radius = cv2.minEnclosingCircle(filtered_circle)
                        ratio = utils.circle_area(circle_radius) / utils.circle_area(filtered_radius)
                        if ratio >= 0.01:
                            final_contours.append(filtered_circle)
        return final_contours

    @staticmethod
    def draw_contours(filtered_contours, original):
        if not filtered_contours:
            return
        for cnt in filtered_contours:
            # x, y, w, h = cv2.boundingRect(cnt)
            # print(cv2.contourArea(cnt))
            # cv2.putText(original, str(cv2.contourArea(cnt)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 2, cv2.LINE_AA)
            (a, b), radius = cv2.minEnclosingCircle(cnt)
            center = (int(a), int(b))
            cv2.circle(original, center, int(radius), (255, 255, 0), 5)


    
   

