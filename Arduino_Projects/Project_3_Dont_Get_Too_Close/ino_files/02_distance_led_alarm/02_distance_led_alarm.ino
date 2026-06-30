// ============================================================
// Project 3 - Don't Get Too Close (Proximity Alarm)
// Sketch 02: Distance + LED Alarm (light up when something is close)
// ============================================================
//
// WHAT THIS SKETCH DOES:
//   Everything Sketch 01 did (measure distance and print it), PLUS:
//   when the nearest object is CLOSER than 20 cm, the LED turns ON.
//   When the object moves away again, the LED turns OFF.
//
// This is your first THRESHOLD: a number from the real world crossing
// a line ("closer than 20 cm") makes something happen.
//
// Open the Serial Monitor at 9600 baud, then move your hand toward the
// sensor. When you get within about 20 cm, the LED lights up.
// ============================================================


// ---- PIN NUMBERS (which Arduino pin each part is wired to) ----
const int TRIG_PIN = 12;  // sensor: sends the ping out
const int ECHO_PIN = 11;  // sensor: listens for the echo
const int LED_PIN  = 9;   // the alarm LIGHT, through a 220 ohm resistor

// ---- THE THRESHOLD (how close is "too close") ----
const int THRESHOLD_CM = 20;  // closer than this many cm -> alarm light ON

// ---- COMMUNICATION SPEED (must match the Serial Monitor) ----
const long SERIAL_BAUD = 9600;


// ============================================================
// readDistanceCm() - ping once and return the distance in centimetres.
// Returns 999 when no echo comes back (nothing is close enough).
// ============================================================
long readDistanceCm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000UL);

  if (duration == 0) {
    return 999;  // no echo -> nothing close
  }
  return duration / 58;  // microseconds -> centimetres
}


// ============================================================
// setup() runs ONE time when the Arduino powers on or resets.
// ============================================================
void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);    // the LED is something we control

  digitalWrite(LED_PIN, LOW);  // start with the alarm light OFF

  Serial.begin(SERIAL_BAUD);
  Serial.println("=================================");
  Serial.println("   DON'T GET TOO CLOSE");
  Serial.println("   LED alarm at 20 cm");
  Serial.println("=================================");
  Serial.println();
}


// ============================================================
// loop() runs OVER AND OVER, forever. Each pass = one check.
// ============================================================
void loop() {
  long distanceCm = readDistanceCm();

  Serial.print("Distance: ");
  Serial.print(distanceCm);
  Serial.print(" cm");

  // ---- THE THRESHOLD CHECK ----
  if (distanceCm < THRESHOLD_CM) {
    digitalWrite(LED_PIN, HIGH);          // too close -> light ON
    Serial.println("   --> TOO CLOSE! (light on)");
  } else {
    digitalWrite(LED_PIN, LOW);           // far enough -> light OFF
    Serial.println();
  }

  delay(100);  // small pause between checks
}
