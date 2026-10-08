# פרויקט 1: אותות אור — הנחיות לקלוד קוד

ההנחיות הכלליות ב-`../CLAUDE.md` חלות תמיד. כאן רק מה שמיוחד לפרויקט הזה.

## הפרויקט בקצרה

- **חומרה:** Arduino Uno + לדים + כפתור
- **מה לומדים:** חיווט ברדבורד, קלט/פלט דיגיטלי, העלאה ראשונה, היכרות עם קלוד קוד
- **מעטפת הבטיחות (למידע בלבד — המורה מתדרך):** מעטפת הבטיחות הנמוכה ביותר בתוכנית: אין הלחמה, אין מנועים, אין סוללות ואין חלקים נעים. הכול 5 וולט.

## מה על השולחן

- 1 × ארדואינו Uno R3 (או תואם)
- 1 × כבל USB-A ↔ USB-B
- 1 × מטריצה מלאה (~830 נקודות)
- 2–3 × נוריות LED 5 מ"מ בצבעים שונים
- 2–3 × נגדים 220Ω — אחד לכל נורית
- 1 × לחצן זעיר (4 רגליים)
- 1 × נגד 10kΩ (pull-down ללחצן)
- ~15 × חוטי גישור M-M
- 1 × מחשב Windows 11 עם Arduino IDE 2.x
- 1 × תיקיית פרויקט אישית בדרייב

## הסקיצות (`ino_files/`)

גרסה 1 מעלה את הסקיצות הממוספרות כמו שהן, לפי הסדר שהכרטיסיות מכתיבות. `T2_*` הן נקודות הפתיחה של גרסה 2 — שם התלמיד משנה דבר אחד שהכרטיסייה מצביעה עליו.

- `01_blink_L_fast` — Blinks the built-in "L" LED on the Arduino Uno faster than the factory sketch. Used at Tier 1 Milestone 2 of Project 1 — the student's first Upload click. No wiring required. The "L" LED is already on the Arduino board, connected…
- `02_blink_external` — Blinks the external LED wired to digital pin 9. Used at Tier 1 Milestone 4 of Project 1 — the student's first external LED lights up because of code they uploaded. Wiring (from Tier 1 Milestone 3): - LED long leg (anode) --> 220 Ω resistor…
- `03_blink_alternating` — Blinks two external LEDs in alternation — when one is on, the other is off. Used at Tier 1 Milestone 6 of Project 1 — the student's first multi-output sketch. Shows that a single Arduino can control two independent things at the same time.
- `04_button_control` — A push-button controls which of two LEDs is on. Used at Tier 1 Milestone 8 of Project 1 — the student's first INTERACTIVE Arduino sketch. Until now the Arduino has been the active element (blinking LEDs on its own). Now the student's input…
- `T2_alternating_starter` — Tier 2 starter sketch for the "alternating" pattern choice in Project 1. This is a Channel A Level 2 starter sketch — the student uploads it as-is first, then uses Claude Code to modify it to match their own design choices. Before asking…
- `T2_breathing_starter` — Tier 2 starter sketch for the "breathing" pattern choice in Project 1. One LED fades smoothly in and out using PWM (Pulse-Width Modulation), so it looks like it is "breathing" — slowly getting brighter, then slowly getting dimmer,…
- `T2_chasing_starter` — Tier 2 starter sketch for the "chasing" pattern choice in Project 1. Three LEDs light up one at a time in sequence, like a chase light on a sign. This is a Channel A Level 2 starter sketch — the student uploads it as-is first, then uses…

## הכרטיסיות (`claude_support/cards/`)

קוראים את קובץ הכרטיסייה לפני שעונים על כל שאלה על שלב. הקבצים ממוספרים לפי סדר הלימוד.

### גרסה 1 — בנייה מודרכת

- `01_T1_M1_setup_workspace.md` — מחברים את הארדואינו ומכינים את עמדת העבודה
- `02_T1_M2_first_upload.md` — מעלים את הקוד הראשון ומאיצים את ההבהוב
- `03_T1_M3_wire_first_led.md` — מחווטים את הלד החיצוני הראשון
- `04_T1_M4_light_up_led.md` — מעלים את הקוד ומדליקים את הלד
- `05_T1_M5_add_second_led.md` — מוסיפים לד שני
- `06_T1_M6_alternating_blink.md` — מעלים את קוד ההבהוב לסירוגין
- `07_T1_M7_wire_button.md` — מחווטים את הכפתור
- `08_T1_M8_button_control.md` — מעלים את הקוד שמופעל בעזרת הכפתור

### גרסה 2 — עיצוב מודרך

- `09_T2_M1_startup.md` — הפעלה ראשונית — ארגון עמדת העבודה, לד ראשון, העלאה ראשונה.
- `10_T2_M2_pick_pattern.md` — בוחרים תבנית אור
- `11_T2_M2a_wire_second_led.md` — מוסיפים לד שני לתבנית לסירוגין
- `12_T2_M3_claude_code_level2.md` — משנים את הקוד בעזרת קלוד קוד
- `13_T2_M4_button_behavior.md` — מוסיפים את הכפתור, בוחרים את התנהגותו
- `14_T2_M5_signature_pattern.md` — תבנית חתימה ותצוגה
- `15_T2_M2b_wire_third_led.md` — מוסיפים שני לדים לרדיפה

### גרסה 3 — עיצוב פתוח

- `16_T3_project_planner.md` — מעצבים את פרויקט 1 שלכם

## כרטיסיות העזר (`claude_support/reference/`)

- `R0_breadboard_basics.md` — איך עובד ברדבורד
- `R1_wiring_reference.md` — חיווט פרויקט 1
- `R2_stuck_protocol.md` — תקועים? קודם מנסים את זה
- `R3_claude_code_prompts.md` — איך מדברים עם קלוד קוד
- `R4_safety_reminder.md` — תזכורת בטיחות (בטיחות — של המורה)
- `R5_sketch_index.md` — איזה קוד פותחים ומתי

## נקודות שמצריכות את המורה בפרויקט הזה

- שלב 1 נעשה יחד עם המורה (לא ערוץ B).
- כל מה שהכרטיסייה מסמנת "קוראים למורה".
- בטיחות: R4 (תזכורת בטיחות) · R1 (חיווט) · R2 (פרוטוקול תקיעות) — התדריך של המורה, לא שלך.
