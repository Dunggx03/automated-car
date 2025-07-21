#ifndef SENSOR_H
#define SENSOR_H

#include "config.h"

inline void setupUltrasonic() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

inline long readDistanceCM() {
  digitalWrite(TRIG_PIN, LOW); delayMicroseconds(4);
  digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH, 30000UL);
  return duration / 58;
}

#endif
