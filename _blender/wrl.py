"""wrl.py — read the CAD meshes KiCad publishes for real components.

The parts in this pipeline were modelled from boxes and cylinders, which is why a connector reads
as a block with a hole rather than as a connector. KiCad's packages3D library ships CAD-derived
VRML for thousands of real packages — proper lead forming on a DIP, the shell and tongue of a
USB-B, the moulded body of a screw terminal. Blender 4.5 as a Python module has no VRML importer,
but the subset KiCad writes is small: Shape { appearance Material { diffuseColor } geometry
IndexedFaceSet { coord Coordinate { point [...] } coordIndex [...] } }.

Units: KiCad exports at 1 unit = 2.54 mm. Rather than trust that, `load` takes the part's real
size in millimetres and scales the mesh to match, which also catches a model exported at a
different convention.
"""
import re
import bpy
import bmesh
from lib import MM, mat

_SHAPE = re.compile(r'Shape\s*\{(.*?)\n\s*\}\s*(?=\n)', re.S)
_DIFF = re.compile(r'diffuseColor\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)')
_SPEC = re.compile(r'specularColor\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)')
_SHIN = re.compile(r'shininess\s+([\d.eE+-]+)')
_TRAN = re.compile(r'transparency\s+([\d.eE+-]+)')
_PTS = re.compile(r'point\s*\[(.*?)\]', re.S)
_IDX = re.compile(r'coordIndex\s*\[(.*?)\]', re.S)
_NUM = re.compile(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?')


def _defs(text):
    """Collect every `DEF <name> Material { ... }` so a later `material USE <name>` resolves.

    KiCad writes each colour once and references it from every shape that uses it. Reading only
    inline diffuseColor meant most shapes fell through to a default grey, which is why an
    imported part arrived uniformly white instead of black body / gold pin / steel can.
    """
    out = {}
    for m in re.finditer(r'DEF\s+([A-Za-z0-9_\-]+)\s+Material\s*\{', text):
        i = text.index('{', m.start()); depth = 0
        for j in range(i, len(text)):
            if text[j] == '{': depth += 1
            elif text[j] == '}':
                depth -= 1
                if depth == 0: break
        body = text[i:j]
        d = _DIFF.search(body); sp = _SPEC.search(body)
        sh = _SHIN.search(body); tr = _TRAN.search(body)
        out[m.group(1)] = {
            'diffuse': tuple(float(x) for x in d.groups()) if d else (0.6, 0.6, 0.6),
            'specular': tuple(float(x) for x in sp.groups()) if sp else (0.1, 0.1, 0.1),
            'shininess': float(sh.group(1)) if sh else 0.2,
            'transparency': float(tr.group(1)) if tr else 0.0,
        }
    return out


def _shapes(text):
    """Yield (points, faces, material-dict) for each Shape block in a KiCad VRML file."""
    defs = _defs(text)
    for m in re.finditer(r'Shape\s*\{', text):
        # walk braces to find this Shape's extent
        i = text.index('{', m.start()); depth = 0
        for j in range(i, len(text)):
            if text[j] == '{': depth += 1
            elif text[j] == '}':
                depth -= 1
                if depth == 0: break
        body = text[i:j]
        pm, im = _PTS.search(body), _IDX.search(body)
        if not pm or not im:
            continue
        nums = [float(v) for v in _NUM.findall(pm.group(1))]
        pts = [tuple(nums[k:k+3]) for k in range(0, len(nums) - 2, 3)]
        idx = [int(v) for v in _NUM.findall(im.group(1))]
        faces, cur = [], []
        for v in idx:
            if v == -1:
                if len(cur) >= 3: faces.append(tuple(cur))
                cur = []
            else:
                cur.append(v)
        if len(cur) >= 3: faces.append(tuple(cur))
        use = re.search(r'material\s+USE\s+([A-Za-z0-9_\-]+)', body)
        if use and use.group(1) in defs:
            yield pts, faces, defs[use.group(1)]
            continue
        d = _DIFF.search(body); s = _SPEC.search(body)
        sh = _SHIN.search(body); tr = _TRAN.search(body)
        yield pts, faces, {
            'diffuse': tuple(float(x) for x in d.groups()) if d else (0.6, 0.6, 0.6),
            'specular': tuple(float(x) for x in s.groups()) if s else (0.1, 0.1, 0.1),
            'shininess': float(sh.group(1)) if sh else 0.2,
            'transparency': float(tr.group(1)) if tr else 0.0,
        }


def load(path, x, y, z, size_mm=None, rot=(0, 0, 0), name='part', tint=None, recolour=None,
         z_ref='origin'):
    """Build a KiCad VRML part at (x, y, z) in millimetres.

    size_mm: the part's real (length, width) in mm. The mesh is uniformly scaled so its footprint
    matches — KiCad's own unit convention is then irrelevant, and a model exported at the wrong
    scale is corrected rather than silently shipped at the wrong size.
    """
    import math
    from mathutils import Vector
    text = open(path, 'r', errors='replace').read()
    objs, allpts = [], []
    for k, (pts, faces, m) in enumerate(_shapes(text)):
        if not pts or not faces:
            continue
        me = bpy.data.meshes.new(f'{name}_{k}')
        bm = bmesh.new()
        vs = [bm.verts.new(p) for p in pts]
        bm.verts.ensure_lookup_table()
        for f in faces:
            try: bm.faces.new([vs[i] for i in f])
            except Exception: pass
        bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(f'{name}_{k}', me)
        bpy.context.collection.objects.link(ob)
        base = m['diffuse']
        if recolour:
            # recolour maps a role to a colour: 'dark' for the moulded body, 'metal' for pins and
            # cans. The role is read off the KiCad material's own brightness, which separates a
            # black nylon body from a plated contact reliably across every package in the library.
            lum = sum(base) / 3.0
            key = 'dark' if lum < 0.30 else ('metal' if max(m['specular']) > 0.45 else 'light')
            base = recolour.get(key, base)
        if tint:
            base = tint
        rough = max(0.12, 1.0 - min(1.0, m['shininess'] * 1.6))
        metal = 0.85 if (max(m['specular']) > 0.55 and sum(base) / 3 > 0.35) else 0.0
        ob.data.materials.append(mat(f'wrl_{name}_{k}', base, rough=rough, metal=metal))
        objs.append(ob); allpts.extend(pts)

    if not objs:
        raise ValueError('no geometry in ' + path)

    xs = [p[0] for p in allpts]; ys = [p[1] for p in allpts]; zs = [p[2] for p in allpts]
    span = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
    s = 2.54                                        # KiCad's own convention, as a default
    if size_mm:
        want = max(size_mm); have = max(span[0], span[1])
        if have > 1e-9: s = want / have
    # KiCad authors every packages3D model with z = 0 AT THE PCB SURFACE, so a through-hole
    # part's solder tails live at negative z. Referencing the bbox bottom therefore lifted every
    # such part clear of the board by its own tail length: 3 mm on a pin header, which turned a
    # 15-way strip into a bed of nails standing 11.5 mm proud, and floated the DIP-28 off the
    # Uno. Referencing the model origin puts the body on the board and the tails inside it.
    cz = 0.0 if z_ref == 'origin' else min(zs)
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2

    g = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(g)
    for ob in objs:
        ob.parent = g
        ob.location = (-cx * s * MM, -cy * s * MM, -cz * s * MM)
        ob.scale = (s * MM, s * MM, s * MM)
    g.location = (x * MM, y * MM, z * MM)
    g.rotation_euler = tuple(math.radians(a) for a in rot)
    return [g] + objs
