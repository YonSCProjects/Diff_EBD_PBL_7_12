// ============================================================
// Project 5 - Remote-Controlled Car
// Sketch 00: ESP32 Test (is the computer ready?)
// ============================================================
//
// WHAT THIS SKETCH DOES:
//   Blinks the small blue LED that is already ON the ESP32
//   board, once per second, and prints a counting message.
//   Nothing is wired yet - this is a handshake with the board.
//
// BEFORE UPLOADING - three one-time settings:
//   1. Tools > Board > esp32 > "ESP32 Dev Module"
//   2. Tools > Port > the COM port that appears when you plug
//      the ESP32 in (unplug/replug to see which one it is)
//   3. If the upload gets stuck on "Connecting...", hold the
//      BOOT button on the board until dots start moving.
//
// WHAT SUCCESS LOOKS LIKE:
//   The blue LED near the ESP32's antenna blinks steadily.
//   Tools > Serial Monitor (115200) shows: shalom 1, shalom 2...
// ============================================================

const int LED = 2;   // the small blue LED soldered onto the board

int count = 0;

void setup() {
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  digitalWrite(LED, HIGH);
  delay(500);
  digitalWrite(LED, LOW);
  delay(500);
  count = count + 1;
  Serial.print("shalom ");
  Serial.println(count);
}
