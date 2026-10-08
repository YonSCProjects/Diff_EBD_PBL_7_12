# פרויקט 2: משחק זמן תגובה — הנחיות לקלוד קוד

ההנחיות הכלליות ב-`../CLAUDE.md` חלות תמיד. כאן רק מה שמיוחד לפרויקט הזה.

## הפרויקט בקצרה

- **חומרה:** ארדואינו + לדים + זמזם + כפתורים
- **מה לומדים:** תזמון, לוגיקת משחק
- **מעטפת הבטיחות (למידע בלבד — המורה מתדרך):** מעטפת בטיחות זהה לפרויקט 1 — 5 וולט, בלי הלחמה, מנועים או סוללות. הרכיב החדש היחיד הוא זמזם פיאזו.

## מה על השולחן

- 1 × ארדואינו Uno R3 + כבל USB
- 1 × מטריצה מלאה
- 1 × נורית LED 5 מ"מ + נגד 220Ω
- 1 × לחצן זעיר + נגד 10kΩ
- 1 × זמזם פיאזו פסיבי קטן — חדש
- 2 × נוריות + 2 נגדים 220Ω נוספים
- 1 × לחצן שני + נגד 10kΩ שני
- ~15 × חוטי גישור M-M

## הסקיצות (`ino_files/`)

גרסה 1 מעלה את הסקיצות הממוספרות כמו שהן, לפי הסדר שהכרטיסיות מכתיבות. `T2_*` הן נקודות הפתיחה של גרסה 2 — שם התלמיד משנה דבר אחד שהכרטיסייה מצביעה עליו.

- `01_wait_flash_measure` — Sketch 01: Wait, Flash, Measure (base game, no buzzer) HOW THE GAME WORKS: 1. The Arduino waits a random amount of time (2 to 5 seconds). 2. Then the LED turns ON. That is your "GO!" signal. 3. As fast as you can, press the button.
- `02_wait_flash_measure_buzzer` — Sketch 02: Wait, Flash, Measure + BUZZER This is the SAME game as sketch 01, with one new part: a buzzer. - It BEEPS at the "GO" moment (when the LED turns on). - It plays a short SUCCESS beep when you press the button. If you compare…
- `T2_buzzer_pattern_starter` — Starter B: BUZZER PATTERN FEEDBACK This builds on sketch 02 (the buzzer game). Same GO light, same random wait, same buzzer beep, same "too early" rule. WHAT IS NEW HERE: After you press the button, the Arduino looks at how fast you were
- `T2_serial_readout_starter` — Starter C: RICH SERIAL READOUT (the simplest of the three) This builds on sketch 02 (the buzzer game). Same GO light, same random wait, same buzzer beep, same "too early" rule. WHAT IS NEW HERE: After you press the button, the Arduino…
- `T2_three_led_feedback_starter` — Starter A: THREE-LED FEEDBACK This builds on sketch 02 (the buzzer game). Same GO light, same random wait, same buzzer beep, same "too early" rule. WHAT IS NEW HERE: After you press the button, the Arduino looks at how fast you were

## הכרטיסיות (`claude_support/cards/`)

קוראים את קובץ הכרטיסייה לפני שעונים על כל שאלה על שלב. הקבצים ממוספרים לפי סדר הלימוד.

### גרסה 1 — בנייה מודרכת

- `01_P2_T1_M1_wire_led_and_button.md` — מחווטים את הלד והכפתור
- `02_P2_T1_M2_upload_wait_flash_measure.md` — מעלים את קוד ההמתנה–הבזק–מדידה
- `03_P2_T1_M3_play_five_rounds.md` — משחקים חמישה סבבים
- `04_P2_T1_M4_add_buzzer.md` — מוסיפים את הזמזם
- `05_P2_T1_M5_upload_buzzer_sketch.md` — מעלים את הקוד עם משוב מהזמזם
- `06_P2_T1_M6_record_fastest_time.md` — רושמים את הזמן הכי מהיר על הפוסטר

### גרסה 2 — עיצוב מודרך

- `07_P2_T2_M1_startup.md` — הפעלה ראשונית — מקימים את המשחק ומריצים סבב
- `08_P2_T2_M2_pick_feedback_mode.md` — בוחרים מצב משוב
- `09_P2_T2_M2b_wire_three_leds.md` — מחווטים את שלושת הלדים
- `10_P2_T2_M3_pick_difficulty_and_modify.md` — בוחרים רמת קושי ומשנים את הקוד
- `11_P2_T2_M4_upload_test_tune.md` — מעלים, בודקים ומכוונים את הגרסה שלכם
- `12_P2_T2_M5_signature_game.md` — משחק חתימה — נותנים שם ומשתפים

### גרסה 3 — עיצוב פתוח

- `13_P2_T3_project_planner.md` — מעצבים את משחק זמן התגובה שלכם

## כרטיסיות העזר (`claude_support/reference/`)

- `R0_breadboard_basics.md` — איך עובד ברדבורד
- `R1_wiring_reference.md` — חיווט פרויקט 2
- `R2_stuck_protocol.md` — תקועים? קודם מנסים את זה
- `R3_claude_code_prompts.md` — איך מדברים עם קלוד קוד
- `R4_safety_reminder.md` — תזכורת בטיחות (בטיחות — של המורה)
- `R5_sketch_index.md` — איזה קוד פותחים ומתי

## נקודות שמצריכות את המורה בפרויקט הזה

- שלב 1 נעשה יחד עם המורה (לא ערוץ B).
- כל מה שהכרטיסייה מסמנת "קוראים למורה".
- בטיחות: R4 (תזכורת בטיחות) · R1 (חיווט) · R2 (פרוטוקול תקיעות) — התדריך של המורה, לא שלך.
