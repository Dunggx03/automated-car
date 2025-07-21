# process.py
import time
from config import *
from fsm import handle_ack
from vision import detect_and_track
from control import control_follow
from utils import centered
from state import state

def process_loop(cam, yolo, tracker, uart, coco):
    while True:
        dist, ack = uart.read_data()
        time.sleep(0.02)
        if dist is None:
            dist = 999.0

        handle_ack(ack, state)
        tracked_box = detect_and_track(cam, yolo, tracker, coco, state)

        if state['track_id'] is None:
            if not state['detect_sent']:
                uart.send_cmd(CMD_DETECT)
                state['detect_sent'] = True
                print("🔄 CMD_DETECT sent")
            time.sleep(0.03)
            continue

        if tracked_box is None:
            uart.send_cmd(CMD_STOP)
            print(" Lost track, STOP and reset")
            state.update(dict(
                detect_sent=False,
                detect_success=False,
                waiting_ack_succ=False,
                avoiding=False,
                track_id=None
            ))
            time.sleep(0.03)
            continue

        if not state['detect_success'] and not state['waiting_ack_succ']:
            if dist > STOP_THRESHOLD and centered(tracked_box):
                uart.send_cmd(CMD_DETECTSUCCESS)
                state['waiting_ack_succ'] = True
                print("CMD_DETECTSUCCESS sent")
        elif state['detect_success']:
            control_follow(uart, state, tracked_box, dist)

        time.sleep(0.03)
