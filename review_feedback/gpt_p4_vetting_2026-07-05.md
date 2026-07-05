# GPT Hebrew pass — Project 4 — vetting record (2026-07-05)

**Run:** `node improve_hebrew_gpt.js` on all 15 P4 Hebrew task cards, model `gpt-5.5-2026-04-23`.
**Raw proposals:** `gpt_p4_proposals_2026-07-05.md` (83 proposals).
**Vetted by Claude against `Hebrew_Translation_Preferences_Log.md` + the program's locked design decisions.**

## Result: 52 accepted (3 modified) · 31 rejected

### Accepted — main classes
- **Grammar/agreement:** missing subjects + gender in the T2_M3 choice options (המכונית עלולה / נצמדת / מתנדנדת), missing "ש-" connective, missing objects (להניח **אותה**/את המכונית), "חלק טבעי כשמעצבים".
- **Calque cleanup (C1):** "לאן חוט הולך" → "לאן מחברים חוט"; "מה מהירות עושה לעיקולים" → "איך המהירות משפיעה על עיקולים"; "נפגש/נפגשת עם" → "משתלב/משתלבת עם"; "להחליט מושלם" → "הבחירה לא צריכה להיות מושלמת"; "הולכים במעגלים" → "נתקעים שוב"; "זה מכוון" → "זה בכוונה"; "ולשתי שניות" → "ובמשך שתי שניות".
- **Technical precision (T1_M6):** the sensor's **reading** flips, not the sensor ("הקריאה שלו מתחלפת", "הקריאות של שני החיישנים מתחלפות").
- **Register (A1/A5):** "עכשיו אתם:" → "עכשיו מתאמנים:"; "אצבעות רחוק מ" → "מרחיקים אצבעות מ"; "אינכם" → "לא"; optional actions get permissive "אפשר ל-" (T2_M5 ×3); "סיימתם והכול נראה נכון?" → "כשמסיימים והכול נראה נכון,".
- **Long-sentence splits** in the why/expected/demo blocks of T1_M5/M7/M8, T2_M4/M6 (short EBD-friendly sentences, content unchanged).
- **Consistency syncs:** T2_M1's speed-preview "ומסוכן" → "ומאתגר" (aligns with the already-approved T2_M2 change) and T2_M2 "ואתגר" → "ומאתגר" (parallel adjectives); "מתנדנדת בישר" → "בקטע הישר"; "עוקבים אחר" → "אחרי".
- **Modified before applying (3):** goggles rule aligned to R4's definite form ("שהמלחם" rather than GPT's "שיש מלחם"); burn-response given a natural verb ("שוטפים מיד במים קרים" rather than GPT's "שמים מים"); T2_M6 stuck-block — only the genuinely redundant trailing sentence removed, the rest of GPT's big rewrite rejected.

### Rejected — and why
- **"ככה עובדים מהנדסים אמיתיים" removals (5×):** this is the program's deliberate recurring motif (normalizing iteration by identification), standardized across the card set; removing it is a design change, not a language fix. *If Yon wants it gone, that's a design decision for the review console.*
- **"תחזוקה, לא כישלון" softening (5×):** deliberate EBD framing from the master doc/source file — destigmatizing breakage is the point; "לא כישלון" stays.
- **"זו לא טעות שלכם" removal (T1_M5):** deliberate no-blame reassurance for the backward-wheel moment (agency pattern).
- **"סיימתם כש:" → "מסיימים כש:" (2×):** program-wide done-when header used on every card in P1–P4; changing it is a global design decision.
- **"אם הלחמתם" → "אחרי הלחמה" (3×):** meaning change — the 2nd-person conditional marks the solder-vs-jumper branch; "after soldering" reads as a sequence step for everyone.
- **P3-mirror phrasings (3×):** "שימו לב — שינוי קוד בכוחות עצמכם", "בשלב 3 תשנו", "בלי פאניקה" are verbatim from the approved Project 3 twin cards; changing only P4 breaks the cross-project mirror.
- **"זו לא העתקה" removal, "נורמלי לגמרי" → "זה קורה הרבה":** deliberate framings (Claude-Code legitimacy; the program's "זה נורמלי, לא תקלה" catchphrase).
- **"הופך הגדרה" → "משנה הגדרה":** the LINE_IS_HIGH fix literally flips a boolean; הופך is the precise family verb ("להפוך true ל-false").
- **"בכרטיסים" → "בכרטיסיות", done-when 2nd-person rewrites, minor word-order swaps:** family-consistency / marginal-gain rejections.
