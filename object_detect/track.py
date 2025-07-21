# track.py
import time, cv2
from utils import centered, delta_to_yaw
from config import *
from control import send_if_changed

def process_loop(cam, yolo, tracker, uart, state):
    while True:
        dist, ack = uart.read_data()
        time.sleep(0.02)
        if dist is None: dist = 999.0

        # Xử lý ACK
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
            print("ACK_AVOID received, restarting detection")

        # Camera + YOLO
        frame = cam.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        res = yolo.predict(frame_bgr, conf=0.3, iou=0.5, imgsz=640, verbose=False)[0]

        # Xử lý bounding boxes
        boxes = res.boxes.xyxy.cpu().numpy()
        scores= res.boxes.conf.cpu().numpy()
        clses = res.boxes.cls.cpu().numpy().astype(int)
        detections, first_person = [], None

        for b,s,c in zip(boxes, scores, clses):
            x1,y1,x2,y2 = map(int,b)
            if c == 0 and first_person is None:
                detections.append(([x1,y1,x2,y2], s, "person"))
                first_person = [x1,y1,x2,y2]
            cv2.rectangle(frame_bgr, (x1,y1), (x2,y2), (0,255,0) if c==0 else (128,128,128), 2)

        # Tracking
        tracks = tracker.update_tracks(detections, frame=frame_bgr)
        tracked_box = None
        for t in tracks:
            if not t.is_confirmed(): continue
            if state['track_id'] is None:
                state['track_id'] = t.track_id
            if t.track_id != state['track_id']: continue
            tracked_box = list(map(int, t.to_ltrb()))
            break

        # Logic điều khiển (tương tự phần trong process_loop của bạn)
        # → bạn có thể copy và điều chỉnh dùng dict `state[...]`

        # Cập nhật khung hình cuối
        state['latest_frame'] = frame_bgr
        time.sleep(0.03)
