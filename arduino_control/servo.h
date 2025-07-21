#ifndef SERVO_H
#define SERVO_H

#include "defines.h"

/* ----- Biến trạng thái ----- */
float target_servo_yaw = TARGET_SERVO_ANGLE;
float current_servo_angle = CURRENT_SERVO_ANGLE;

/* ----- LOW‑LEVEL PWM ----- */
inline void setServoPulse(int pin, int pulseWidth) {
  digitalWrite(pin, HIGH);
  delayMicroseconds(pulseWidth);
  digitalWrite(pin, LOW);
  delayMicroseconds(PULSE_PERIOD - pulseWidth);
}

/* ----- API ----- */
inline void setServoAngle(float angleDeg) {
  angleDeg = constrain(angleDeg, SERVO_MIN, SERVO_MAX);
  int pw = map(angleDeg, 0, 180, PULSE_MIN, PULSE_MAX);
  setServoPulse(SERVO_PIN, pw);
  current_servo_angle = angleDeg;
}
inline void initServo() {
  pinMode(SERVO_PIN, OUTPUT);
  setServoAngle(TARGET_SERVO_ANGLE);
}



/* Giữ hướng camera: bù quay thân xe */
inline void servoCmd(float currentYawDeg, float targetCameraYaw) {
  float servoAngle = targetCameraYaw - currentYawDeg;
  while (servoAngle < SERVO_MIN) servoAngle += 360.0;
  while (servoAngle > SERVO_MAX) servoAngle -= 360.0;
  servoAngle = constrain(servoAngle, SERVO_MIN, SERVO_MAX);
  setServoAngle(servoAngle);
}

/* Quét servo từ min đến max rồi quay lại */
inline void sweepServo(uint8_t step = 2, uint16_t delayMs = 15) {
  for (int a = SERVO_MIN; a <= SERVO_MAX; a += step) {
    setServoAngle(a);
    delay(delayMs);
  }
  for (int a = SERVO_MAX; a >= SERVO_MIN; a -= step) {
    setServoAngle(a);
    delay(delayMs);
  }
}

/* ✅ STOP SERVO: ngắt xung và cập nhật góc hiện tại */
inline float stopServo() {
  pinMode(SERVO_PIN, OUTPUT);
  digitalWrite(SERVO_PIN, LOW);              // Ngừng gửi xung PWM
  target_servo_yaw = current_servo_angle;    // Cập nhật góc mới
  return current_servo_angle;                // Trả về góc hiện tại
}

#endif
