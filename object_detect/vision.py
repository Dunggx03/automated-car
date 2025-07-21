# vision.py
import cv2

def detect_and_track(cam, yolo, tracker, coco, state):
    frame = cam.capture_array()
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    res = yolo.predict(frame_bgr, conf=0.3, iou=0.5, imgsz=640, verbose=False)[0]

    boxes = res.boxes.xyxy.cpu().numpy()
    scores= res.boxes.conf.cpu().numpy()
    clses = res.boxes.cls.cpu().numpy().astype(int)

    detections, first_person = [], None
    for b, s, c in zip(boxes, scores, clses):
        x1, y1, x2, y2 = map(int, b)
        if c == 0 and first_person is None:
            detections.append(([x1, y1, x2, y2], s, "person"))
            first_person = [x1, y1, x2, y2]
        clr = (255, 0, 0) if c == 0 else (128, 128, 128)
        cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), clr, 2)
        cv2.putText(frame_bgr, f"{coco[c]} {s:.2f}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, clr, 1)

    tracks = tracker.update_tracks(detections, frame=frame_bgr)
    tracked_box = None
    for t in tracks:
        if not t.is_confirmed():
            continue
        if state['track_id'] is None:
            state['track_id'] = t.track_id
        if t.track_id != state['track_id']:
            continue
        tracked_box = list(map(int, t.to_ltrb()))
        break

    state['latest_frame'] = frame_bgr
    return tracked_box
