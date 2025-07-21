# utils.py
from config import FRAME_W

def centered(box):
    x1, _, x2, _ = box
    return abs(((x1 + x2) // 2) - FRAME_W // 2) < 30

def delta_to_yaw(delta):
    max_yaw = 30
    norm = max(min(delta / (FRAME_W / 2), 1), -1)
    return int(norm * max_yaw)
