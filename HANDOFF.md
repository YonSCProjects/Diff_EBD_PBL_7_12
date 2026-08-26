# HANDOFF — Arduino PBL at Agourim School

**Written 2026-08-26, on moving this project out of the Claude Code environment it was built in.**

You are picking up a curriculum, not a codebase. The code exists only to produce two things: a
set of **Hebrew task cards** that students in a special-education robotics workshop hold in their
hands, and the **figures printed on them**. Every tool in this repo is downstream of that.

Read this file top to bottom once. It is long because the project is nine months old and has a
lot of hard-won convention in it, and because several of the ways to damage it are silent.

---

## 1. The project in one page

**Who it is for.** Yonatan Lev El runs a robotics workshop at Agourim School (בית ספר עגורים) in
Nahariya for 4–8 students in grades 7–12 with emotional and behavioural difficulties (EBD). Each
student works on an individual project. The programme is differentiated: the same milestone is
offered at several levels of independence.

**What the deliverable is.** Eight Arduino projects, each a set of Hebrew **task cards** — one
card per milestone — that a student can follow with a teacher nearby. A card is a single
self-contained HTML page (`.dc.html`) that prints to A4 and also works on screen with
checkboxes that persist. Around them sit reference cards, a master programme document, and a
funder-facing overview.

**Language.** The Hebrew cards are the **only** development target (standing rule since
2026-08-05). English card sets exist, are stale, and must not be used as a source for anything.

**Where the project stands.** Projects 1–8 all have full Hebrew card sets. The figures are the
active work: wiring diagrams are done, step figures were rebuilt in Blender in August 2026 and
are good but not finished. Yon's verdict, 2026-08-25: *"ok its better, we still need some
improvements."*

**Scale.** 156 Hebrew cards in all — 130 task cards plus 26 reference cards, all `.dc.html`.
About 60 Blender step figures, 22 Fritzing wiring figures, a 428 KB master document, and roughly
310 MB of project assets.

**Repository weight.** `git gc` was run on 2026-08-26 and took the object store from 1.53 GiB in
3,627 loose objects to **658 MB packed**. Most of the remaining weight is the committed card
bundles in `build_output/` (18 tracked files, ~397 MB), which inline every figure as base64. If
those bundles do not need to be in git, dropping them would shrink the repository by more than
half — worth asking Yon, since he works from `build_output/`.

---

## 2. The five things that will bite you

Read these before touching anything.

### 2.1 Words are final

`dc_design_spec.md` §0 is the Prime Directive: when converting or
laying out a card, you reflow text into components — you never reword it. `check_text.js` exists
as a gate because a previous tool silently reworded and condensed a whole project's cards. If a
sentence must change, it changes because Yon said so, in his words.

### 2.2 A figure must be published over the filename the card already embeds

Every Blender build
script carries a `PUBLISH` map of `scene:figure_name`. The right-hand side is not a label — it is
the exact filename in `task_cards_he/assets/` that a card's `<img src>` points at. Publishing
under a fresh name once produced a folder of beautiful renders that no student ever saw, because
the cards kept showing the old artwork. `node _blender/shot_cards.js <project-dir>` exists to make
that impossible to repeat: it opens every card and exits non-zero if any image failed to load.

### 2.3 The card source is not what the student sees

`.dc.html` files are React templates. The
runtime in `support.js` boots, replaces `<x-dc>` with a rendered tree, resolves `{{ }}` holes,
drops `<sc-if>` branches whose condition is false, and hoists `<helmet>` into `<head>`. Measured
on one card: **24 visible ✓ marks with JavaScript off, 4 with it on.** So — any tool that edits a
card works on the **source bytes**; any tool that judges what a student sees must **run the
runtime and wait for it to settle**. `render_cards_lib.js` does the settling; `build_single_card.js`
does *not* (it disables JS) and should not be used for dc cards despite what
`card_authoring_process.md` step 6 says.

### 2.4 Review exports are cumulative, and they re-export applied edits

The review console exports the
*entire* localStorage state on every save, so same-sitting saves are supersets — process the
newest. But it also re-exports edits that were applied in earlier rounds, because the console
cache is not reset. **Every edit in the 2026-08-25 round was a stale re-export of the 2026-08-23
round.** Always verify: if `beforeText` is absent from the card and `afterText` is present, the
edit is already applied — skip it. And remind Yon to press **"איפוס הכל"** in the console.

