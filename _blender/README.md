# `_blender/` — the step-figure pipeline

Every **step** illustration for Projects 4, 5, 7 and 8 is rendered here: hardware modelled in
Blender, ink outlines drawn by Freestyle, Hebrew callouts composited over the render as SVG.

It replaced `Arduino_Projects/_illustration_kit/`, which sorted its polygons with a painter's
algorithm. That algorithm cannot produce correct occlusion for interlocking geometry, and every
depth bug fought in P5, P7 and P8 traced back to it. A z-buffer renderer is the fix, and the
same renderer gives real shadows and real materials for free.

Wiring diagrams still come from `Arduino_Projects/_fritzing_kit/`. The two kits answer different
questions: this one shows what the student's hands are doing, that one shows what connects to
what.

## Running it

Portable Blender lives at `C:\Users\Yon\tools\blender-4.5.12-windows-x64\blender.exe`; override
with `BLENDER=...`. Node is needed for the compositor.

```
bash _blender/build_p4.sh                # Cycles, full quality, publishes into the cards
bash _blender/build_p4_m3.sh             # the seven chassis-assembly step figures
bash _blender/build_p5.sh --eevee        # fast preview of a whole project
bash _blender/build_p7.sh s_power_rails  # one scene
bash _blender/build_p8.sh --compose-only # re-label without re-rendering
bash _blender/preview.sh s_wiring s_track   # contact sheet for the look-and-fix loop
node _blender/shot_cards.js Arduino_Projects/Project_5_Remote_Controlled_Car
```

Each build script's `PUBLISH` map is the load-bearing part: it writes **over the exact filename
the card already embeds**. Publishing under a fresh name is how the first attempt at this
produced a folder full of good renders that no student ever saw. `shot_cards.js` exists to make
that impossible to repeat — it opens every card and fails on any image that did not load.

## Files

| file | what it is |
| --- | --- |
| `lib.py` | units, primitives, materials, lighting, cameras, anchors, render |
| `p4_car.py` | the line-following car, with an Uno or an ESP32 brain |
| `p8_drone.py` | the tiny quadcopter |
| `tools.py` | the Project 4 hand tools |
| `props.py` | phone, cone, FTDI, ESP32-CAM, buck, scale, tray, meter, prop box, LiPo bag, post |
| `hand.py` | a hand — modelled, **not yet used**, see its docstring |
| `scenes_p4.py`, `scenes_p4_m3.py`, `scenes_p5.py`, `scenes_p7.py`, `scenes_p8.py` | one `s_*()` per figure |
| `callouts/*.json` | the Hebrew for each figure, keyed by anchor name |
| `compose.js` | render + anchors + callouts → one self-contained SVG |
| `render.py` | the CLI every build script drives |
| `preview.sh` | EEVEE contact sheets |
| `shot_cards.js` | screenshots the cards and fails on a missing image |

## The two ideas that make the figures work

**Ink outlines.** `lib.outlines()` runs a Freestyle pass over silhouette, border, crease and
material-boundary edges. A raytraced image already hides what should be hidden, but without an
outline every part dissolves into its neighbour wherever their tones are close — a near-white
polygal plate against a pale bench, a grey motor can against a grey rim. The ink line is what
turns a soft product render into a technical illustration, and it is the single biggest quality
step in this pipeline.

**Annotations stay out of the render.** The scene builds hardware and registers named anchors in
millimetres; `render.py` projects them to pixel coordinates beside the PNG; `compose.js` hangs
the Hebrew on them. A wording change costs a re-compose (a second) instead of a re-render (a
minute a frame), and the type stays vector-crisp at print size.

## Framing

`lib.camera_fit()` places the camera at the closest distance that still holds every registered
anchor inside the frame. Hand-picked distances were why callouts kept vanishing: `compose.js`
refuses to draw a label whose anchor is off-screen, so a bench prop carrying the whole point of
a card silently lost its Hebrew. Two knobs matter:

- `subject='drone'` centres the frame on one anchor instead of on the bounding box of all of
  them, so the thing the card is about sits in the middle and the accessories sit at the edges.
- `extra=L.bbox_pts(...)` adds points that must be in view but carry no label — a car's wheels,
  for instance, which no callout ever points at but which cannot be cropped off.

Accessory anchors are placed on the side of the accessory that faces the subject (`_near()` in
the scene modules), so a 130 mm meter beside a 50 mm board is free to run off the frame edge
while its callout still lands on it.

## Gotchas that cost real time

- `bpy.ops.object.transform_apply()` acts on the **selected** object, and objects made with
  `bpy.data.objects.new()` are never selected — it silently transformed something else. Use
  `lib._bake()`, which transforms the mesh data directly.
- `box()` bakes its scale into the mesh and puts the object origin at the box **centre**. Place a
  rotated segment by its midpoint; placing it by its start vertex leaves it hanging half its own
  length past where it belongs.
- A scene that calls `_bench()` must not also call `L.ground()`. Two coplanar surfaces z-fight,
  the shadow catcher wins, and you get a black bench-shaped hole.
- Area-light watts are real units: 11–26 W at 0.3–0.5 m, with `view_settings.exposure = -0.45`.
- A row of little boxes gets inked box by box and a strip of floor tape comes out looking like a
  bicycle chain. Use `lib.ribbon()`, which builds one mesh with exactly two contours.
- A laptop lid's screen normal ends up at `(sin ang, -cos ang)` while the camera sits at
  `(cos az, -sin az)`, so the screen faces the lens at `ang = 90 - az`. Back it off about 30° or
  the screen fills the frame and the laptop stops reading as a laptop.
- `world_to_camera_view` reads `matrix_world`, which is stale on a freshly created object until
  `bpy.context.view_layer.update()` runs.
- Bash heredocs in this environment corrupt escapes and occasionally drop a character. Write
  patch scripts to a file and run them.
