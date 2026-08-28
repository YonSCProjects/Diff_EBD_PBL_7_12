"""render.py — CLI entry for the Blender pipeline.

  blender --background --factory-startup --python _blender/render.py -- <scene> <out.png> [opts]

Options after the scene name:
  --eevee            fast preview instead of Cycles
  --samples N        Cycles samples (default 128)
  --res WxH          output resolution (default 1800x1350)
  --no-ink           skip the Freestyle contour pass

Scenes live in scenes_p4.py. Each returns nothing; it just builds into the current scene.
"""
import os
import sys
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
if len(argv) < 2:
    print('usage: ... -- <scene> <out.png> [--eevee] [--samples N] [--res WxH]')
    sys.exit(2)

scene_name, out_path = argv[0], argv[1]
engine = 'BLENDER_EEVEE_NEXT' if '--eevee' in argv else 'CYCLES'
samples = 128
res = (1800, 1350)
if '--samples' in argv:
    samples = int(argv[argv.index('--samples') + 1])
if '--res' in argv:
    w, h = argv[argv.index('--res') + 1].lower().split('x')
    res = (int(w), int(h))

import lib as L
import quality
import p4_car
import p8_drone
import hand
import tools
import props
import scenes_p4
import scenes_p4_m3
import scenes_p5
import scenes_p7
import scenes_p8

SCENE_MODULES = (scenes_p4, scenes_p4_m3, scenes_p5, scenes_p7, scenes_p8)

for mod in (L, quality, p4_car, p8_drone, hand, tools, props) + SCENE_MODULES:
    importlib.reload(mod)

L.reset()
L.ANCHORS.clear()
p4_car.M = None                          # materials are per-file, so rebuild them
p8_drone.reset()
hand.reset()
tools.reset()
props.reset()
fn = None
for mod in SCENE_MODULES:
    fn = getattr(mod, scene_name, None)
    if fn is not None:
        break
if fn is None:
    print('no such scene:', scene_name)
    names = [n for mod in SCENE_MODULES for n in dir(mod) if n.startswith('s_')]
    print('available:', ', '.join(sorted(set(names))))
    sys.exit(2)

# configure BEFORE the scene builds: camera_fit reads the render resolution to work out the
# frame's aspect, and with Blender's 1920x1080 default still in place it framed for the wrong
# shape and pushed the camera back
L.configure(engine=engine, samples=samples, res=res)
fn()

# The scene builds its own three-light rig and heavy ink because that is what a diagram needs.
# These figures are meant to show a student the part in their hand, so the shading is swapped for
# a product-render setup after the geometry is in place: a gradient environment instead of a flat
# grey one, a softbox rig, a micro-surface on every opaque material, and a light silhouette-only
# ink line in place of the uniform heavy outline. Pass --diagram to keep the original look.
if '--diagram' not in argv:
    quality.apply(level=os.environ.get('QLEVEL', 'product'))
# quality.apply() at 'product'/'photo' already installed the light, silhouette-only ink.
# The legacy pass below runs AFTER it and replaces the whole lineset, so it must be skipped
# whenever quality owns the ink -- otherwise every figure gets a 2.4 px crease+boundary
# outline regardless of what quality.ink() asked for. That was the heavy 'sticker' edge.
_quality_owns_ink = ('--diagram' not in argv) and os.environ.get('QLEVEL', 'product') in ('product', 'photo')
if '--no-ink' not in argv and not _quality_owns_ink:
    # the contour pass is what makes these read as technical illustrations rather than
    # soft product shots; scale the line with the frame so it stays the same visual weight
    L.outlines(thickness=max(1.4, res[0] / 700.0))
os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
L.render(out_path)
print('RENDERED', out_path)
