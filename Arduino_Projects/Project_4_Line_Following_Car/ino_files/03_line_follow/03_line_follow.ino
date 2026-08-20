// ============================================================
// Project 4 - Line-Following Car
// Sketch 03: Line Follow (the car drives itself!)
// ============================================================
//
// HOW IT WORKS - the whole idea in three lines:
//   Both sensors see the floor  -> the line is between them -> drive forward.
//   LEFT sensor sees the line   -> the car drifted right    -> slow the LEFT motor (steer left).
//   RIGHT sensor sees the line  -> the car drifted left     -> slow the RIGHT motor (steer right).
//
//   (Both sensors see the line -> end mark or car lifted -> stop.)
//
// SETUP:
//   Place the car so the black tape line runs BETWEEN the two
//   sensors. Switch on the battery pack. Let go.
// ============================================================


// ---- PIN NUMBERS (L298N driver: six pins in a row, D5-D10) ----
// Note: each "motor" below is really a PAIR of motors wired in
// parallel on the same L298N channel - the code treats each pair
// as one motor, so nothing else changes.
const int ENB = 5;   // right motor pair speed (PWM)
const int IN4 = 6;   // right motor pair direction
const int IN3 = 7;   // right motor pair direction
const int IN2 = 8;   // left motor pair direction
const int IN1 = 9;   // left motor pair direction
const int ENA = 10;  // left motor pair speed (PWM)

const int SENSOR_LEFT  = 11;  // left IR sensor OUT
const int SENSOR_RIGHT = 12;  // right IR sensor OUT

// ---- DRIVING SETTINGS ----
// Keep BASE_SPEED at 200 or below: a freshly charged 8.4V battery
// pack would over-volt the 3-6V motors at full (255) duty.
const int  BASE_SPEED  = 140;   // normal forward speed (0-200)
const int  CORRECTION  = 90;    // how much the inner wheel slows in a turn
const bool LINE_IS_HIGH = true; // flip to false if your sensor boards are inverted


// Returns true when the given sensor sees the black line.
bool seesLine(int sensorPin) {
  int reading = digitalRead(sensorPin);
  return LINE_IS_HIGH ? (reading == HIGH) : (reading == LOW);
}

// Set both motors forward, each at its own speed.
void drive(int leftSpeed, int rightSpeed) {
  digitalWrite(IN1, HIGH);  // left motor forward
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);  // right motor forward
  digitalWrite(IN4, LOW);
  analogWrite(ENA, leftSpeed);
  analogWrite(ENB, rightSpeed);
}

void stopMotors() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}


// ============================================================
// setup() runs ONE time when the Arduino powers on or resets.
// ============================================================
void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(SENSOR_LEFT, INPUT);
  pinMode(SENSOR_RIGHT, INPUT);

  stopMotors();
  delay(2000);  // 2 seconds to place the car and let go
}


// ============================================================
// loop() runs OVER AND OVER, forever. Each pass = one decision.
// ============================================================
void loop() {
  bool leftOnLine  = seesLine(SENSOR_LEFT);
  bool rightOnLine = seesLine(SENSOR_RIGHT);

  if (!leftOnLine && !rightOnLine) {
    // Line is between the sensors - all good, straight ahead.
    drive(BASE_SPEED, BASE_SPEED);
  }
  else if (leftOnLine && !rightOnLine) {
    // Car drifted RIGHT (line appeared under the left eye)
    // -> slow the LEFT wheel to steer back LEFT.
    drive(BASE_SPEED - CORRECTION, BASE_SPEED);
  }
  else if (!leftOnLine && rightOnLine) {
    // Car drifted LEFT (line appeared under the right eye)
    // -> slow the RIGHT wheel to steer back RIGHT.
    drive(BASE_SPEED, BASE_SPEED - CORRECTION);
  }
  else {
    // BOTH eyes see the line: an end mark, a crossing,
    // or the car was lifted off the track. Stop safely.
    stopMotors();
  }
}
