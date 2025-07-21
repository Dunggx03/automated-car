#config.py
# ★ Camera / inference
FRAME_W, FRAME_H = 480, 480              # resize fed to YOLO
YOLO_MODEL = "yolov8n_ncnn_model"                # or custom .pt

# ★ UART port
UART_PORT     = "/dev/ttyACM0"           # adapt to your setup
UART_BAUDRATE = 115200

# ★ Binary protocol (little‑endian) – Pi → Arduino
P2A_START = 0xAA                         # start byte
P2A_LEN   = 5                            # AA + CMD + SPEED + YAW_L + YAW_H

# ★ Binary protocol – Arduino → Pi
A2P_START = 0xAB                         # start byte
A2P_LEN   = 4                            # AB + DIST_L + DIST_H + YAW_L + YAW_H

# ★ Command byte values (Pi → Arduino)
CMD_STOP   = 0x00
CMD_MOVE   = 0x01
CMD_LEFT   = 0x02
CMD_RIGHT  = 0x03
CMD_AVOID  = 0x04
CMD_DETECTSUCCESS    = 0x05        # yaw to target angle (deg, int16)
CMD_DETECT  = 0x06        # optional: set servo angle
# ACK từ Arduino gửi về Pi sau khi hoàn tất hành động
ACK_NONE            = 0x00
ACK_DETECTSUCCESS   = 0xF1
ACK_AVOID           = 0xF2

DEFAULT_SPEED = 80       # PWM 0‑255
AVOID_THRESHOLD = 40  # cm, distance to start avoidinga
STOP_THRESHOLD = 15   # cm, distance to stop following

