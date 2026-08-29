# HANDOFF — Cowork back to Claude Code

**Written 2026-08-29, at the end of a Cowork phase that reworked the Project 4/5/7 step figures
and the wiring diagrams.**

This is the return leg of `HANDOFF.md`. That document is still the authority on the curriculum,
the Hebrew conventions and the repo map, and `_blender/README.md` is still the authority on how
the step-figure pipeline works. **Read both.** This file covers only what those two do not:
how to stand the toolchain up in the first place, what changed in commits `76377a3` and after,
and the traps that cost real time in this phase.

---

## 1. Standing the toolchain up

Nothing in `HANDOFF.md` or `_blender/README.md` says what to install. This is that section, and
**it contains the two things most likely to stop you on the first run.**

There are two ways to execute this pipeline, and the committed scripts use the first:

**A — the Blender application (what `build_p*.sh` expects).** Every driver script runs

```
"$BLENDER" --background --factory-startup --python _blender/render.py -- ...
```

with `BLENDER` defaulting to `/c/Users/Yon/tools/blender-4.5.12-windows-x64/blender.exe`, i.e.
Git Bash on Windows against an installed Blender 4.5.12. Override the env var if it moves.

**B — `bpy` as a pip module (what Cowork used).** No GUI Blender in a container, so:

```
python 3.11            # not 3.12 — bpy wheels are built per Python minor version
pip install bpy==4.5.12
```

`render.py` is agnostic; it just imports `bpy`. Use B for headless or CI, A for normal work.

### The two things that will stop you

**1. Pillow has to be inside the interpreter that actually runs.** `pcb.py` does
`from PIL import Image, ImageDraw, ImageFont` at module scope, and `p4_car.py`, `props.py` and
`scenes_p4.py` all import `pcb` — so essentially every P4/P5/P7 scene needs it. Under route A
that interpreter is **Blender's bundled Python**, not your system one:

```
"/c/Users/Yon/tools/blender-4.5.12-windows-x64/4.5/python/bin/python.exe" -m pip install pillow
```

Install it into system Python under route A and every scene dies at import.

**2. The silkscreen font search was Linux-only until 2026-08-29.** `pcb.py` hardcoded
`/usr/share/fonts/truetype/liberation/...`; on Windows neither path exists, PIL falls back to
`ImageFont.load_default()` — an ~11 px bitmap face at 24 px/mm — and every pin label on every
board renders as an unreadable blob **without raising**. Fixed: `_FONT_CANDIDATES` now covers
Linux, Windows and macOS and prints a warning if nothing matches. If you see that warning, add a
path rather than ignoring it — this failure is silent by nature.

**Smoke test** — under route A, and it exercises both fixes:

```
"$BLENDER" --background --factory-startup --python-expr \
  "import sys; sys.path.insert(0,'_blender'); import pcb; print('font:', pcb._FONT)"
```

A path means you are good. `None` plus the warning means fix 2 has not taken.

The callout compositor `_blender/compose.js` is **pure Node** — it carries its own PNG decoder
and needs no browser. The separate card build (`build_cards_only.js` at the repo root) does need
puppeteer's Chrome, but that is already in the root `package.json` and has been working on Yon's
machine for months.

### Rendering

A whole project, through the drivers that render, run the compositor and write the `.svg`
straight into both `images/` and `task_cards_he/assets/`:

```
bash _blender/build_p4_m3.sh                  # also build_p4 / build_p5 / build_p7 / build_p8
bash _blender/build_p4_m3.sh --eevee          # fast preview, drops to 40 samples
bash _blender/build_p4_m3.sh --compose-only   # re-label without re-rendering
bash _blender/build_p4_m3.sh --samples 128
```

One figure, if you are iterating on geometry:

```
"$BLENDER" --background --factory-startup --python _blender/render.py -- \
    s_m3_4_motors _blender/work/out.png --samples 96 --res 1700x1275
node _blender/compose.js _blender/work/out.png _blender/callouts/<name>.json out.svg
```

