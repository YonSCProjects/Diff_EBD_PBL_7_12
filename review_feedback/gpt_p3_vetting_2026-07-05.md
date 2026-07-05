# GPT Hebrew pass — Project 3 — vetting record (2026-07-05)

**Run:** `node improve_hebrew_gpt.js` on all 12 P3 Hebrew task cards, model `gpt-5.5-2026-04-23`.
**Raw proposals:** `gpt_p3_proposals_2026-07-05.md` (74 proposals).
**Vetted by Claude against `Hebrew_Translation_Preferences_Log.md` + locked design decisions.**

## Result: ~60 accepted (8 modified) · 14 rejected

*(A planned 3-edit sync to P4's T2_M3 turned out unnecessary — the P4 twin is the speed/correction card and contains none of the light/sound mode phrases; the exact-match guard correctly skipped all three.)*

### Accepted — main classes
- **Real grammar breaks:** "אין לא אור ולא צליל" → "אין אור ואין צליל"; "מגיב פחות יציב" → "בצורה פחות יציבה"; "זה לא תקלה" → "זו לא תקלה"; doubled "בערך" removed.
- **The "שומרת על" idiom sweep (T2_M5 + T1_M6, 8 spots):** "מה האזעקה שומרת" → "על מה האזעקה שומרת" etc. — also fixes a card↔poster mismatch (the poster column already says "על מה האזעקה שלי שומרת").
- **B3 leftovers (T1_M3):** "קוד שמדליק אותו" → "שמאיר אותו", "האור נדלק" → "הלד מאיר".
- **Mode-agnostic response descriptions (T2_M3):** "דולקת ומצפצפת" → "פועלת", "נדלקת ונכבית" → "פועלת ומפסיקה", buzzer prompt "נדלק וכבה" → "עם הפסקות" — a sound-only alarm doesn't "light". **Synced to P4's twin card too.**
- **Component-precision:** "שניהם נעצרים/נפסקים" → "הלד כבה והזמזם משתתק/מפסיק לצפצף"; "האזעקה דלוקה" → "פועלת"; sensor explanation "מרחק רגיל… מאות סנטימטרים".
- **Calques/clarity:** "להחליט מושלם", "כמו להושיט", "מתקרב אל מתחת", "אין לו ממה להחזיר הד", "חוצה את ה-20 ס"מ" → "יורד מתחת ל-20 ס"מ", "מה בדיוק יוצא" → "קורה", ambiguous "דילגתם על שני השלבים" → "על אזעקה בשני שלבים", "קערת חיה" → "קערת חיית מחמד".
- **Register:** "קחו את הזמן שלכם" → "לוקחים את הזמן"; "אינכם" → "לא"; A5 "אפשר ל-" for optional actions (photo, self-check); A2 "עוזר לנו"; long why/expected blocks split into short sentences.
- **Gender-neutral prompt template (T2_M4):** "אני עובד על…" → "זאת אזעקת הקרבה שלי מפרויקט 3."
- **Modified before applying (8):** kept "שימו לב" headers but fixed זה→זו; kept the warm "נרגעת"; impersonalized the code-preview box while keeping "אתם מבינים מה שיניתם"; aligned "הבחירה לא צריכה להיות מושלמת" with P4's accepted form; T3 intruder-quote aligned to T2_M2's "אל תיגעו בדברים שלי"; clearer "כשהמרחק קטן מ-20 ס"מ".

### Rejected — and why
- **The "האזעקה נדלקת" idiom sweep (T2_M2 ×3, T3, T2_M4-quote):** during the P3 build this was deliberately kept as idiomatic Hebrew for whole-alarm activation. Consistent decision, multi-occurrence replacement risk. **Program-wide question for Yon:** standardize alarm verbs (נדלקת ↔ מופעלת/מגיבה)?
- **"חיישנים אמיתיים אינם מושלמים, וזה בסדר גמור" (T1_M5):** the fails-gracefully reassurance is the design point (master doc §6.7).
- **P2-mirror phrasings:** "הזמזם על הברדבורד", "לא באותו טור, זה ייצור קצר" (family catchphrase), "שימו לב" callout headers.
- **"מקשיב להד" → "קולט":** the listening metaphor is the deliberate kid-friendly framing (and GPT itself kept מקשיב elsewhere).
- **Sensor-seating "בשורה ישרה אחת":** technically correct per the breadboard vocab (one lettered row, four columns) — more precise than "קו ישר".
- **"וחגג איתכם" removal, "בשבילכם ובשביל כל הקבוצה" trim:** deliberate Principle-8 warmth.
- **"זה תקין"→"הוא תקין", catchphrase micro-edits:** the "זה תקין/נורמלי, לא תקלה" form is the program catchphrase (one נורמלי→תקין change WAS accepted to unify within P3).
