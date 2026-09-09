# Project 9 — sketches

One sketch per milestone; each is self-contained (the shared pin map is documented in
`pins.h`, but every sketch carries its own copy of the pins it uses so it compiles alone).

| sketch | card | what it proves |
|---|---|---|
| `00_hello_blink` | T1·M2 | the ESP32-S3 is alive (onboard RGB blinks) |
| `01_click_test` | T1·M3 | the board IS a USB mouse — the silent switches click on screen |
| `02_sensor_test` | T1·M5 | the PMW3360 moves the cursor |
| `03_basic_mouse` | T1·M6 | clicks + cursor + front scroll + middle click |
| `04_dpi_roller` | T1·M7 | rear roller changes speed live, three LEDs show the level |
| `05_full_wired` | T1·M8 | side buttons + function layer + layer LED — the full wired mouse |
| `06_bt_mouse` | T1·M11 | the same mouse over Bluetooth, no cable |
| `T2_mouse_starter` | T2 | 06 with a marked TUNING BLOCK for the Claude Code sessions |

## Tools settings (Arduino IDE)

- **Board**: `ESP32S3 Dev Module` (esp32 board package by Espressif)
- **USB Mode**: `USB-OTG (TinyUSB)` — required for sketches 01–05. Without it the
  computer never sees a mouse. (For 06/T2 it does not matter; USB is only for upload.)
- Everything else stays at defaults.

If an upload will not start, hold **BOOT**, tap **RESET**, release BOOT, retry.
After an OTG-mode sketch is running, the serial port may vanish — that is normal for a
device that became a mouse; use BOOT+RESET to get back to upload mode.

## Libraries

- **PMW3360 Module** by SunjunKim (Library Manager). Carries the sensor's SROM firmware
  and uploads it in `begin()` — this is why the sketch does not ship a blob of its own.
- **ESP32-BLE-Mouse** by T-vK (06 and T2 only). If the Library Manager does not list
  it, install the ZIP from its GitHub releases page.

## Honesty note (same as Project 8)

These sketches are **not compile-tested** — this machine has no ESP32 core installed.
They were written against the documented APIs of the esp32 Arduino core 3.x
(`USB.h`/`USBHIDMouse.h`, `rgbLedWrite`) and the two libraries above, and reviewed
statically. The first student session that uploads them is the real test; expect at
most small compile fixes, and let Claude Code make them.

## Deviations from the source plan (recorded, deliberate)

1. **Control pins re-assigned.** The plan's GPIO 25–34 do not exist / are not usable on
   an ESP32-S3 (22–25 absent, 26–32 flash, 19/20 native USB). Sensor pins 10–14 kept —
   they are the S3's default SPI. New map in `pins.h`.
2. **AMS1117-3.3 dropped from the power path.** Its ~1.1 V dropout is below a Li-ion's
   voltage for most of the discharge curve, so the plan's battery→LDO rail browns out.
   The build uses the Project 8 pattern instead: battery → TP4056 (protected) → power
   switch → MT3608 boost pre-tuned to **5.0 V** → the DevKit's **5V pin**; peripherals
   feed from the DevKit's 3V3 output.
3. **2.4 GHz dongle mode moved out of the core build** — it needs a second ESP32-S3
   (optional in the BOM). Bluetooth is the wireless mode of the card set; the dongle is
   a Tier-3 extension idea.
