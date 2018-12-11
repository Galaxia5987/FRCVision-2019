import cv2

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640, 480))

class Display:
    def __init__(self, port=0):
        self.camera = cv2.VideoCapture(port)

    def get_frame(self):
        return self.camera.read()[1]

    @staticmethod
    def show_frame(frame, title='image'):
        cv2.imshow(title, frame)
        if title == 'contour image':
            out.write(frame)
