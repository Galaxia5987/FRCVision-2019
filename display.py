import cv2
import datetime

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640, 480))

class Display:
    def __init__(self, port=0):
        self.camera = cv2.VideoCapture(port)

    def get_frame(self):
        ret, frame = self.camera.read()
        out.write(frame)
        return frame

    @staticmethod
    def show_frame(frame, title='image'):
        cv2.imshow(title, frame)
