#include "config.h"
#include "motor.h"
#include "servo.h"
#include "sensor.h"
#include "uart.h"

MPU6050 mpu(Wire);
float targetYawDeg = -90.0;
float targetYawRad = targetYawDeg * PI / 180.0;
float targetServoAngle = 45;
int current_servo_angle = 90;

uint8_t cmd, speed;
int16_t yawDeg;
bool detect_done = false;
uint8_t ack_to_send = ACK_NONE;

void setup() {
  Serial.begin(115200);
  initMotors();
  initServo(SERVO_PIN);
  setupUltrasonic();
  setupUART();

  Wire.begin();
  if (mpu.begin() != 0) {
    Serial.println("MPU6050 init failed!"); while (1);
  }

  Serial.println("Calibrating MPU...");
  mpu.calcOffsets();
  Serial.println("Done!");
}

void loop() {
  float dist = readDistanceCM();
  sendTelemetry(dist, ack_to_send);
  ack_to_send = ACK_NONE;

  if (!detect_done) {
    sweepServoWithSpeed(0.05);
    yawServoCmd((targetServoAngle - 90.0) * PI / 180.0, true);
    ack_to_send = ACK_DETECTSUCCESS;
    detect_done = true;
    return;
  }

  if (readUARTCommand(cmd, speed, yawDeg)) {
    switch (cmd) {
      case CMD_STOP: stopMotors(); break;
      case CMD_MOVE: moveForward(speed); break;
      case CMD_LEFT: yawServoCmd(yawDeg * PI / 180.0, false); break;
      case CMD_RIGHT: yawServoCmd(yawDeg * PI / 180.0, false); break;
      case CMD_AVOID:
        yawServoCmd(yawDeg * PI / 180.0, false);
        ack_to_send = ACK_AVOID;
        break;
    }
    cmd = 0;
  }

  delay(10);
}
