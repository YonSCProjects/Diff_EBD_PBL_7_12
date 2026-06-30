// ============================================================
// Project 3 - Don't Get Too Close (Proximity Alarm)
// Sketch 01: Distance to Serial (read the sensor, print the number)
// ============================================================
//
// WHAT THIS SKETCH DOES:
//   1. The HC-SR04 sensor measures how far away the nearest object is.
//   2. The Arduino prints that distance, in centimetres, to the screen.
//   3. The number updates many times every second.
//
// TRY IT:
//   Open the Serial Monitor (magnifying glass, top-right of the IDE) and
//   set the speed at the bottom to 9600 baud. Then move your hand slowly
//   toward the sensor and watch the number get SMALLER. Move it away and
//   the number gets BIGGER.
//
// A BIG NUMBER (like 999) IS NORMAL. It just means nothing is close
// enough for the sensor to hear an echo come back. That is not a bug.
// ============================================================


// ---- PIN NUMBERS (which Arduino pin each sensor wire goes to) ----
const int TRIG_PIN = 12;  // Arduino sends a short "ping" out from this pin.
const int ECHO_PIN = 11;  // Arduino listens here for the echo to come back.

// ---- COMMUNICATION SPEED (must match the Serial Monitor) ----
const long SERIAL_BAUD = 9600;


// ============================================================
// readDistanceCm() - ping once and return the distance in centimetres.
// Returns 999 when no echo comes back (nothing is close enough).
// ============================================================
long readDistanceCm() {
  // Send a clean 10-microsecond pulse out on TRIG to start a measurement.
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Listen on ECHO for how long the echo takes to return, in microseconds.
  // The 30000 is a timeout so we never wait forever when no echo comes back.
  long duration = pulseIn(ECHO_PIN, HIGH, 30000UL);

  // No echo heard in time -> nothing is close. Report a big number.
  if (duration == 0) {
    return 999;
  }

  // Sound travels about 1 cm every 58 microseconds, out and back.
  // So the distance in cm is the echo time divided by 58.
  return duration / 58;
}


// ============================================================
// setup() runs ONE time when the Arduino powers on or resets.
// ============================================================
void setup() {
  pinMode(TRIG_PIN, OUTPUT);  // we SEND pings out on TRIG
  pinMode(ECHO_PIN, INPUT);   // we READ echoes in on ECHO

  Serial.begin(SERIAL_BAUD);  // start talking to the computer over USB

  Serial.println("=================================");
  Serial.println("   DON'T GET TOO CLOSE");
  Serial.println("   Distance reader");
  Serial.println("=================================");
  Serial.println("Move your hand toward the sensor.");
  Serial.println("Watch the number get smaller!");
  Serial.println();
}


// ============================================================
// loop() runs OVER AND OVER, forever. Each pass = one measurement.
// ============================================================
void loop() {
  long distanceCm = readDistanceCm();

  Serial.print("Distance: ");
  Serial.print(distanceCm);
  Serial.println(" cm");

  delay(100);  // small pause so the numbers are easy to read
}
