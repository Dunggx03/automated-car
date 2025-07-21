#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>
#include <Wire.h>
#include <MPU6050_light.h>

// Motor pins
#define IN1 13
#define IN2 12
#define ENA 11
#define IN3 10
#define IN4 8
#define ENB 9

// Servo & Sensor pins
#define SERVO_PIN 7
#define TRIG_PIN 2
#define ECHO_PIN 3

// PID
#define Kp_yaw 55.0
#define YAW_THRESHOLD (2.0 * PI / 180.0)

// Servo config
#define SERVO_MIN 0
#define SERVO_MAX 180
#define PULSE_MIN 500
#define PULSE_MAX 2500
#define PULSE_PERIOD 20000

// Speed
#define MAX_SPEED 150
#define MIN_SPEED 90
#define NEUTRAL_STEERING 127
#define STEERING_THRESHOLD 5

// Global variables
extern MPU6050 mpu;
extern float targetYawDeg;
extern float targetYawRad;
extern float targetServoAngle;
extern int current_servo_angle;

#endif
