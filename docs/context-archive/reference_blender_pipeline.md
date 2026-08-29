---
name: reference_blender_pipeline
description: _blender/ renders every P4/P5/P7/P8 step figure in Cycles with Freestyle ink and Hebrew callouts composited as SVG; read its README before drawing anything new
metadata: 
  node_type: memory
  type: reference
  originSessionId: 23475edf-dbb3-4a71-8074-6f8e659f8622
  modified: 2026-08-29T08:01:42.770Z
---

`_blender/` is the source of every **step** figure for Projects 4, 5, 7 and 8. It replaced
`Arduino_Projects/_illustration_kit/` (see [[reference_illustration_kit]]) because that kit's
painter's-algorithm depth sort **cannot** produce correct occlusion for interlocking geometry —
every depth bug fought in P5/P7/P8 traced back to that one cause. A z-buffer renderer is the fix.
Wiring figures still come from [[reference_fritzing_kit]]; these two answer different questions.

Portable Blender 4.5.12 LTS lives at `C:\Users\Yon\tools\blender-4.5.12-windows-x64\blender.exe`
(chocolatey install fails without admin). Override with `BLENDER=...`.

**Modules**
- `lib.py` — units (MM = 0.001), `box`/`cyl`/`prism`/`prism_xz`/`revolve`/`helix`/`tube`/`torus`,
  `ribbon` + `ellipse_pts` (one-mesh strips: tape loops, annuli, rubber bands), `studio`,
  `ground`, `camera`, `anchor`/`project_anchors`, `render`, and **`outlines()`** — the Freestyle
  contour pass that turns a soft product render into a technical illustration.
- `p4_car.py` — the car (Uno **and** ESP32 brains). `p8_drone.py` — the quadcopter.
- `tools.py` — the P4 hand tools. `props.py` — everything the later projects put beside them
  (phone, cone, FTDI, ESP32-CAM, buck, scale, tray, multimeter, prop box, LiPo bag, post).
- `scenes_p4.py`, `scenes_p4_m3.py`, `scenes_p5.py`, `scenes_p7.py`, `scenes_p8.py` — one
  `s_*()` per figure, hardware only, registering named anchors.
- `compose.js` — render + anchors → one self-contained SVG. Supports `items` (labelled
  callouts), `arrows`, `wifi` (radio fans) and `badges` (numbered discs).
- `render.py` — the CLI. `preview.sh` — fast EEVEE contact sheets for the look-and-fix loop.
- `shot_cards.js` — screenshots every card in a project and **fails** on any `<img>` that did
  not load. This is the only honest check that a figure reached the student.

**Setting it up on Yon's machine (route A, the `build_p*.sh` path).** Those scripts drive the
installed Blender, so the interpreter that runs the scenes is **Blender's bundled Python**, not
the system one. `pcb.py` imports PIL at module scope and `p4_car.py` / `props.py` / `scenes_p4.py`
all import `pcb`, so without Pillow *in that interpreter* every P4/P5/P7 scene dies at import:

    "/c/Users/Yon/tools/blender-4.5.12-windows-x64/4.5/python/bin/python.exe" -m pip install pillow

Installed 2026-08-29 (pillow 12.3.0). Smoke test, which also proves the silkscreen font search
resolves — it was Linux-only paths until 2026-08-29 and degraded *silently* to an 11 px bitmap:

    "$BLENDER" --background --factory-startup --python-expr "import sys; sys.path.insert(0,'_blender'); import pcb; print('font:', pcb._FONT)"

A path means good; `None` plus a warning means the font fix has not taken. On Windows it resolves
to `C:/Windows/Fonts/arialbd.ttf`.

**One lineset, one owner.** Freestyle keeps exactly one lineset per view layer, so a second
`outlines()`-style call does not add to the first — it replaces it. `quality.apply()` owns the ink
now and `render.py` guards it with `_quality_owns_ink`. See [[project_handoff_to_cowork]] for how
this shipped a heavy black sticker outline on every figure for two rounds without anyone seeing it.

**Build**: `bash _blender/build_p4.sh` (also `build_p4_m3.sh`, `build_p5.sh`, `build_p7.sh`,
`build_p8.sh`). Flags: `--eevee`, `--samples N`, `--compose-only` (re-label without re-rendering),
`s_<scene>`. Each script's `PUBLISH` map is load-bearing — it writes **over the filename the card
already embeds**. See [[feedback_figures_must_reach_the_cards]].

**Hard-won gotchas**
- `bpy.ops.object.transform_apply()` acts on the SELECTED object, and `bpy.data.objects.new()`
  objects are never selected — it silently transformed something else. Use `lib._bake()`.
- `box()` bakes scale into the mesh and puts the origin at the box **centre**: place a rotated
  segment by its midpoint, never by its start vertex.
- A scene with `_bench()` must not also call `L.ground()` — coplanar surfaces z-fight and the
  shadow catcher wins, leaving a black bench-shaped hole.
- Area-light watts are real: 11–26 W at 0.3–0.5 m, with `exposure = -0.45`.
- A row of little boxes gets inked box-by-box and reads as a bicycle chain. Use `ribbon`.
- A laptop lid's screen normal ends up at `(sin ang, -cos ang)` and the camera sits at
  `(cos az, -sin az)`, so the screen faces the lens at `ang = 90 - az` (back it off ~30° so the
  base stays visible).
- Bash heredocs here eat backslashes and sometimes a stray character. Write patch scripts with
  the Write tool and run them; do not paste Python through a heredoc.
