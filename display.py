import cv2


class Display:
    def __init__(self, port=0):
        self.camera = cv2.VideoCapture(port)

    def get_frame(self):
        image = self.camera.read()[1]
        return image

    def show_frame(self, frame, title='image'):
        cv2.imshow(title, frame)
