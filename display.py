import cv2


class Display:
    def __init__(self, port=0):
        self.camera = cv2.VideoCapture(port)
        self.camera.set(11, 7)
        self.camera.set(15, -6)
        self.camera.set(5, 17)
        print('Contrast: '+str(self.camera.get(11))+'\tExposure: '+str(self.camera.get(15))+'\tFPS: '+str(self.camera.get(5)))


    def get_frame(self):
        return self.camera.read()[1]

    @staticmethod
    def show_frame(frame, title='image'):
        cv2.imshow(title, frame)
