# The Blender pipeline — high-quality step figures

Replaces the flat isometric SVGs for the step illustrations. The hardware is modelled and
path-traced; the Hebrew callouts stay vector and are composited afterwards.

Currently built out for **Project 4 only**. P5/P7/P8 still use `_illustration_kit`.

## Why it is split this way

Renders are ~1 minute a frame on this machine (CPU Cycles, 12 threads — no GPU is exposed to
Cycles here). Baking the labels into the render would mean re-rendering every time a word
changes. So the render is hardware only, and the labels go on afterwards as SVG text: crisp at
any print size, and a wording change costs a re-compose, not a re-render.

## Install

Blender is **not** installed system-wide — chocolatey needs admin and was denied. It lives as a
portable build at:

    C:\Users\Yon\tools\blender-4.5.12-windows-x64\blender.exe

Nothing else on the machine was touched. To move or upgrade it, drop a new portable zip there and
update `BLENDER` in `build_p4.sh`.

## Run

    # one frame
    blender --background --factory-startup --python _blender/render.py -- s_wiring out.png \
            [--eevee] [--samples 96] [--res 1800x1350]

    # labels on top
    node _blender/compose.js out.png _blender/callouts/s_wiring.json final.svg

    # everything
    bash _blender/build_p4.sh

`--eevee` is the fast preview (seconds); Cycles is the deliverable.

## Files

| file | what it is |
|---|---|
| `lib.py` | units, primitives (`box` `cyl` `prism` `tube` `torus`), materials, studio lighting, camera, anchors |
| `p4_car.py` | the car itself, at the same millimetres `parts.py` and the chassis template use |
| `scenes_p4.py` | one `s_*` function per step: what is in frame, where the camera is, which anchors |
| `render.py` | CLI entry; writes `<name>.png` plus `<name>.anchors.json` |
| `compose.js` | render + anchors + callouts → one self-contained SVG |
| `callouts/*.json` | the Hebrew for each figure, keyed by anchor name |
| `onwhite.py` | flatten a transparent render onto white, for eyeballing |

## Anchors

A scene registers named 3-D points in millimetres:

    L.anchor('driver', (DRV_X + 22, DRV_Y + 22, PLATE_T + 16))

`render.py` projects them through the camera and writes pixel coordinates next to the PNG.
`compose.js` then puts a label on a real part without anyone hand-guessing image coordinates —
and when a camera angle changes, the labels follow it for free.

## Things that bit, so they do not bite again

- **A bench and `L.ground()` must not coexist.** They end up coplanar, the shadow catcher wins the
  z-fight, and you get a black bench-shaped hole. Scenes with `_bench()` add no ground.
- **Blanket smooth shading melts cylinders.** Smoothing every polygon rounds a cylinder's end caps
  into its wall and wheels turn into blobs. `_finish` uses auto-smooth with a 35° split instead.
- **Area lights are in watts.** At 0.3–0.5 m from a 250 mm object, 15–25 W is a lit scene; the
  first pass used 260 W and everything clipped to white paper.
- **A wheel rim must be smaller than the tyre's inner radius.** Model it larger and it swallows the
  tyre; the wheel reads as a featureless lump.
- **Transmission needs Cycles.** EEVEE wants per-material `use_screen_refraction`, which `mat()`
  sets, but the polygal only really reads as twin-wall under Cycles.

## Not chosen

`_render3d/` holds a working three.js/WebGL alternative (hardware-accelerated, seconds per frame,
no install). It was built to compare against Blender and lost on material quality. Kept as a
fallback if Cycles ever proves too slow to iterate with.
