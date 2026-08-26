---
name: global-rules-no-carveouts
description: When Yon states a vocabulary or formatting rule "in all X", apply it literally — do NOT invent semantic carve-outs from your own reasoning
metadata:
  type: feedback
---

When Yon states a global rule for a project ("use X instead of Y in all cards", "always do Z"), apply the rule literally across the stated scope. Do NOT carve out semantic exceptions based on your own reasoning about edge cases.

**Why:** On 2026-05-19 Yon said *"Use רגל in all cards instead of פין. Use הלד instead of נורת ה-LED in all cards."* I applied it across T1_M3–M8 but unilaterally decided that the L-marked indicator LED on the Arduino board was "a board indicator, not the project's LED component" and kept `נורה המסומנת L` in T1_M1 and T1_M2. I even wrote that carve-out into Pattern B6 of [[hebrew-translation-preferences]] as if it were the rule. Yon caught it on the next turn and corrected it: the L LED is also `הלד`. The carve-out was my interpretation, not his. The cost was a second commit + rebuild cycle.

**How to apply:**
- If the user says "in all" / "always" / "throughout", treat the scope as literal.
- When you notice a genuinely marginal case while applying a global rule, do NOT pre-decide. Either: (a) apply the rule globally and flag the marginal case in your end-of-task report so the user can correct it, OR (b) ask before carving the exception.
- Do not encode your own carve-out into a durable artifact (a log entry, a memory file, a code comment) as if it were the user's rule. If a carve-out belongs in the log, it must come from the user.
- The value of a unified-vocabulary rule is the *unification itself* — semantic distinctions that justify exceptions ("but it's actually a board indicator, not a project component") undermine the simplification the user is buying.

**Counter-example — when carving IS fine:** Code-level decisions inside a single function where the user has delegated judgment, or where the carve-out is required to make the code work (e.g., HTML attributes can't contain the same char as the wrapping quote). The pattern above is about *user-stated content rules*, not implementation details.
