import cv2
import numpy as np

import utils
from targets.target_base import TargetBase


class Target(TargetBase):
    """Hatch panel ye mum."""

    @staticmethod
    def _is_correct(cnt, contours, hierarchy):
        if cv2.contourArea(cnt) < 2_000:
            return False
        return utils.is_circle(cnt, 0.6)

    def filter_contours(self, contours, hierarchy):
        cnts = [cnt for cnt in contours if self._is_correct(cnt, contours, hierarchy)]

        if len(cnts) == 2:
            areas = []
            papa = 0
            for cnt in cnts:
                children = utils.get_children(cnt, contours, hierarchy)
                if children:
                    papa = cnt

                convex_area = cv2.contourArea(cv2.convexHull(cnt))
                areas.append(convex_area)

            if len(areas) == 2:
                if 0.5 < (min(areas)/max(areas)) < 0.7:
                    return papa

        elif len(cnts) == 1:
            area = cv2.contourArea(cnts[0])
            hull_area = cv2.contourArea(cv2.convexHull(cnts[0]))

            if 0.2 < (area/hull_area) < 0.5:
                return cnts



    @staticmethod
    def draw_contours(filtered_contours, original):
        if not filtered_contours:
            return
        for cnt in filtered_contours:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(original,(x,y),(x+w,y+h),(0,255,0),2)