### 2.5 Hardware beats the card

A build step is not evidence about the hardware. On 2026-08-24 a
figure was rebuilt from hot-glue to screws because the card's own step 4 said "screwed, not
glued" — and the motors have no screw holes at all. Both were wrong; the figure had been made to
match a wrong instruction. This is rule **H5** in the preferences log. When a figure and a step
disagree, resolve against the actual part, then fix both.

---

## 3. First hour in a new environment

### 3.1 What must be installed

| Tool | Version here | Needed for |
| --- | --- | --- |
| Node | v24.14.1 (≥18) | every build script |
| npm packages | `puppeteer ^24.40`, `pdf-lib ^1.17`, `jszip ^3.10` | run `npm install`; puppeteer downloads its own Chromium |
| Python 3 | 3.14.4 | the `.claude` hooks, `_blender/preview.sh` (needs **Pillow**) |
| Blender | **4.5.12 LTS**, portable | all step figures |
| Fritzing desktop | any recent | all wiring figures — **and its `fritzing-parts/core` library, which is NOT vendored here** |
| Pandoc | v3+ | DOCX output only (`build_outputs.bat`) |
| `md-to-pdf` | via `npx`, not a declared dep | the overview PDFs |

`package-lock.json` is gitignored, so dependency resolution is unpinned. If a build behaves
oddly on a fresh install, that is the first thing to suspect.

### 3.2 Absolute paths that must be rewritten

| Where | Value | Override? |
| --- | --- | --- |
| `.mcp.json` | `C:\Python314\python.exe`, `C:\Fritzing mcp\run_mcp.py`, cwd `C:\Fritzing mcp` | **none — highest-severity blocker** |
| `_blender/build_*.sh`, `preview.sh` | `/c/Users/Yon/tools/blender-4.5.12-windows-x64/blender.exe` | `BLENDER=` env |
| `_fritzing_kit/build_figure.js`, `extract_pins.js`, `make_fzz.py` | `C:/Program Files/Fritzing` | `FRITZING_PATH=` env |
| `build_outputs.bat` | `%LOCALAPPDATA%\Pandoc\pandoc.exe` | edit |
| `.claude/settings.local.json`, two agent prompts | `/c/Users/Yon/...` | cosmetic |

**The nastiest one is not a path.** Both `PostToolUse` hooks in `.claude/settings.json` gate on
the literal folder name `Diferential pbl for BE` — typo included. Rename or relocate the folder
and **both hooks silently stop firing**: no error, no warning. If you keep the hooks, fix the
matcher; if you drop them, know what they did (see §7.4).

### 3.3 What needs a network at run time

- `support.js` fetches **React 18.3.1 + ReactDOM UMD from unpkg.com** on every card render.
  Offline, no dc card renders. This is why `render_cards_lib.js` waits for `networkidle0`.
- `render_cards_lib.js` and `_blender/compose.js` pull Rubik and JetBrains Mono from Google Fonts.
- `improve_hebrew_gpt.js` calls the OpenAI API and needs `OPENAI_API_KEY` (never set here).

### 3.4 There is no CI

No `.github/`, no pipeline. Everything is local hooks plus hand-run scripts. The only automated
guards are the two hooks and `shot_cards.js` / `build_card_nav.js --check` when you remember to
run them.

### 3.5 What does not travel in `.claude/`

`settings.local.json` is **untracked**. On the new machine it takes with it
`enabledMcpjsonServers: ["fritzing"]` and the whole permission allowlist — so the MCP will not
auto-enable and permission prompts come back. Recreate it or accept the prompts.

Also outside the repo and therefore gone: the global `~/.claude/CLAUDE.md` (which held the
Fritzing MCP rules), the user-level `/save` and `/end-session` commands, and the memory directory
— whose key encodes the absolute path, so **it is orphaned by moving the folder even on the same
machine**. That memory is archived in `docs/context-archive/` (§10).

### 3.6 Smoke test — prove the environment works

```bash
npm install
node build_card_nav.js --check                       # exits 1 on nav drift
node _blender/shot_cards.js Arduino_Projects/Project_4_Line_Following_Car
BLENDER=/path/to/blender bash _blender/preview.sh s_wiring   # writes _blender/work/_sheet.png
node build_cards_only.js he 4                        # → build_output/Project_4_Cards_he.pdf
```

If all four pass, you have a working environment.

### 3.7 How to actually look at a card

