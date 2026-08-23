"""render.py — CLI entry for the Blender pipeline.

  blender --background --factory-startup --python _blender/render.py -- <scene> <out.png> [opts]

Options after the scene name:
  --eevee            fast preview instead of Cycles
  --samples N        Cycles samples (default 128)
  --res WxH          output resolution (default 1800x1350)

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
import p4_car
import scenes_p4

for mod in (L, p4_car, scenes_p4):
    importlib.reload(mod)

L.reset()
L.ANCHORS.clear()
p4_car.M = None                          # materials are per-file, so rebuild them
fn = getattr(scenes_p4, scene_name, None)
if fn is None:
    print('no such scene:', scene_name)
    print('available:', ', '.join(sorted(n for n in dir(scenes_p4) if n.startswith('s_'))))
    sys.exit(2)

fn()
L.configure(engine=engine, samples=samples, res=res)
os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
L.render(out_path)
print('RENDERED', out_path)
