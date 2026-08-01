#!/usr/bin/env node
// improve_hebrew_gpt.js — send Hebrew task cards (.dc.html) to the OpenAI API
// and get back Hebrew-improvement PROPOSALS (before/after), never rewritten files.
//
// Usage:
//   node improve_hebrew_gpt.js <card.dc.html> [more-cards...] [--out <file>] [--model <id>]
//
// Requires the OPENAI_API_KEY environment variable (see error message below for setup).
// Model: --model flag > OPENAI_MODEL env var > default below.
// Proposals print to stdout (or --out file); token usage prints to stderr.
//
// The proposals are meant to be vetted by Claude Code against
// Hebrew_Translation_Preferences_Log.md before any card is edited.

const fs = require('fs');
const path = require('path');

const API_URL = 'https://api.openai.com/v1/chat/completions';
const DEFAULT_MODEL = 'gpt-5.5';
const PREFS_LOG = path.join(__dirname, 'Hebrew_Translation_Preferences_Log.md');

function fail(msg) {
  console.error(msg);
  process.exit(1);
}

// ---- parse args ----
const args = process.argv.slice(2);
const cards = [];
let outFile = null;
let model = process.env.OPENAI_MODEL || DEFAULT_MODEL;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--out') outFile = args[++i];
  else if (args[i] === '--model') model = args[++i];
  else cards.push(args[i]);
}
if (cards.length === 0) {
  fail('Usage: node improve_hebrew_gpt.js <card.dc.html> [more-cards...] [--out <file>] [--model <id>]');
}
for (const c of cards) {
  if (!fs.existsSync(c)) fail(`Card file not found: ${c}`);
  if (!c.endsWith('.dc.html')) console.error(`Warning: ${c} is not a .dc.html card — sending anyway.`);
}

const apiKey = process.env.OPENAI_API_KEY;
if (!apiKey) {
  fail(
    'OPENAI_API_KEY is not set.\n\n' +
    'One-time setup:\n' +
    '  1. Create an API key at https://platform.openai.com/api-keys\n' +
    '     (needs prepaid API credits — ChatGPT Plus does NOT include API access)\n' +
    '  2. Set it as a user-level environment variable:\n' +
    '       setx OPENAI_API_KEY "sk-..."\n' +
    '  3. Restart the terminal / VS Code, then re-run this script.'
  );
}

if (!fs.existsSync(PREFS_LOG)) fail(`Style guide not found: ${PREFS_LOG}`);
const prefsLog = fs.readFileSync(PREFS_LOG, 'utf8');

const SYSTEM_PROMPT = `You are an expert Hebrew-language editor reviewing educational task cards for a robotics workshop for EBD students (emotional and behavioral difficulties, grades 7-12). The cards must use simple, direct, warm Hebrew — short sentences, no preachy or redundant prose.

You will receive the full source of one card: an HTML-like ".dc.html" document in which Hebrew student-facing text is interleaved with HTML tags, inline style attributes, {{ }} template tokens, <sc-if> blocks, English text, and Arduino code.

Your task: propose improvements to the HEBREW STUDENT-FACING TEXT ONLY, following the binding style guide at the end of this message.

HARD CONSTRAINTS:
- Propose changes only to Hebrew prose text nodes.
- Never propose edits to HTML tags, attributes, inline styles, {{ }} tokens, <sc-if> blocks, English UI text, file paths, or code (sketches, pin names, commands).
- Each "Before" quote must be an EXACT contiguous substring of the card source and must contain NO HTML markup — plain Hebrew text only (punctuation, digits, and Latin product names like Arduino appearing inside the sentence are fine).
- Each "After" text must be a drop-in replacement for the "Before" text: same meaning, valid in the same position, no added markup.
- Breadboard vocabulary: the numbered strips (1-30) are "טורים"; the lettered strips (a-j) are "שורות". Component legs go into different טורים, never שורות.
- Do not propose changes for their own sake. If the Hebrew is already good, return few or zero proposals.

OUTPUT FORMAT (markdown, ordered high confidence first):

### Proposal N
**Pattern:** style-guide pattern ID + name if one applies, otherwise "—"
**Location:** short quote of the nearest heading or surrounding context, so the spot is easy to find
**Before:**
> exact Hebrew text as it appears in the card
**After:**
> improved Hebrew text
**Rationale:** 1-2 sentences.
**Confidence:** high | medium | low

End with a **Summary** line: number of proposals and the main issue types found.
If there is nothing to improve, output exactly: "No proposals — the Hebrew is consistent with the style guide."

BINDING STYLE GUIDE (Hebrew_Translation_Preferences_Log.md):

${prefsLog}`;

async function reviewCard(cardPath) {
  const cardSource = fs.readFileSync(cardPath, 'utf8');
  const res = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model,
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: `Card file: ${path.basename(cardPath)}\n\n${cardSource}` },
      ],
    }),
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`OpenAI API error ${res.status} for ${cardPath}:\n${body}`);
  }
  const json = await res.json();
  const u = json.usage || {};
  console.error(`[${path.basename(cardPath)}] model=${json.model} in=${u.prompt_tokens} out=${u.completion_tokens} tokens`);
  return json.choices[0].message.content;
}

(async () => {
  const sections = [];
  for (const card of cards) {
    console.error(`Reviewing ${card} ...`);
    const proposals = await reviewCard(card);
    sections.push(`## ${path.basename(card)}\n\n${proposals}`);
  }
  const output = sections.join('\n\n---\n\n') + '\n';
  if (outFile) {
    fs.writeFileSync(outFile, output, 'utf8');
    console.error(`Proposals written to ${outFile}`);
  } else {
    console.log(output);
  }
})().catch((err) => fail(String(err.message || err)));
