# פרויקט 9: עכבר אישי — הנחיות לקלוד קוד

ההנחיות הכלליות ב-`../CLAUDE.md` חלות תמיד. כאן רק מה שמיוחד לפרויקט הזה.

## הפרויקט בקצרה

- **חומרה:** ESP32-S3 + חיישן אופטי PMW3360 + מתגים + גלגלת + סוללת 18650
- **מה לומדים:** עכבר אישי: הלחמה, לוח כוח, יום הסוללה, Bluetooth
- **מעטפת הבטיחות (למידע בלבד — המורה מתדרך):** שני דברים דורשים כבוד: המלחם והסוללה. אין מדחפים ואין משקפי מגן — הסכנות כאן הן מלחם חם אחד ותא ליתיום אחד.

## מה על השולחן

- 1 × ESP32-S3 DevKitC-1 N8R2, 44 פינים
- 1 × חיישן PMW3360DM-T2QU עם עדשת LM19
- 2 × אנקודרים Kailh
- 2 × מתגי Kailh GM 8.0 ללחיצות הראשיות
- 3 × מתגים זעירים 6×6×5 מ"מ
- 1 × תא NCR18650B מוגן + מחזיק קפיצי
- 1 × מודול טעינה TP4056 USB-C עם הגנת DW01A+8205A
- 1 × מתג הזזה SS12F15
- 4 × נוריות 5 מ"מ + נגדי 330Ω
- 1 × מודול MT3608 מהמלאי, מכויל ל-5.0V
- — × יריעת PTFE, חוטים, כבל USB-C

## הסקיצות (`ino_files/`)

גרסה 1 מעלה את הסקיצות הממוספרות כמו שהן, לפי הסדר שהכרטיסיות מכתיבות. `T2_*` הן נקודות הפתיחה של גרסה 2 — שם התלמיד משנה דבר אחד שהכרטיסייה מצביעה עליו.

- `00_hello_blink` — Project 9 — step 2: the ESP32-S3 is alive. Blinks the small RGB LED that is already on the DevKit board — no wiring yet. This sketch needs no special USB mode and no libraries.
- `01_click_test` — Project 9 — step 3: the first click. Two silent switches on the breadboard become the LEFT and RIGHT buttons of a real USB mouse. Plug the board in, upload, and pressing the switch clicks on screen. Tools settings that MUST be set (like…
- `02_sensor_test` — Project 9 — step 5: the cursor moves. The PMW3360 optical sensor — the mouse's eye — drives the cursor for the first time. sensor's firmware blob and uploads it at begin(). Wiring (J1, harness under 40 mm — these are the S3's default SPI…
- `03_basic_mouse` — Project 9 — step 6: a whole basic mouse. Clicks + optical sensor + the front scroll wheel (and its push = middle click). New wiring in this step (J2, the 11 mm front encoder): A → GPIO 4 · B → GPIO 5 · PUSH → GPIO 6 · C(common) → GND
- `04_dpi_roller` — Project 9 — step 7: the speed roller. The small rear roller changes the mouse speed LIVE, and three LEDs show the level. This is the project's signature feature. New wiring in this step: J3 (9 mm rear roller): A → GPIO 15 · B → GPIO 16 ·…
- `05_full_wired` — Project 9 — step 8: the whole mouse, wired. Everything together: clicks, sensor, both rollers, three side buttons, four LEDs. Pushing the rear roller toggles a FUNCTION LAYER for the side buttons; the yellow layer LED shows which layer is…
- `06_bt_mouse` — Project 9 — step 11: the cable comes off. The same full mouse, but over Bluetooth: the computer pairs with "P9-MOUSE" and the mouse runs from its own battery. No USB cable. the USB port is only used for uploading and charging.) Libraries:…
- `T2_mouse_starter` — This is 06_bt_mouse with every personal decision pulled up into the TUNING BLOCK below. In Tier 2 you change these numbers and mappings with Claude Code until the mouse fits YOUR hand — that is the whole point of building your own.

## הכרטיסיות (`claude_support/cards/`)

קוראים את קובץ הכרטיסייה לפני שעונים על כל שאלה על שלב. הקבצים ממוספרים לפי סדר הלימוד.

### גרסה 1 — בנייה מודרכת

- `01_P9_T1_M1_meet_parts_contract.md` — פוגשים את החלקים  ⛔ שער: תדריך הפתיחה של הפרויקט
- `02_P9_T1_M2_board_alive.md` — הלוח מתעורר לחיים
- `03_P9_T1_M3_first_click.md` — הקליק הראשון
- `04_P9_T1_M4_wire_the_eye.md` — מחווטים את העין
- `05_P9_T1_M5_cursor_moves.md` — הסמן זז
- `06_P9_T1_M6_scroll_wheel.md` — גלגלת הגלילה
- `07_P9_T1_M7_speed_roller.md` — גלגלת המהירות
- `08_P9_T1_M8_side_buttons_layer.md` — כפתורי הצד ושכבת הקסם
- `09_P9_T1_M9_solder_power_board.md` — מלחימים את לוח הכוח
- `10_P9_T1_M10_battery_day.md` — יום הסוללה  ⛔ שער: תדריך הסוללה
- `11_P9_T1_M11_bluetooth.md` — הכבל יורד
- `12_P9_T1_M12_mattress_test_celebrate.md` — מבחן המזרן וחוגגים

### גרסה 2 — עיצוב מודרך

- `13_P9_T2_M1_startup.md` — מעירים את העכבר
- `14_P9_T2_M2_your_speeds.md` — המהירויות שלך
- `15_P9_T2_M3_your_buttons.md` — הכפתורים שלך ושם משלו
- `16_P9_T2_M4_bed_mode.md` — מצב מיטה
- `17_P9_T2_M5_shell_mockup.md` — הקליפה מתחילה
- `18_P9_T2_M6_signature_demo.md` — הדגמת החתימה

### גרסה 3 — עיצוב פתוח

- `19_P9_T3_project_planner.md` — מתכננים הרחבה משלכם

## כרטיסיות העזר (`claude_support/reference/`)

- `R1_battery_soldering_safety.md` — בטיחות סוללה והלחמה (בטיחות — של המורה)

## נקודות שמצריכות את המורה בפרויקט הזה

- שלב 1 נעשה יחד עם המורה (לא ערוץ B).
- גרסה 1, שלב 1 — "פוגשים את החלקים": לפני השלב התלמיד עובר עם המורה על תדריך הפתיחה של הפרויקט.
- גרסה 1, שלב 10 — "יום הסוללה": לפני השלב התלמיד עובר עם המורה על תדריך הסוללה.
- כל מה שהכרטיסייה מסמנת "קוראים למורה".
- בטיחות: R1 (בטיחות סוללה והלחמה) — נקראת בקול לפני כל מפגש הלחמה ולפני כל עבודה עם הסוללה. — התדריך של המורה, לא שלך.