**A note on sample counts.** The committed scripts default to **96** Cycles samples. The 32
figures currently in the repo were rendered at **40**, because the Cowork container had two CPU
cores and 96 would have taken six hours. They are clean at 40 with OpenImageDenoise, but a
re-render through the unmodified scripts will produce slightly better images and will not match
byte-for-byte. That is expected, not a regression.

To eyeball everything at the size a card actually shows it:

```
node _blender/review/make_review.js > build_output/figure_review.html
```

### It will be much faster than it was here

`lib.py` already probes for `OPTIX`, `CUDA`, `HIP`, `ONEAPI` and `METAL` and falls back to CPU —
that logic predates this phase. The Cowork container had **two CPU cores and no GPU**, which is
the only reason 32 figures at 40 samples took roughly two and a half hours (~5 min each). On a
12-thread desktop CPU expect something like a sixth of that, and on an NVIDIA card through OptiX,
minutes for the whole set. Same scripts, no changes — the device is chosen at run time.

---

## 2. The trap that produced this whole phase

Yon's verdict on the previous figures was that they *"look like toys"*. Two rounds of work went
into geometry and shading before the actual cause turned up, so it is worth stating plainly:

**`quality.apply()` installed a light silhouette-only ink line, and four lines later `render.py`
called the legacy `lib.outlines()`, which replaced it.** Freestyle keeps exactly one lineset per
view layer, so the second call did not add to the first — it wiped it. Every figure in every
pass had been inked at `max(1.4, res/700)` — 2.4 px at 1700 — on silhouette **and** crease **and**
material boundary. A heavy black sticker outline around every object, drawn on top of correctly
rendered CAD geometry.

`render.py` now guards this with `_quality_owns_ink`, and `quality.ink()` carries a comment
saying so. **If you add any Freestyle call anywhere in the render path, check that guard.** The
two settings look independent in the source, which is why the bug survived a full review of both
files; it only showed up by rendering the same scene at three ink weights and noticing the image
never changed.

Current ink: `0.80 px`, silhouette and border only, set in `quality.ink()`.

---

## 3. CAD parts — the conventions that are not obvious

`wrl.py` reads KiCad's published VRML models; `cadparts.py` wraps each one at its real
millimetre size. Four things about that library will bite:

**KiCad authors every packages3D model with z = 0 at the PCB surface**, so a through-hole part's
solder tails sit at negative z. Referencing the mesh bounding box therefore lifts every such part
clear of the board by its own tail length — 3.0 mm on a pin header, 3.3 mm on a DIP-28. On the
Uno that read as a slightly floaty chip; on the ESP32 it turned the two 15-way strips into an
11.5 mm bed of nails that hid the module and the pin numbers a student has to read.
`wrl.load(..., z_ref='origin')` is the default and is what you want. `z_ref='bbox'` exists only
as an escape hatch.

**Every strip package in the library runs along Y**, so call sites pass `rot=90` to lay one along
X. `wrl.load` centres the model on its bounding box in x and y, so call sites pass **centres**,
not corners — unlike `lib.box()`, which takes its minimum corner. Mixing those two conventions up
is the single easiest way to misplace a component.

**Two models in `_blender/cad/` are the wrong variant and are deliberately not used.** The
crystal and the trimpot are 17 mm tall vertical parts; the boards here use the low horizontal
ones, so `pcb.py` still builds those two by hand. Do not "fix" this by switching them to CAD.

**Male pin headers on a dev board point down.** `CAD.header(..., flip=True)` turns the part over
so the plastic sits under the PCB and the pins go into a breadboard, which is how a DevKit is
actually assembled. `C.ESP_STANDOFF` (8.5 mm) then holds the board off whatever it rests on, and
the P5 scenes and the signal-wire routing all reference that constant rather than repeating the
number.

---

## 4. Anchors: the method, not just the principle

`_blender/README.md` already makes the point that an anchor which *projects* inside the frame is
not necessarily *visible*. What it does not record is how the current positions were arrived at,
which matters because they are shared.

