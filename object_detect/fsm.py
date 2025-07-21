# fsm.py
import time
from config import *

def handle_ack(ack, state):
    if ack == ACK_DETECTSUCCESS:
        state.update(dict(
            detect_success=True,
            waiting_ack_succ=False,
            follow_start_time=time.time(),
            allow_steer=False,
            avoiding=False
        ))
        print("ACK_DETECTSUCCESS received → follow starts")
    elif ack == ACK_AVOID:
        state.update(dict(
            awaiting_avoid_ack=False,
            detect_success=False,
            detect_sent=False,
            track_id=None,
            avoiding=False
        ))
        print(" ACK_AVOID received, restarting detection")
