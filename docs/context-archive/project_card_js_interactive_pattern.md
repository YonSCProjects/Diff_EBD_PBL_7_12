---
name: Interactive checkbox persistence pattern (card.js)
description: Hebrew HTML navigation cards have a clickable-checkbox JS feature keyed by student nickname; state persists across sessions on a shared workstation
type: project
originSessionId: 3d210c3a-c0bd-44fd-9c8b-2b5b6675b02f
---
**What this is.** `Arduino_Projects/Project_1_Light_Signals/task_cards/card.js` turns the printed-laminate navigation cards into interactive HTML cards when opened in a browser. On first load it prompts for the student's nickname (the same Cheetah/Fox/etc. convention already used for their Google Drive folder), then makes `.checklist li` items clickable. Check state is persisted in `localStorage` keyed by `"<nickname>::<card-id>::<item-index>"` so a shared workstation remembers each student's progress separately across sessions.

**Why nickname-keyed, not raw localStorage:** Agourim workstations are shared between students across sessions. A plain per-browser key would mean student B opens the card and sees student A's checkmarks already filled in — demotivating ("someone already did this"). Keying by nickname means the same browser remembers progress separately per student. Yon chose this over the simpler "reset button" approach (option B vs option A in the 2026-04-13 design discussion).

**How it's wired:**
- `<link rel="stylesheet" href="../task_cards/style.css">` + `<script src="../task_cards/card.js" defer></script>` in the card `<head>`.
- CSS additions in the shared stylesheet: `.checklist li { cursor: pointer; }`, `.checklist li.checked::before { content: "☑"; }`, `.checklist li.checked { color: #666; text-decoration: line-through; }`, `.nickname-indicator` strip styling.
- `@media print` hides the nickname bar, restores empty `☐` boxes, and removes strikethrough — so the laminated print artifact is unaffected and still works with a dry-erase marker.

**UI in browser:**
1. First load → `prompt()` asks "מה הכינוי שלך?" (stores in `localStorage` under `agourim_card_nickname`).
2. Nickname bar at top with two buttons: **החלף כינוי** (re-prompt + re-render with that nickname's stored state) and **איפוס סימונים** (reset this card's checks for this student, with confirm).
3. Click any checklist item → toggles ☑ + strikethrough; state saved per `nickname::card-id::index`.

**Status:** Wired into all 14 Hebrew Project 1 task cards as of 2026-04-13 commit `d003818`. Reference cards skipped — no `.checklist` elements so the script no-ops there anyway. Future projects (2–8) should inherit the same `<script>` line and re-use the same `card.js` file.

**Honest caveat:** `localStorage` is per-origin-per-browser. Opening the card on a different physical machine will not see the state. A student who changes workstations starts fresh on that machine (or reenters their nickname and sees state there if they used it before).