`_car_anchors()` in each of `scenes_p4.py`, `scenes_p5.py` and `scenes_p7.py` registers one set
of anchors used by **six cameras** in P4 alone. A position that clears from one camera can sit
behind a tyre from the next. Swapping primitives for real CAD geometry moved every occluder at
once and broke eight labelled callouts — they were being drawn onto bare plastic.

The fix was not to nudge each one by eye. It was to ray-cast candidate positions from **every**
camera that shares the anchor and keep only positions clear from all of them. Two things to know
if you repeat that:

- **Update the depsgraph before ray-casting.** `bpy.context.view_layer.update()` followed by
  `bpy.context.evaluated_depsgraph_get().update()`. Without it the cast returns garbage — first
  everything reads as occluded, then everything reads as clear, and both are wrong.
- **Off-screen is not the same as occluded.** `project_anchors()` returns
  `{'width', 'height', 'anchors'}`, and an anchor outside the frame is reported with
  `visible: False` but is deliberately *not* added to the `OCCLUDED` line. A checker that treats
  the two the same will send you chasing phantoms — mine did, and it cost an hour.

The render prints `OCCLUDED anchors (...)` for hidden ones and `compose.js` prints
`HIDDEN (anchor behind geometry)` for the subset that actually carry a label. **The second list
is the one that matters** — an occluded anchor nobody labels is harmless.

As of this phase, all 32 P4/P5/P7 scenes report every anchor both on-screen and unoccluded.

---

## 5. Wiring figures: why `polish_for_print.js` exists

`_fritzing_kit/README.md` documents the tool. The measurement behind it is worth keeping:

`compose.js` in the kit draws its callout labels at a fixed size **in sketch units**, but a dc
card renders every figure at the same 640 px however much sketch that spans. Label size on the
page is therefore inversely proportional to the diagram's extent:

| figure | sketch width | label on card |
|---|---|---|
| `w_p5_01_esp32_pins` | 1,952 | 19 px |
| `w_p7_01_ftdi_upload` | 3,508 | 9.1 px |
| `w_p4_04_line_sensors` | 7,525 | 4.8 px |
| `w_p4_01_driver_wiring` | 14,525 | 3.5 px |
| `w_p7_04_full_explorer` | 10,465 | 3.2 px |

Three pixels is not small type, it is no type — which is why the wide diagrams read as mush while
the narrow ones look fine, from the same generator with the same settings.

`polish_for_print.js` removes the Fritzing watermark (it sat on top of the TCRT sensor on
`w_p4_01_driver_wiring`) and scales each label about its own centre toward ~8 px on-card, capped
at 2.2×, reducing any label that would then collide with a neighbour it was clear of, and growing
the viewBox and its white backdrop so a widened tag near an edge is not sliced. Run it after
`build_figure.js`. It is idempotent — polished labels carry `data-print-scaled`.

**One thing it cannot fix.** There is no empty margin to reclaim: Fritzing exports tight, and ink
fills the viewBox exactly in all 14 figures. The wide diagrams are crowded because the *layout*
is spread out, not because of padding. Making `w_p4_01_driver_wiring` genuinely readable needs
the parts moved closer together in the `.fzz` and a re-run of `build_figure.js` — which needs
Fritzing installed, so it is natural work for Claude Code and was not practical from Cowork.

---

## 6. Building the card bundles

`node build_cards_only.js he 4` (and `5`, `7`, …) produces `build_output/Project_N_Cards_he.html`
and `.pdf`. On Yon's machine this just works. Two things in it are worth knowing because they
will bite in any sandboxed environment, and because they explain some scar tissue:

- The `.dc.html` cards **fetch React 18.3.1 UMD from unpkg at render time**. `loadReactUmd()`
  short-circuits when `window.React` and `window.ReactDOM` already exist, so an offline
  environment can preload them via `page.evaluateOnNewDocument`. Without React the cards boot to
  a blank page and every PDF comes out as a single empty sheet — 902 bytes.
