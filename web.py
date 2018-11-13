from multiprocessing import Process
from threading import Thread

from gevent.monkey import patch_all; patch_all()

import cv2
from flask import Flask, render_template, Response, request
from gevent.pywsgi import WSGIServer
from gevent.server import _tcp_listener


class Web:
    def __init__(self):
        self.last_frame = None  # Keep last frame for streaming
        self.app = Flask("Web")  # Flask app
        #self.listener = _tcp_listener(('0.0.0.0', 5200))  # Web tcp listener

        @self.app.route('/')
        def index():  # Returns the HTML template
            return render_template('index.html')

        @self.app.route('/stream.mjpg')
        def video_feed():  # Initiate the feed
            return Response(self.stream_frame(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route("/save", methods=['POST'])
        def save():
            print("Save")
            return '', 204

        @self.app.route("/update", methods=['POST'])
        def update():
            print("Update: " + request.data.decode("utf-8"))
            return '', 204

    def stream_frame(self):
        while True:
            if self.last_frame is None:
                continue
            jpg = cv2.imencode('.jpg', self.last_frame)[1].tostring()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpg + b'\r\n')

    def serve(self):
        WSGIServer(('0.0.0.0', 5987), self.app).serve_forever()

    def run_app(self):
        Thread(target=self.serve, daemon=True).start()

    def start_thread(self):
        self.run_app()

    def set_frame(self, frame):
        self.last_frame = frame
