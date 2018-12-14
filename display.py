import cv2

fourcc = 0
out = 0
record = False

class Display:
    def __init__(self, port=0):
        self.camera = cv2.VideoCapture(port)

    def get_frame(self):
        return self.camera.read()[1]

    @staticmethod
    def show_frame(frame, title='image'):
        cv2.imshow(title, frame)
        if title == 'contour image' and record:
            out.write(frame)