- The cards also **pull Rubik and JetBrains Mono from Google Fonts**. Without them the type
  silently falls back to Liberation Sans; the PDF still builds and looks plausible until you run
  `pdffonts` on it.

Neither of those patches is in the repo — they were local to the Cowork container.
`render_cards_lib.js` on disk is untouched. If you ever build somewhere without network, both
are re-derivable: React from `node_modules/react/umd/`, the fonts from `@fontsource/rubik` and
`@fontsource/jetbrains-mono`, which ship Google's exact files with the right `unicode-range`
values. Get the ranges right or the latin subset shadows the Hebrew one at the same weight.

Reference cards in P4 pull their images from `../images/`, **not** from `./assets/` like the task
cards. `images/` is a build input, not a mirror.

---

## 7. State of play

Committed and pushed as of `6151f72`:

- **32 step figures** re-rendered for P4/P5/P7 with CAD parts, the new shading rig and correct
  ink, installed into both `images/` and `task_cards_he/assets/` — 64 copies, verified.
- **14 wiring figures** polished, in both locations — 26 copies, verified.
- **New pipeline modules**: `wrl.py`, `cadparts.py`, `quality.py`, rewritten `pcb.py`, the
  14-model `cad/` library with its CC-BY-SA licence, and `_fritzing_kit/polish_for_print.js`.
- **Card bundles** for P4/P5/P7 rebuilt (88/40/47 pages) and committed.
- The chassis card's done-when box now says the motors are **glued with hot glue**, in Yon's own
  words from the same card — it had said screwed, which contradicted the build.

### Open

1. **No print-ready PDFs for P4/5/7.** Projects 1–3 have `Project_N_Task_Cards_he_print.pdf`
   (stage-per-page, nothing cut mid-section, white space squeezed) via `tools/print/`. The other
   three only have the on-screen bundles. Yon has never asked for these — offer, do not assume.
   Needs a per-project empirical shrink pass, like the `.zooms.json` files already there.
2. **The dense wiring diagrams** — `w_p4_01_driver_wiring`, `w_p7_02_power_rails`,
   `w_p7_04_full_explorer` — need a layout change in Fritzing to be genuinely readable. See §5.
3. **`pcb.py`'s font fix is uncommitted** as of writing — it is on disk, not in git. Commit it
   with anything else you do.
4. **`build_output/` weight.** The bundles are committed by an explicit `!` negation in
   `.gitignore` and have been re-committed **24 times**; `.git` is 825 MB.
   `Project_4_Cards_he.html` is **55.35 MB** — past GitHub's recommended 50 MB and heading for
   the 100 MB hard rejection limit. Dropping the negation and attaching bundles to a Release
   instead is a one-line fix. Worth putting to Yon; `HANDOFF.md` §1 raised it first.
5. **`_to_delete/`** — 1.1 GB, now gitignored, still on disk. `Remove-Item -Recurse -Force` it.
6. Everything under `HANDOFF.md` §9 that this phase did not touch, including the possibly-stale
   Project 8 figures.

---

## 8. What is different now that you are back on the metal

The Cowork phase reached Yon's disk through a bridge into an isolated Linux VM. Three things were
awkward there and are simply not your problem:

- **Deleting** was blocked, which is why scratch accumulated in `_to_delete/` instead of being
  removed, and why `git add` left stray `tmp_obj_*` files in `.git/objects` — git could not
  unlink its temporaries. Yon's `git gc` has since absorbed them.
- **Pushing** was impossible: the VM cannot see Windows Credential Manager. Commits were made
  through the bridge; Yon pushed.
- **Line endings.** The repo stores LF, the Windows worktree is CRLF, and git on that VM had no
  `autocrlf`, so it reported 284 modified files when only 139 had really changed. Commits from
  the bridge had to force `-c core.autocrlf=true`. **Your git normalises correctly — do not
  copy that flag into anything.**

The trade was worth it for a disposable box that could take a 1 GB `bpy` install and a headless
Chromium. For everything from here — faster renders, real git, no approval prompts — the metal is
better.
