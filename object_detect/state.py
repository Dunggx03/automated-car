# state.py

state = dict(
    detect_sent=False,
    waiting_ack_succ=False,
    detect_success=False,
    waiting_ack_avoid=False,
    awaiting_avoid_ack=False,
    avoiding=False,
    track_id=None,
    latest_frame=None,
    last_cmd=None,
    last_speed=None,
    last_yaw=None,
    last_direction=None,
    last_steer_time=0,
    follow_start_time=0,
    allow_steer=False,
    avoid_sent_time=0
)
