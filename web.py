from threading import Thread

import cv2
from flask import Flask, render_template, Response, request
import time

import utils


class Web:
    """This class handles the web server we use for streaming & control."""

    def __init__(self, main):
        self.main = main
        self.last_frame = None  # Keep last frame for streaming
        self.app = Flask('Web')  # Flask app for web

        # Index html file
        @self.app.route('/')
        def index():  # Returns the HTML template
            if self.main.results.networktables:
                filename = self.main.nt.get_item('match-data', 'Enter file name')
            else:
                filename = time.strftime("%d-%m-%Y-%H-%M-%S")
            return render_template('index.html', initial_filename=filename)

        # Video feed endpoint
        @self.app.route('/stream.mjpg')
        def video_feed():  # Initiate the feed
            return Response(self.stream_frame(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route('/save', methods=['POST'])
        def save():
            """Post route that saves HSV values."""
            self.main.hsv_handler.save_hsv_values()
            return '', 204

        @self.app.route('/update', methods=['POST'])
        def update():
            """Post route to change target."""
            target = request.data.decode('utf-8')
            self.main.change_name(target)
            return '', 204

        @self.app.route('/record', methods=['POST'])
        def record():
            """Start recording."""
            filename = request.data.decode('utf-8')
            if filename:
                self.main.display.start_recording(filename)
            else:
                print('File name not present')
            return '', 204

        @self.app.route('/stopRecording', methods=['POST'])
        def stop_recording():
            """Stop recording."""
            self.main.display.stop_recording()
            return '', 204

    def stream_frame(self):
        """
        This is the generator that encodes and streams the last frame to the stream endpoint.
        :return: JPEG encoded frame
        """
        while True:
            if self.last_frame is None:
                continue
            jpg = cv2.imencode('.jpg', self.last_frame)[1].tostring()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpg + b'\r\n')

    def serve(self):
        """Start the web server."""
        # Print out ip and port for ease of use
        print(f'Web server: http://{utils.get_ip()}:5987')
        # Run flask and bind to all IPs
        self.app.run('0.0.0.0', 5987, threaded=True)

    def start_thread(self):
        """Run web server in a thread - daemon so it lets the program exit."""
        Thread(target=self.serve, daemon=True).start()

    def set_frame(self, frame):
        """
        Save the last frame.

        This method is called from Main.
        """
        self.last_frame = frame
