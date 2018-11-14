from threading import Thread

import cv2
from flask import Flask, render_template, Response, request

import utils


class Web:
    def __init__(self, main):
        self.main = main
        self.last_frame = None  # Keep last frame for streaming
        self.app = Flask("Web")  # Flask app

        @self.app.route('/')
        def index():  # Returns the HTML template
            return render_template('index.html')

        @self.app.route('/stream.mjpg')
        def video_feed():  # Initiate the feed
            return Response(self.stream_frame(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route("/save", methods=['POST'])
        def save():
            self.main.trackbars.save_to_file()
            return '', 204

        @self.app.route("/update", methods=['POST'])
        def update():
            target = request.data.decode("utf-8")
            self.main.change_name(target)
            return '', 204

    def stream_frame(self):
        while True:
            if self.last_frame is None:
                continue
            jpg = cv2.imencode('.jpg', self.last_frame)[1].tostring()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpg + b'\r\n')

    def serve(self):
        # Print out ip and port for ease of use
        print("Web server: http://{}:{}".format(utils.get_ip(), 5987))
        self.app.run('0.0.0.0', 5987, threaded=True)

    def start_thread(self):
        Thread(target=self.serve, daemon=True).start()

    def set_frame(self, frame):
        self.last_frame = frame
