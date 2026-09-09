// Project 9 — the personal mouse: one pin map for every sketch.
//
// Board: ESP32-S3 DevKitC-1.  The source plan's control pins (GPIO 25-34) do not
// exist or are not usable on an S3 (22-25 absent, 26-32 = flash, 19/20 = native USB,
// 0/3/45/46 = straps, 35-37 = PSRAM on octal modules, 48 = onboard RGB LED), so the
// controls were re-pinned below. The PMW3360 pins are kept exactly as the plan wrote
// them — they are the S3's default FSPI pins, so the sensor library needs no remap.

#pragma once

// PMW3360 optical sensor (SPI) — J1, keep the harness under 40 mm
#define PIN_SENS_CS      10
#define PIN_SENS_MOSI    11
#define PIN_SENS_SCK     12
#define PIN_SENS_MISO    13
#define PIN_SENS_MOTION  14   // motion interrupt (optional in the starter sketches)

// Main click switches (silent) — J4.  INPUT_PULLUP, switch closes to GND.
#define PIN_BTN_LEFT      1
#define PIN_BTN_RIGHT     2

// Front scroll encoder, 11 mm — J2
#define PIN_ENC_F_A       4
#define PIN_ENC_F_B       5
#define PIN_ENC_F_PUSH    6   // middle click

// Rear speed roller, 9 mm — J3
#define PIN_ENC_R_A      15
#define PIN_ENC_R_B      16
#define PIN_ENC_R_PUSH   17   // toggles the side-button function layer

// Side thumb buttons — J5
#define PIN_BTN_S1        7
#define PIN_BTN_S2        8
#define PIN_BTN_S3        9

// Indicator LEDs through 330 ohm — J6
#define PIN_LED_DPI1     39
#define PIN_LED_DPI2     40
#define PIN_LED_DPI3     41
#define PIN_LED_LAYER    42
