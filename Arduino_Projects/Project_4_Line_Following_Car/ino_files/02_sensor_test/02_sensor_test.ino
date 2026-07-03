// ============================================================
// Project 4 - Line-Following Car
// Sketch 02: Sensor Test (see what the car's "eyes" see)
// ============================================================
//
// WHAT THIS SKETCH DOES:
//   Reads the two IR line sensors many times a second and prints
//   what each one sees to the Serial Monitor:
//       LEFT: FLOOR   RIGHT: LINE
//
// TRY IT:
//   Open the Serial Monitor (magnifying glass, top-right) at 9600
//   baud. Hold the car over the black tape line and slide it slowly
//   left and right. Watch each side flip between FLOOR and LINE
//   exactly when that sensor crosses the tape.
//
// The motors do NOT move in this sketch - it is eyes only.
// ============================================================


// ---- PIN NUMBERS ----
const int SENSOR_LEFT  = 11;  // left IR sensor OUT
const int SENSOR_RIGHT = 12;  // right IR sensor OUT

// ---- SENSOR POLARITY ----
// Most sensor boards read HIGH over black tape (no reflection).
// If your readings are flipped (LINE on bare floor), change
// this to false.
const bool LINE_IS_HIGH = true;

// ---- COMMUNICATION SPEED (must match the Serial Monitor) ----
const long SERIAL_BAUD = 9600;


// Returns true when the given sensor sees the black line.
bool seesLine(int sensorPin) {
  int reading = digitalRead(sensorPin);
  if (LINE_IS_HIGH) {
    return reading == HIGH;
  } else {
    return reading == LOW;
  }
}


// ============================================================
// setup() runs ONE time when the Arduino powers on or resets.
// ============================================================
void setup() {
  pinMode(SENSOR_LEFT, INPUT);
  pinMode(SENSOR_RIGHT, INPUT);

  Serial.begin(SERIAL_BAUD);
  Serial.println("=================================");
  Serial.println("   LINE-FOLLOWING CAR");
  Serial.println("   Sensor test (eyes only)");
  Serial.println("=================================");
  Serial.println("Slide the car across the tape line");
  Serial.println("and watch the readings flip.");
  Serial.println();
}


// ============================================================
// loop() runs OVER AND OVER, forever. Each pass = one reading.
// ============================================================
void loop() {
  Serial.print("LEFT: ");
  Serial.print(seesLine(SENSOR_LEFT) ? "LINE " : "FLOOR");
  Serial.print("   RIGHT: ");
  Serial.println(seesLine(SENSOR_RIGHT) ? "LINE " : "FLOOR");

  delay(200);  // five readings per second - easy to follow
}
