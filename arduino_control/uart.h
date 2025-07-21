#ifndef UART_H
#define UART_H

#include <Arduino.h>

// ───────── Frame constants ─────────
#define P2A_START  0xAA   // Pi → Arduino: 5 bytes
#define A2P_START  0xAB   // Arduino → Pi: 4 bytes

#define P2A_LEN    5
#define A2P_LEN    4

// ───────── Command codes (from Pi) ─────────
#define CMD_STOP           0x00
#define CMD_MOVE           0x01
#define CMD_LEFT           0x02
#define CMD_RIGHT          0x03
#define CMD_AVOID          0x04
#define CMD_DETECT         0x05
#define CMD_DETECTSUCCESS  0x06

// ───────── ACK codes (from Arduino) ─────────
#define ACK_NONE           0x00
#define ACK_DETECTSUCCESS  0xF1
#define ACK_AVOID          0xF2

// ───────── UART parsing state ─────────
struct PiCommand {
  uint8_t cmd;
  uint8_t speed;
  int16_t yaw;
  bool    valid;

  PiCommand() : cmd(0), speed(0), yaw(0), valid(false) {}
};

// ───────── UART send + receive logic ─────────
class UARTHandler {
public:
  PiCommand currentCmd;
  uint8_t rx_buf[P2A_LEN];
  uint8_t rx_index = 0;

  UARTHandler() {}

  // Call inside loop()
  void readPiCommand() {
    while (Serial.available()) {
      uint8_t byte = Serial.read();

      // sync to start byte
      if (rx_index == 0 && byte != P2A_START) continue;

      rx_buf[rx_index++] = byte;

      if (rx_index == P2A_LEN) {
        currentCmd.cmd   = rx_buf[1];
        currentCmd.speed = rx_buf[2];
        currentCmd.yaw   = (rx_buf[4] << 8) | rx_buf[3];
        currentCmd.valid = true;
        rx_index = 0;
        return;
      }
    }
  }

  void resetCmd() {
    currentCmd.valid = false;
  }

  // distance: mm, ack: one of ACK_*
  void sendTelemetry(uint16_t distance_mm, uint8_t ack_code) {
    uint8_t pkt[A2P_LEN];
    pkt[0] = A2P_START;
    pkt[1] = distance_mm & 0xFF;
    pkt[2] = distance_mm >> 8;
    pkt[3] = ack_code;
    Serial.write(pkt, A2P_LEN);
  }
};

#endif
