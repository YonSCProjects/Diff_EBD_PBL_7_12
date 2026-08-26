---
name: project-gpt-hebrew-pass
description: "improve_hebrew_gpt.js sends Hebrew .dc.html task cards to the OpenAI API for improvement proposals; manual trigger only, Claude vets and applies"
metadata: 
  node_type: memory
  type: project
  originSessionId: a36e2fb6-da7d-444d-9b3e-2154a4d6d98f
---

ChatGPT second-opinion pass for Hebrew task cards (built 2026-07-05, Yon's request).

- **Script:** `improve_hebrew_gpt.js` at repo root. `node improve_hebrew_gpt.js <card.dc.html> [more...] [--out <file>] [--model <id>]`. Node 18+ native fetch, no npm deps.
- **Model:** default `gpt-5.5` (flagship GA as of July 2026, $5/M in, $30/M out); override via `OPENAI_MODEL` env or `--model`. Roughly $0.15–0.25 per card (~30k input tokens: card + full preferences log).
- **Key:** `OPENAI_API_KEY` user-level Windows env var. Yon has only ChatGPT Plus, which does NOT include API access — as of 2026-07-05 the key was not yet created; script prints setup steps (platform.openai.com/api-keys, prepaid credits, `setx`) if missing.
- **Design decisions (Yon's):** GPT returns *proposals only* (before/after, same format as [[project-hebrew-reviewer-agent]] output) — never rewrites files, protecting the fragile `.dc.html` markup ({{ }} tokens, `<sc-if>`, inline styles). **Manual trigger only** — no hook; run when Yon asks.
- **Vet-and-apply workflow:** run script → check each proposal against `Hebrew_Translation_Preferences_Log.md` + markup safety (Before-quote must exact-match the file, no markup inside) → apply accepted with Edit → rebuild build_output → optionally hebrew-translation-reviewer as final gate → report applied/rejected. Rejections revealing a stable preference → propose adding to the log (with confirmation).
- The system prompt reads the preferences log from disk at runtime, so log updates flow through automatically.
- First live run (pilot on one card, e.g. T2_M2b) still pending Yon setting the API key.
