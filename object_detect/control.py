# control.py
import time
from config import *
from utils import centered, delta_to_yaw

def send_if_changed(uart, cmd, speed, yaw, state):
    should_send = (
        state['last_cmd'] is None or
        state['last_speed'] is None or
        state['last_yaw'] is None or
        abs(state['last_yaw'] - yaw) > 5 or
        state['last_cmd'] != cmd or
        state['last_speed'] != speed
    )
    if should_send:
        uart.send_cmd(cmd, speed, yaw)
        state['last_cmd'] = cmd
        state['last_speed'] = speed
        state['last_yaw'] = yaw
    return should_send

def control_follow(uart, state, tracked_box, dist):
    now = time.time()
    if not state['allow_steer'] and now - state['follow_start_time'] < 3.0:
        send_if_changed(uart, CMD_MOVE, DEFAULT_SPEED, 0, state)
        print("FOLLOW: straight for 3s")
        state['last_direction'] = 'forward'
        return

    state['allow_steer'] = True

    if dist < AVOID_THRESHOLD and not state['avoiding']:
        uart.send_cmd(CMD_AVOID, 60, 30)
        state['avoiding'] = True
        state['awaiting_avoid_ack'] = True
        state['avoid_sent_time'] = time.time()
        print(" AVOID: CMD_AVOID sent")
        return

    if state['avoiding']:
        print("⏳ Waiting avoid to complete...")
        return

    # Control hướng
    x1, y1, x2, y2 = tracked_box
    cx = (x1 + x2) // 2
    delta = cx - FRAME_W // 2

    if abs(delta) < 30:
        if state['last_direction'] != 'forward':
            send_if_changed(uart, CMD_MOVE, DEFAULT_SPEED, 0, state)
            print("🚶 FOLLOW: forward")
            state['last_direction'] = 'forward'
    elif delta > 0:
        if time.time() - state['last_steer_time'] > 0.5:
            yaw = delta_to_yaw(delta)
            send_if_changed(uart, CMD_RIGHT, DEFAULT_SPEED, yaw, state)
            print(f" FOLLOW: right {yaw}")
            state['last_steer_time'] = time.time()
            state['last_direction'] = 'right'
    else:
        if time.time() - state['last_steer_time'] > 0.5:
            yaw = delta_to_yaw(delta)
            send_if_changed(uart, CMD_LEFT, DEFAULT_SPEED, yaw, state)
            print(f"FOLLOW: left {yaw}")
            state['last_steer_time'] = time.time()
            state['last_direction'] = 'left'
