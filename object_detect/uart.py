import serial, struct, time, collections
from config import *

class UART:
    """Bi‑directional binary UART (Pi ↔ Arduino)."""

    def __init__(self, port: str = UART_PORT, baud: int = UART_BAUDRATE):
        self.ser  = serial.Serial(port, baud, timeout=0.02)
        time.sleep(2)
        self._buf = collections.deque(maxlen=64)

    # ───── Pi → Arduino ─────
    def send_cmd(self, cmd: int, speed: int = 0, yaw_deg: int = 0):
        yaw16 = int(yaw_deg) & 0xFFFF
        pkt = struct.pack("<BBBBB",
                          P2A_START,
                          cmd & 0xFF,
                          speed & 0xFF,
                          yaw16 & 0xFF,
                          yaw16 >> 8)
        self.ser.write(pkt)

    # ───── Arduino → Pi ─────
    def read_data(self):
        """
        Try reading one telemetry frame.
        Return (distance_cm: float, ack_code: int) or (None, None)
        """
        self._buf.extend(self.ser.read(self.ser.in_waiting or 1))

        while len(self._buf) >= A2P_LEN:
            if self._buf[0] != A2P_START:
                self._buf.popleft()
                continue
            if len(self._buf) < A2P_LEN:
                break
            raw = bytes(self._buf.popleft() for _ in range(A2P_LEN))
            _, dL, dH, ack = struct.unpack("<BBBB", raw)
            dist = ((dH << 8) | dL) / 10.0  # mm / 10 → cm
            return dist, ack
        return None, None

    def close(self):
        self.ser.close()
