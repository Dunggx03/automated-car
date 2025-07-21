# stream.py

import cv2
import time
from flask import Flask, Response
from state import state  # dùng latest_frame từ state toàn cục

app = Flask(__name__)

@app.route('/')
def index():
    return '<h3>Pi Camera Stream</h3><img src="/video">'

@app.route('/video')
def video():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
    while True:
        frame = state.get('latest_frame')
        if frame is not None:
            ok, buf = cv2.imencode('.jpg', frame)
            if ok:
                yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' +
                    buf.tobytes() +
                    b'\r\n'
                )
        time.sleep(0.05)
