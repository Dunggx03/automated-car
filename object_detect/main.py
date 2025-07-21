# main.py
import threading
from uart import UART
from detect import init_camera, init_yolo
from deep_sort_realtime.deepsort_tracker import DeepSort
from process import process_loop
from stream import app
from state import state

if __name__ == "__main__":
    cam = init_camera()
    yolo, coco = init_yolo()
    tracker = DeepSort(max_age=30, n_init=3, nms_max_overlap=1.0)
    uart = UART()

    try:
        threading.Thread(target=process_loop, args=(cam, yolo, tracker, uart, coco), daemon=True).start()
        app.run(host="0.0.0.0", port=5000, threaded=True)
    finally:
        cam.stop()
        uart.close()
