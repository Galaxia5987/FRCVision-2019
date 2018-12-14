import os

import cv2


class Display:
    def __init__(self, port=0):
        self.codec = cv2.VideoWriter_fourcc(*'XVID')
        self.record = False
        self.out = None
        self.camera = cv2.VideoCapture(port)

    def get_frame(self):
        return self.camera.read()[1]

    def release(self):
        if self.out:
            self.out.release()
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()

    def start_recording(self, title):
        if not os.path.isdir("recordings"):
            os.makedirs("recordings")
        self.record = True
        self.out = cv2.VideoWriter(f'recordings/{title}.avi', self.codec, 30.0, (640, 480))

    def stop_recording(self):
        if self.out:
            self.out.release()

    def show_frame(self, frame, title='image'):
        cv2.imshow(title, frame)
        if title == 'contour image' and self.record and self.out:
            self.out.write(frame)
