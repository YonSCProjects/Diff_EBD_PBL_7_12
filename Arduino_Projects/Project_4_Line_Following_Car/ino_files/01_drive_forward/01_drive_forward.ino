// ============================================================
// Project 4 - Line-Following Car
// Sketch 01: Drive Forward (first motor test)
// ============================================================
//
// WHAT THIS SKETCH DOES:
//   Both wheels spin FORWARD at medium speed for 3 seconds,
//   pause for 1 second, and repeat. Forever.
//
// IMPORTANT - BEFORE UPLOADING:
//   Prop the car up so the wheels spin in the AIR and the car
//   cannot drive off the desk. Only after you see both wheels
//   spinning forward, put it on the floor for a real run.
//
// IF ONE WHEEL SPINS BACKWARD:
//   That is normal, not a mistake. Swap that motor's two wires
//   at the L298N output terminals (OUT1 <-> OUT2 for the left
//   motor, OUT3 <-> OUT4 for the right motor) and test again.
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

// ---- SPEED (0 = stopped, 200 = fastest allowed) ----
// Keep speeds at 200 or below: a freshly charged 8.4V battery
// pack would over-volt the 3-6V motors at full (255) duty.
const int DRIVE_SPEED = 150;  // medium speed for the first test


// ---- small helpers so the loop is easy to read ----

// Both motors forward at the given speed.
void driveForward(int speed) {
  digitalWrite(IN1, HIGH);  // left motor forward
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);  // right motor forward
  digitalWrite(IN4, LOW);
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
}

// Both motors off.
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

  stopMotors();   // start still
  delay(2000);    // 2 seconds to put the car down / step back
}


// ============================================================
// loop() runs OVER AND OVER, forever.
// ============================================================
void loop() {
  driveForward(DRIVE_SPEED);  // go...
  delay(3000);                // ...for 3 seconds

  stopMotors();               // rest...
  delay(1000);                // ...for 1 second
}
