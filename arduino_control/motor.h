
#include "motor.h"

void initMotors() {
  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT); pinMode(ENA, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT); pinMode(ENB, OUTPUT);
}

void moveForward(int speed) {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW); analogWrite(ENA, speed);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW); analogWrite(ENB, speed);
}

void moveBackward(int speed) {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH); analogWrite(ENA, speed);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH); analogWrite(ENB, speed);
}

void turnLeft(int speed) {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH); analogWrite(ENA, speed);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW); analogWrite(ENB, speed);
}

void turnRight(int speed) {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW); analogWrite(ENA, speed);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH); analogWrite(ENB, speed);
}

void stopMotors() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW); analogWrite(ENA, 0);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW); analogWrite(ENB, 0);
}