There are three obvious ways and two of them are wrong.

- ❌ Opening the `.dc.html` over `file://` — `support.js` needs the network and
  `--allow-file-access-from-files`; you get the raw template.
- ❌ `node build_single_card.js <card>` — it disables JavaScript, so every checkbox renders
  pre-ticked (§2.3).
- ✅ **`start_review.bat`, then `http://127.0.0.1:8765`** — the review console, which is also
  where Yon works.
- ✅ Or a settled render through `render_cards_lib.js` — which is what `build_cards_only.js` and
  `_blender/shot_cards.js` both do.

### 3.8 What a green build means

After editing a card, three checks close the loop. There is no CI, so they are yours to run:

```bash
node build_card_nav.js --check                       # nav in sync?          exit 1 on drift
node _blender/shot_cards.js <project-dir>            # every image loads?    exit 1 on broken
node build_cards_only.js he <N>                      # bundle regenerates?
```

Add `node check_text.js <source> <target>` whenever text was carried from another file — that is
the verbatim gate (§2.1).

**Wall-clock, so you do not start an hour-long job thinking it is quick:** a Cycles figure is
**~2–2.5 minutes**, so a whole-project re-render is 15 min (P5/P7) to **70 min (P8's 28 figures)**.
`--eevee` previews are seconds. `--compose-only` re-labels in about a second per figure. A cards
bundle takes a few minutes and can produce a 50–90 MB PDF.

---

## 4. Repo map

```
Arduino_Projects/            the curriculum — 8 project folders + 3 shared kits
  Project_N_<name>/
    task_cards_he/           ← THE source of truth. P*_T*_M*_<slug>_he.dc.html
      support.js             the dc runtime (vendored artifact, identical in all 8)
      card_nav.js            GENERATED — do not hand-edit
      assets/                the figures cards embed as ./assets/<name>
    reference_cards_he/      R-cards, also .dc.html (R0 breadboard, R1 wiring, R2 stuck
                             protocol, R3 prompts, R4 safety, R5 sketches, R6 soldering)
    images/                  canonical figure masters + images/fritzing/ sources
    <sketches>.ino
  _blender/  → no, it is at repo root; see below
  _fritzing_kit/             wiring-figure pipeline (real parts)
  _illustration_kit/         RETIRED renderer — see §5.3
_blender/                    step-figure pipeline (Blender)
build_output/                generated bundles; gitignored except Project_N_Cards*
review_feedback/             review-console exports + GPT-pass artefacts
docs/context-archive/        ← the previous environment's memory; see §10
fritzing_steps/              canonical P1 .fzz sources
articles_full_texts/         80 research papers backing the literature review
tools/card_figures/          small Fritzing part-inspection helpers
_render3d/                   abandoned WebGL experiment — ignore
```

**Root scripts.** `build_cards_only.js` (the one you will use most), `build_single_card.js`
(avoid for dc — see §2.3), `build_card_nav.js`, `build_overview_with_cards.js`,
`render_cards_lib.js` (library, not a CLI), `check_text.js`, `svg_to_png.js`,
`fix_wiring_svgs.js`, `improve_hebrew_gpt.js`, `review_server.js` + `review_console.html` +
`start_review.bat`.

**Two asset conventions, and nothing states this anywhere else.** A **task** card references
`./assets/<name>.svg`; a **reference** card references `../images/<name>.svg`. The `assets/`
folder is a copy of what lives in `images/`. This is why an orphan check restricted to
`./assets/` produces false positives, and why deleting an "unused" asset can be wrong.

**Card file naming.** `P<n>_T<t>_M<m>_<slug>_he.dc.html` — project, **tier**, milestone.
`build_card_nav.js` parses it. The tier is not a version number: it is the differentiation axis,
and it governs how much scaffolding a card carries. The tiers are defined in
`Robotics_Workshop_DI_PBL_Framework.md` part 3 — read that before authoring, because you cannot
pick the right register without it. Project 1's cards omit the `P1_` prefix; every other project
carries it.

**Root documents.** `dc_design_spec.md` and `card_authoring_process.md` are the two authoring
contracts. `Arduino_PBL_Program.md` is the 428 KB master. `Arduino_Principles.md` holds the ten
design principles. Four preference logs (§6.3). The literature-review set and `Verification_Log.md`.

---

## 5. The three figure pipelines

They are complementary, not competing. A single P4 card can carry figures from two of them.

| | `_blender/` | `_fritzing_kit/` | `_illustration_kit/` |
| --- | --- | --- | --- |
| Answers | *what are the hands doing* | *what connects to what* | both — superseded |
| Status | **authoritative, step figures** | **authoritative, wiring figures** | **retired renderer** |
| Covers | P4, P5, P7, P8 — ~60 figures | P4–P8 — ~22 figures | — |

### 5.1 `_blender/` — step figures

Read `_blender/README.md` first; it is current and detailed. The two ideas that make the output
work:

**Ink outlines.** `lib.outlines()` runs a Freestyle contour pass over silhouette, border, crease
and material-boundary edges. A raytraced image already hides what should be hidden, but without
an outline every part dissolves into a neighbour of similar tone — a near-white polygal plate on a
pale bench, a grey motor can against a grey rim. This single change is what took the figures from
"soft product render" to "technical illustration".

**Annotations stay out of the render.** The scene builds hardware only and registers named
anchors in millimetres. `render.py` projects them to pixel coordinates beside the PNG;
`compose.js` hangs the Hebrew callouts on them. A wording change therefore costs a re-compose
(a second) instead of a re-render (two minutes a frame), and the type stays vector-crisp at print
size. `--compose-only` is the flag for that.

**Framing is automatic.** `lib.camera_fit()` binary-searches the closest camera distance that
still holds every anchor inside the frame, because `compose.js` refuses to draw a label whose
anchor is off-screen — hand-picked distances were silently dropping callouts. `subject=` aims at
the midpoint between a named anchor and the content centroid; `extra=L.bbox_pts(...)` adds
must-be-visible points that carry no label, such as a car's wheels.

```bash
bash _blender/build_p4.sh                    # whole project, Cycles
bash _blender/build_p7.sh s_power_rails      # one scene
bash _blender/build_p8.sh --compose-only     # re-label, no re-render
bash _blender/build_p5.sh --eevee            # fast preview
bash _blender/preview.sh s_wiring s_track    # contact sheet, look-and-fix loop
node _blender/shot_cards.js <project-dir>    # prove it reached the cards
```

Roughly two minutes per Cycles frame at 1800×1350 on CPU.

### 5.2 `_fritzing_kit/` — wiring figures

Builds real `.fzz` sketches (openable in Fritzing) plus the composited `*_breadboard.svg` the
cards embed. It supplies the parts Fritzing core lacks — ESP32 DevKit, ESP32-CAM, L298N, TT
motor, FTDI, buck converter, TCRT5000, 8×AA box. Read its README before touching it. Note that
Fritzing's core parts library is **not vendored in this repo**, so a machine without Fritzing
installed cannot rebuild these.

### 5.3 `_illustration_kit/` — retired, but do not delete

Its `iso.py` sorted polygons with a painter's algorithm, which **cannot** produce correct
occlusion for interlocking geometry. Every depth bug fought in P5/P7/P8 traced back to that one
cause; that diagnosis is why the Blender pipeline exists. Do not draw anything new with it.

Three things in it are still live and must not be deleted:
- `parts.py` / `parts_p8.py` — the millimetre geometry the Blender modules were ported from
- `p8_facts_and_briefs.json` — the per-card authority for Project 8: pin map, rotation table,
  power tree, MOSFET channel wiring, and a brief with Hebrew callouts for every card
- `embed_steps.js` — **still the script that inserts summary figures into cards.** A live
  dependency stranded in a retired kit; worth moving.

---

## 6. Conventions that are law

### 6.1 Hebrew

| Rule | Detail |
| --- | --- |
| **Plural impersonal verbs** (לשון סתמית) | `מחברים`, `מסתכלים`, `קוראים` — never imperative (`חבר`, `קחו`). Gender-neutral and non-commanding; explicitly chosen for a population where directive language triggers opposition. An imperative in Yon's own edit text is a typing slip — normalise it and say so. |
| **Geresh ׳ (U+05F3)** on option letters | `אפשרות ב׳`, `חלק ג׳`, `(א׳)(ב׳)(ג׳)`. Verified: 40 option labels in the cards, all marked. Not applied to prepositions (`ב-Arduino`) or transliterations (`ג'אמפר`). |
| **No comma before conjunctive ו** | Swept: 349 removals across 75 cards. Where removing it creates a garden path, repair by swapping ו for **אבל** — never by restoring the comma. |
| **Breadboard vocabulary** | numbered strips 1–30 = **טורים**; lettered strips a–j = **שורות**. LED legs go into different **טורים**, never שורות. |
| Optional tasks | use `אפשר ל-` rather than the plural impersonal, which is reserved for primary instructions. |

**Open convention gap:** gershayim (״) was never standardised. The render layer uses typographic
״ (U+05F4) — 201 occurrences under `_blender/` — while the cards still carry **98 ASCII** `מ"מ` /
`ס"מ`. The geresh decision ("one mark, one function, programme-wide") would imply sweeping these
too, but no rule was ever written. Worth asking Yon.

### 6.2 Protected motifs

Locked programme-level phrases that outrank any learned rule: `זה תקין, לא תקלה`, `סיימתם כש:`,
`בלי פאניקה`, `חיישנים אמיתיים אינם מושלמים וזה בסדר גמור`, the celebration blocks on final
milestones. Do not generalise a rule over them.

**One is currently in dispute.** The soldering escalation `קוראים למורה, תמיד` was a locked motif
that must never be trimmed — and on 2026-08-25 Yon deleted it himself on P4 T1_M2. Eight
instances survive (P4 M1/M4/T2_M1/T2_M5/T3, P8 T2_M2, R4, R6) and were deliberately **not** swept.
The carve-out is recorded as *suspended, not lifted*. Do not trim another one without asking.

### 6.3 The four preference logs

| Log | Lines | Maintained by | Holds |
| --- | --- | --- | --- |
| `Card_Editing_Preferences_Log.md` | 1111 | the `/learn-changes` skill | card-authoring rules learned from Yon's own edits, on a TENTATIVE → FIRM → CONFIRMED ladder |
| `Hebrew_Translation_Preferences_Log.md` | 495 | the hebrew-translation-reviewer agent | verb binyan, calques, register, markup conventions |
| `Editorial_Preferences_Log.md` | 293 | the editorial-coherence agent | Yon's editorial voice (frozen since April) |
| `Verification_Log.md` | 145 | the article-verifier agent | citation verification status |

`Card_Editing_Preferences_Log.md` is the one that matters day to day. **FIRM and CONFIRMED rules
are applied silently when authoring; TENTATIVE ones are leanings.** Its header ladder and its
"Processed feedback ledger" are load-bearing — the ledger is how `/learn-changes` knows what it
has already ingested.

### 6.4 Research standard

Only 100 %-verified citations with real authors and real DOIs go into programme documents.
Unverified ones are removed and logged. This is absolute.

---

## 7. How work actually flows

### 7.1 Authoring a new card

`card_authoring_process.md` has the full seven steps. In outline: author from `dc_design_spec.md`
(the component library, extracted verbatim from eight approved exemplars) → wiring diagram →
`check_text.js` verbatim gate → reviewer agents → optional GPT Hebrew pass → rebuild → Yon's
review console.

### 7.2 The review loop

This is the heartbeat of the project.

```
Yon runs start_review.bat  →  reviews cards in the browser  →  saves
    → review_feedback/feedback_YYYY-MM-DD_HHMM.json
        → "apply the feedback"   (the apply-feedback skill)
            → cards edited, bundles rebuilt, ONE consolidated commit
        → "/learn-changes"       (the learn-changes skill)
            → Card_Editing_Preferences_Log.md updated, committed alone
```

The console is at `http://127.0.0.1:8765`. It auto-discovers every
`Arduino_Projects/Project_*/task_cards_he/*.html` with no project filter — 130 cards today —
so new projects appear without any change.

**It is a wording tool.** Its `edits[]` bind to text blocks; there is no way to anchor a comment
to a region of a figure. Figure feedback therefore arrives as free-form `cardNote` / `globalNotes`
prose, and lands as instructions to interpret rather than mechanical replacements.

### 7.3 Yon's working preferences

- For a batch of review fixes across many cards: **one end-to-end run and one consolidated
  commit** — not per-proposal confirmations. Resolve ambiguities by judgment and list them in the
  commit message.
- When he says "use X in all cards", apply it literally. Do not invent semantic exceptions from
  your own reasoning. (The one place I departed from this — leaving safety goggles in Project 8's
  propeller cards while removing them from the soldering cards — is flagged openly in §9, not
  done silently.)
- For a new project's card set: one batch of concrete hardware questions first, then the whole
  process autonomously.
- `build_output/` must be regenerated after every content change; he works from it.

### 7.4 The two hooks

Both are `PostToolUse` on `Edit|Write|MultiEdit`. One nudges the citation verifier when a project
markdown file changes; one runs `.claude/build-reminder.py`, which reminds that build outputs must
be regenerated. Both gate on the literal folder name — see §3.2.

---

## 8. State of play

| Project | Subject | Task cards | Ref cards | Step figures | Wiring figures |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 Light Signals | LEDs, patterns | 16 | 6 | — | 2 |
| 2 Reaction Time Game | button, buzzer, timing | 13 | 6 | — | 9 |
| 3 Don't Get Too Close | HC-SR04 proximity alarm | 12 | 6 | — | 4 |
| 4 Line-Following Car | first soldering, L298N | 15 | 7 | **17** | 5 |
| 5 Remote-Controlled Car | ESP32, Wi-Fi driving | 14 | 0 | **7** | 3 |
| 6 ESP32 Wi-Fi Controller | — | 15 | 0 | — | 5 |
| 7 Camera Explorer | ESP32-CAM, drive by video | 17 | 0 | **8** | 4 |
| 8 Tiny Quadcopter | MOSFET board, tethered hover | 28 | 1 | **28** | 6 |

Step figures exist only where the build is physical enough to need them. Projects 5, 6 and 7 have
**no reference cards** — whether they need them is an open question for Yon.

**Every image referenced by every one of the 218 card files resolves on disk** — zero broken
references, verified 2026-08-26. Thirteen assets are present but unreferenced, and all thirteen
are duplicate copies: the live copy lives in `<project>/images/` and reference cards point at it
as `../images/…`. When auditing this yourself, resolve `../` references too — a check restricted
to `task_cards_he/*.dc.html` and `./assets/` reports false orphans (it wrongly flagged three P4
wiring figures that R1 does reference).

One figure is genuinely built and embedded nowhere: **`w_p8_06_full_drone_breadboard.svg`**.

---

## 9. Open work, ranked

### 9.1 Figure work Yon has asked for and not yet received

From the 2026-08-25 review round, all on Project 4 and all still open. These are the concrete
next tasks:

1. **Figures below the text, and larger.** Asked four separate times on the chassis card. This is
   rule **V6**; it is a change to the embed scripts and the step wrapper width, not a text sweep.
2. **The step-6 figure is illegible** — "can't tell where the Arduino is, where the L298N is,
   where the batteries are."
3. **The step-7 figure is wrong** — no sensor visible, no front visible, and a stray soldering
   iron that the step never mentions.
4. **The drill must read as a drill**; **the motor shaft must be visible**; **remove the yellow
   masking-tape rectangles** from the cut-plate figure.
5. **No breadboard on the car** — the M4 wiring figure still shows one.
6. Rules **V6** and **V7** in the preferences log are the general statements of 1–4. V7 is worth
   using as an acceptance test: read the step aloud and point at each noun in the render.

### 9.2 Five Project 8 figures are probably stale — re-render them

**This is a suspicion, not a proven fact — treat it as such.** The 28 P8 step figures were
written in three runs on 2026-08-24. `p8_drone.py` — the shared quadcopter model **every** P8
figure draws — was last written at **20:21**, which is after five of the figures were rendered
and before the other twenty-three. That *could* mean those five draw an older model; it could
equally have been a comment change or a no-op save. `p8_drone.py` has a single commit, so git
cannot tell you, and Cycles output is stochastic, so re-rendering and comparing bytes cannot
either. The cheap move is simply to re-render them and stop wondering:

```
s_p8_parts   s_p8_press_fit   s_p8_mount   s_p8_t2_solder1   s_p8_t2_solder24
```

Git shows one coherent state — all 28 were committed together; only the mtimes hint at the split.
About twelve minutes:

```bash
bash _blender/build_p8.sh s_p8_parts
bash _blender/build_p8.sh s_p8_press_fit
bash _blender/build_p8.sh s_p8_mount
bash _blender/build_p8.sh s_p8_t2_solder1
bash _blender/build_p8.sh s_p8_t2_solder24
node build_cards_only.js he 8
```

The third run that same evening (four figures at 21:31–21:38) was *not* an interruption — it was
a deliberate, complete re-render of exactly the four scenes that call `_usb_aside()` after the
USB coil was moved. That one is consistent. P4 is clean too.

**The structural problem behind this:** `build_p8.sh` and its siblings have **no staleness
check**. They render whatever you name and nothing compares a figure's age against its sources.
Edit a shared module — `lib.py`, `p4_car.py`, `p8_drone.py`, `props.py`, `tools.py` — and every
figure that draws it is silently stale. Until something checks this, the rule is: **after
touching a shared model, re-render the whole project, not the scene you were looking at.**

### 9.3 The hand

`_blender/hand.py` models an adult hand at real millimetres and is **deliberately not used in any
figure**. Its `flat` and `point` poses read; the curled ones (`press`, `pinch`, `grip`) still read
as a mitten with sticks. Every card brief describes a hand doing something, so finishing it is the
single biggest remaining lever on figure quality. When it is finished, put it everywhere the
briefs call for one — not in two figures out of sixty. Check poses with the `s_handcheck` scene.

### 9.4 Blocked on a decision from Yon

- **Pull P4 T1_M1 out of Project 4** into a family of intro cards (soldering, breadboard,
  Arduino…). Renumbers all eight P4 steps, the progress percentages, the nav and the bundle, and
  needs a home and naming scheme that do not exist yet. Rule **C6**.
- **Remove R-card references from task cards.** Rule **C7**. 85 references survive across 38
  cards, and most are substantive — `בודקים מול כרטיס העזר R1` sends the student to the wiring
  table. Deleting the pointer leaves the instruction dangling, so this needs a *replacement*
  (inline the table? a student-facing card?), not a sweep.
- **Safety goggles in Project 8.** Yon asked for every mention removed "in these projects",
  justified by soldering being simple. Done for the soldering cards. In P8, goggles are a
  *propeller* rule — "משקפי מגן בכל רגע שמנוע יכול להסתובב", inside the six flight-day safety
  rules — so **68 mentions across all 28 P8 task cards** were left standing pending his word.

  **This left a live inconsistency that needs fixing either way.** Goggles survive in **31 card
  files**, not 28: the 28 P8 task cards *plus three reference cards* —
  `P8/reference_cards_he/R1_flight_safety_he`, and **`P4/reference_cards_he/R4_safety_reminder_he`
  and `R6_soldering_basics_he`**. Those last two are P4's own soldering cards. P4's task cards now
  say there are three safety rules and no goggles; P4's reference cards still say four rules with
  goggles. Whichever way Yon decides, R4 and R6 must be brought into line with the task cards.
- **The soldering motif** — see §6.2.
- **The gershayim convention** — see §6.1.

### 9.5 Carried over from earlier phases

These predate the current figure work and are written in prose rather than as TODO markers —
there are no `TODO`/`FIXME` markers anywhere in the repo, by convention.

- **The GPT Hebrew pass never ran on P1 and P2.** P3 and P4 went through it on 2026-07-05;
  `card_authoring_process.md` step 5 records P1/P2 as still on the backlog.
- **Project 8 propeller guards are undecided and not in the kit.** Until they exist, every
  practice flight is tethered — that is why the tether appears in every P8 flight figure. The P8
  brief also leaves the cell size open.
- **Three deferred sweeps** in `Card_Editing_Preferences_Log.md`: rule **P1** (minimal commas,
  FIRM, sweep deferred), rule **P2**'s remaining per-instance cases, and an open note that the
  R0 "single leg" instances swept under the no-carve-outs rule **may want reverting**.
- **Two loose ends from the last learn run**: P2 T2_M2's JS branch messages were never reviewed,
  and T2_M1's done-when still requires Claude Code to be open although the step that opened it
  was trimmed away.

### 9.6 Two questions from Yon still unanswered

- *"Why 3.5 mm?"* for the sensor holes — he is right that half-millimetre bits are awkward to buy;
  3 mm or 4 mm both work if the M3 screw is a clearance fit. Needs a decision, then a text fix.
- He referenced a link to the exact motor model in a review comment, but the link did not come
  through in the note text. Ask for it.

### 9.7 Smaller loose ends

- `embed_steps.js` is a live dependency inside the retired illustration kit — move it.
- `build_single_card.js` disables JavaScript and so mis-renders dc cards; either fix it or remove
  the recommendation from `card_authoring_process.md` step 6.
- `_blender/README.md` claims `shot_cards.js` writes a contact sheet; it does not.
- `embed_m3_steps.js` is missing from the README's file table.
- `_illustration_kit/README_P8.md` still says "`scenes_p8.py` does not exist yet — that is the
  next thing to write". It does exist, in both kits. Stale.
- Until this file, the repo had **no root README or onboarding document** — subsystem READMEs
  only (`_blender/`, `_fritzing_kit/`, `_illustration_kit/`, `tools/card_figures/`, P8 sketches,
  P4 Fritzing sources). If you add one, point it here rather than duplicating.
- Four unpublished Blender scenes exist as QA aids, not card figures: `s_toolcheck`,
  `s_toolcheck2`, `s_hero`, `s_handcheck`. That is intentional — but `s_hero` is the one with no
  docstring saying so; give it one or delete it. Everything else lines up exactly: 60 published
  scenes, 60 `PUBLISH` entries, 60 callout JSONs, no orphans in either direction.
- Both `_blender/` and `_illustration_kit/` contain files named `scenes_p4.py`, `scenes_p5.py`,
  `scenes_p7.py`, `scenes_p8.py`. Only the `_blender/` ones are live. Check your path.
- `_render3d/` is an abandoned WebGL experiment, superseded by `_blender/`. Deletable.
- **`build_overview_with_cards.js en` is silently broken.** It splits the overview at
  `<!-- INSERT_CARDS_HERE -->`; that marker appears once in
  `Arduino_PBL_Program_Overview_he.md` and **zero times in the English one**, so the English build
  falls through to appending the cards at the end instead of at Appendix 1. No error is raised.
- `support.js` is a **vendored build artifact**. Its own header says it is generated from a
  `dc-runtime/src/*.ts` tree with `bun run build` — and that tree is not in this repo. All 156
  cards depend on it, and it hard-codes a pinned React 18.3.1 UMD URL from unpkg with an SRI
  hash. If unpkg or that pin ever goes stale, every card stops rendering and there is no
  documented way to rebuild. Worth finding the source tree, or vendoring React locally.

---

## 10. Context that does not travel

The Claude Code sessions that built most of this kept a persistent memory outside the repo — 53
files, 357 KB. It has been copied to **`docs/context-archive/`** so the move does not lose it.
Read `docs/context-archive/README.md` for how it is organised and which parts are stale.

This handoff document supersedes anything in the archive that disagrees with it. The archive's
`feedback_*` files are the most durable part — they are standing instructions rather than status.

Two other things do not travel: the `/save` and `/end-session` commands lived at user level, not
in the repo; and the Fritzing MCP server is an unversioned tree at `C:\Fritzing mcp\` outside this
repository.

---

## 11. How not to break this

1. **Do not rename the repo folder** without fixing both hook matchers (§3.2).
2. **Do not publish a figure under a new filename.** Overwrite the name the card embeds, then run
   `shot_cards.js`.
3. **Do not hand-edit `card_nav.js`** — it is generated. Re-run `node build_card_nav.js` after
   adding or renaming a card, and `--check` in review.
4. **Do not run a programme-wide sweep because a rule says FIRM.** Sweeps happen only when Yon
   approves them; `/learn-changes` proposes, it never applies.
5. **Do not trust a card's own text about hardware** (§2.5).
6. **After editing a shared Blender module, re-render the whole project.** Nothing detects a
   figure that is older than the model it draws — that is how five P8 figures went stale (§9.2).
7. **Do not use `build_single_card.js` on a dc card** (§2.3).
8. **Do not reword Hebrew** unless Yon wrote the new words (§2.1).
9. **Do not re-apply a review round without the staleness check** (§2.4).
10. **Do not treat the English cards as a source.** They are stale by standing rule.
11. **Regenerate `build_output/`** after any content change, and commit the tracked bundles.

---

## 12. A suggested first week

1. Stand the environment up and pass the smoke tests in §3.6, and read §3.7 so you look at cards the right way.
2. Read `_blender/README.md`, `dc_design_spec.md` §0–3, and `card_authoring_process.md`.
3. Re-render the five suspect P8 figures (§9.2) — it is mechanical, twelve minutes, it exercises
   the whole pipeline end to end, and it clears a known inconsistency.
4. Do the Project 4 figure work in §9.1. Preview with `preview.sh`, verify with `shot_cards.js`,
   rebuild the bundle, one commit.
5. Take the §9.4 decisions to Yon in a single batch — he prefers one set of concrete questions
   over a trickle.
6. Then the hand (§9.3), which is where the next real quality step is.
