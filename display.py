import cv2
from flask import Flask, render_template, Response
from gevent.pywsgi import WSGIServer


class Display:
    def __init__(self, port=0):
        self.camera = cv2.VideoCapture(port)
        self.last_frame = self.get_frame()

        self.app = Flask(__name__)  # the app used for streaming

        @self.app.route('/')
        def index():  # Returns the HTML template (lower case 't')
            return render_template('index.html')

        @self.app.route('/mjpg/video.mjpg')
        def video_feed():  # Initiate the feed
            return Response(self.stream_frame(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

    def get_frame(self):
        image = self.camera.read()[1]
        return image.copy()

    def set_frame(self, frame):
        self.last_frame = frame

    @staticmethod
    def show_frame(frame, title='image'):
        cv2.imshow(title, frame)

    def stream_frame(self):
        while True:
            jpg = cv2.imencode('.jpg', self.last_frame)[1].tostring()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpg + b'\r\n')

    def run_app(self):
        WSGIServer(('0.0.0.0', 5987), self.app).serve_forever()
