# detect.py
import time
import cv2
from picamera2 import Picamera2
from ultralytics import YOLO
from config import *

def init_camera():
    cam = Picamera2()
    cam.configure(cam.create_video_configuration(main={"size": (FRAME_W, FRAME_H)}))
    cam.start()
    time.sleep(1)
    return cam

def init_yolo():
    model = YOLO(YOLO_MODEL, task="detect")
    return model, model.names
