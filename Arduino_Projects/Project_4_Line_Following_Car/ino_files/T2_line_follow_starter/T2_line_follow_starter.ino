// ============================================================
// Project 4 - Line-Following Car
// Tier 2 STARTER: tune your own car
// ============================================================
//
// This is the full line-follower, with the settings YOU tune
// marked at the top. Change only the numbers in the "THINGS YOU
// CAN CHANGE" box - you do not have to touch anything below it.
//
//   BASE_SPEED  - how fast the car drives (0-200).
//                 Slow ~110, medium ~140, fast ~180.
//                 200 is the MAX - the 8 x AA pack is 12V when fresh and
//                 would over-volt the 3-6V motors above that.
//   CORRECTION  - how strongly the car steers back to the line.
//                 Gentle ~60, strong ~110.
//                 (CORRECTION must stay SMALLER than BASE_SPEED.)
//   LINE_IS_HIGH - only if the car steers AWAY from the line:
//                 flip true <-> false.
//
// Ask Claude Code to help you change these, then upload and test
// on YOUR track. Tuning takes two or three tries - that is how
// real engineers do it too.
// ============================================================


// ====== THINGS YOU CAN CHANGE (this is your design) ======
const int  BASE_SPEED   = 140;   // driving speed (0-200 MAX): slow 110 / medium 140 / fast 180
const int  CORRECTION   = 90;    // steering strength: gentle 60 / strong 110
const bool LINE_IS_HIGH = true;  // flip only if the car steers away from the line
// =========================================================


// ---- PIN NUMBERS (you do not need to change these) ----
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


// Returns true when the given sensor sees the black line.
bool seesLine(int sensorPin) {
  int reading = digitalRead(sensorPin);
  return LINE_IS_HIGH ? (reading == HIGH) : (reading == LOW);
}

// Set both motors forward, each at its own speed.
void drive(int leftSpeed, int rightSpeed) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
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
    drive(BASE_SPEED, BASE_SPEED);              // straight ahead
  }
  else if (leftOnLine && !rightOnLine) {
    drive(BASE_SPEED - CORRECTION, BASE_SPEED); // steer left
  }
  else if (!leftOnLine && rightOnLine) {
    drive(BASE_SPEED, BASE_SPEED - CORRECTION); // steer right
  }
  else {
    stopMotors();                               // end mark / lifted
  }
}
