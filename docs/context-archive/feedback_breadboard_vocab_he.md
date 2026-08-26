---
name: feedback-breadboard-vocab-he
description: "Hebrew breadboard vocabulary — numbered strips (1-30) are \"טורים\" (columns); lettered strips (a-j) are \"שורות\" (rows). Never call a numbered strip \"שורה\"."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 601fb431-d7ce-4a89-bb1b-b20eea8e6c67
---

In Hebrew Project 1 materials, when describing the breadboard:

- **Numbered strips (1, 2, 3, ..., 30)** = `טורים` (columns). Use `טור` for a single one (e.g. `טור 9`).
- **Lettered strips (a, b, c, d, e in the upper bank; f, g, h, i, j in the lower bank)** = `שורות` (rows).

**Why:** R0_breadboard_basics_he sets this as the canonical convention. LED legs that "go into different strips so they don't short" are in different **columns** (`טורים`), not rows — because columns are the 5-hole electrically-connected vertical strips. Drift to `שורה` for the numbered strips appeared in the tutorial and several T-cards and was corrected in commit f015f62 (2026-05-26). Yon explicitly asked for this rule across all already-created cards.

**How to apply:**
- For LED placement: "כל רגל בטור שונה" / "שתי הרגליים בטורים שונים" — never `שורה`.
- For "one strip over" / "next to" offsets: "טור אחד הצידה" / "בטור סמוך" — never `שורה אחת הצידה`.
- For the 4-pin button straddling the center gap: don't say "ארבע שורות שונות" (the legs actually occupy 2 columns × 2 rows). Prefer "ארבעה חורים שונים" or "שני טורים שונים משני צדי המרווח".
- For row labels (a, b, …, j): correct usage is `שורה a` / `השורות a–e`.

Linked: [[project-hebrew-reviewer-agent]] — this rule should be in Hebrew_Translation_Preferences_Log.md too (not yet added there as of 2026-05-26; add when next editing that log).
