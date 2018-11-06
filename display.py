import cv2
import netifaces as ni
from flask import Flask, render_template, Response


class Display:
    def __init__(self, port=0):
        self.camera = cv2.VideoCapture(port)

        self.ip = None
        while self.ip is None:
            for interface in ni.interfaces():
                try:
                    addrs = ni.ifaddresses(interface)[ni.AF_INET]  # IPv4 addresses for current interface
                    # print(addrs)
                    self.ip = addrs[0]['addr']  # The first IP address (probably the local one)
                    if self.ip is not '127.0.0.1':
                        break
                except:
                    pass

        print("IP: " + self.ip)

        self.app = Flask(__name__)  # the app used for streaming

        @self.app.route('/')
        def index():  # Returns the HTML template (lower case 't')
            return render_template('index.html')

        @self.app.route('/mjpg/video.mjpg')
        def video_feed():  # Initiate the feed
            return Response(self.gen_frame(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

    def get_frame(self):
        image = self.camera.read()[1]
        return image.copy()

    @staticmethod
    def show_frame(frame, title='image'):
        cv2.imshow(title, frame)

    def gen_frame(self):
        jpg = cv2.imencode('.jpg', self.get_frame)[1].tostring()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpg + b'\r\n')

    def stream(self):
        self.app.run(host=self.ip, port=80, debug=False)
