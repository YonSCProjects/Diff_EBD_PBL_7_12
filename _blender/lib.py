"""lib.py — shared Blender helpers: units, primitives, materials, lighting, camera, output.

Everything here works in millimetres and converts once, so the model code can quote the same
numbers the chassis template and parts.py use.

Run through render.py, never on its own.
"""
import math
import os
import bpy
from mathutils import Vector, Matrix

MM = 0.001                      # model mm -> Blender metres

# Named 3-D points the annotation layer hangs its callouts on. The scene registers them in
# millimetres; render() projects them to pixel coordinates and writes them beside the PNG, so the
# SVG compositor can put a label on a real part without anyone guessing at image coordinates.
ANCHORS = {}


def anchor(name, xyz_mm):
    ANCHORS[name] = tuple(xyz_mm)
    return xyz_mm


# ---------------------------------------------------------------- scene setup
def reset():
    """Empty the file: no default cube, camera or lamp."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    sc.unit_settings.length_unit = 'MILLIMETERS'
    return sc


def outlines(thickness=1.5, colour=(0, 0, 0), crease_angle=118.0, on=True):
    """Freestyle contour lines — what turns a soft product render into a technical illustration.

    A raytraced image already hides what should be hidden, but without an outline every part
    dissolves into its neighbour wherever their tones are close: a light plate against a light
    bench, a grey motor can against a grey rim. An ink line drawn exactly on the true silhouette,
    border and crease edges is what makes each part read as a separate object.

    Blender derives these from the geometry itself, so unlike a painter's-algorithm outline they
    are guaranteed to sit on real boundaries and only there.
    """
    sc = bpy.context.scene
    sc.render.use_freestyle = on
    if not on:
        return
    sc.render.line_thickness_mode = 'ABSOLUTE'
    sc.render.line_thickness = thickness
    for vl in sc.view_layers:
        vl.use_freestyle = True
        fs = vl.freestyle_settings
        fs.crease_angle = math.radians(crease_angle)
        while fs.linesets:
            fs.linesets.remove(fs.linesets[0])
        ls = fs.linesets.new('ink')
        ls.select_silhouette = True      # the outer edge of every object
        ls.select_border = True          # open mesh boundaries
        ls.select_crease = True          # hard folds, e.g. a box corner
        ls.select_edge_mark = False
        ls.select_material_boundary = True   # where one material meets another
        ls.linestyle.color = colour
        ls.linestyle.thickness = thickness
        ls.linestyle.caps = 'ROUND'


def configure(engine='CYCLES', samples=128, res=(1800, 1350), transparent=True, denoise=True):
    sc = bpy.context.scene
    sc.render.engine = engine
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = transparent
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'
    sc.render.image_settings.compression = 20
    names = [v.name for v in sc.view_settings.bl_rna.properties['view_transform'].enum_items]
    sc.view_settings.view_transform = next((n for n in ('AgX', 'Filmic', 'Standard') if n in names),
                                           'Standard')
    sc.view_settings.exposure = -0.45
    sc.view_settings.look = 'None'
    if engine == 'CYCLES':
        sc.cycles.samples = samples
        sc.cycles.use_denoising = denoise
        sc.cycles.max_bounces = 8
        sc.cycles.transmission_bounces = 8
        sc.cycles.caustics_reflective = False
        sc.cycles.caustics_refractive = False
        # use whatever compute the machine has; fall back to CPU silently
        try:
            prefs = bpy.context.preferences.addons['cycles'].preferences
            for kind in ('OPTIX', 'CUDA', 'HIP', 'ONEAPI', 'METAL'):
                prefs.compute_device_type = kind
                prefs.get_devices()
                if any(d.type == kind for d in prefs.devices):
                    for d in prefs.devices:
                        d.use = (d.type == kind)
                    sc.cycles.device = 'GPU'
                    break
            else:
                sc.cycles.device = 'CPU'
        except Exception:
            sc.cycles.device = 'CPU'
    else:
        sc.eevee.taa_render_samples = samples
        for attr, val in (('use_gtao', True), ('use_ssr', True), ('use_ssr_refraction', True),
                          ('use_soft_shadows', True)):
            if hasattr(sc.eevee, attr):
                setattr(sc.eevee, attr, val)
    return sc


# ---------------------------------------------------------------- materials
def mat(name, base, rough=0.5, metal=0.0, clearcoat=0.0, cc_rough=0.1,
        transmission=0.0, ior=1.5, emission=None, emission_strength=1.0, alpha=1.0):
    """A Principled BSDF material. base is (r, g, b) in 0..1 linear-ish sRGB."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']

    def put(key, value):
        if key in b.inputs:
            b.inputs[key].default_value = value

    put('Base Color', (*base, 1.0))
    put('Roughness', rough)
    put('Metallic', metal)
    put('IOR', ior)
    put('Alpha', alpha)
    # Blender 4.x renamed the coat and transmission sockets
    for key in ('Coat Weight', 'Clearcoat'):
        put(key, clearcoat)
    for key in ('Coat Roughness', 'Clearcoat Roughness'):
        put(key, cc_rough)
    for key in ('Transmission Weight', 'Transmission'):
        put(key, transmission)
    if emission:
        for key in ('Emission Color', 'Emission'):
            put(key, (*emission, 1.0))
        put('Emission Strength', emission_strength)
    if transmission > 0:
        for attr, val in (('use_screen_refraction', True), ('use_raytrace_refraction', True),
                          ('refraction_depth', 0.002)):
            if hasattr(m, attr):
                setattr(m, attr, val)
    if alpha < 1.0 and hasattr(m, 'blend_method'):
        m.blend_method = 'BLEND'
    return m


def hexcol(h):
    """'#rrggbb' -> linear RGB, so the renders match the palette the cards already use."""
    h = h.lstrip('#')
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb)


# ---------------------------------------------------------------- primitives
def _bake(ob, matrix):
    """Apply a transform to the MESH DATA. bpy.ops.object.transform_apply() acts on whatever is
    SELECTED, and objects created with bpy.data.objects.new() are not selected — so the operator
    silently transformed some other object and this one kept its axis unrotated. Baking the
    matrix into the data has no such dependency."""
    ob.data.transform(matrix)
    ob.rotation_euler = (0, 0, 0)
    ob.scale = (1, 1, 1)
    return ob


def _finish(ob, m, shade_smooth=False, bevel=0.0):
    if m:
        ob.data.materials.append(m)
    if bevel > 0:
        b = ob.modifiers.new('bevel', 'BEVEL')
        b.width = bevel * MM
        b.segments = 3
        b.limit_method = 'ANGLE'
        b.angle_limit = math.radians(40)
    if shade_smooth:
        # blanket smoothing rounds a cylinder's end caps into its wall and the part reads as
        # a blob; auto-smooth keeps any edge sharper than the angle crisp
        for p in ob.data.polygons:
            p.use_smooth = True
        try:
            bpy.context.view_layer.objects.active = ob
            bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
        except Exception:
            ob.data.use_auto_smooth = True
            ob.data.auto_smooth_angle = math.radians(35)
    return ob


def box(x, y, z, w, d, h, m=None, bevel=0.35, name='box'):
    """Axis-aligned box with its MIN corner at (x, y, z) — same convention as the SVG kit."""
    bpy.ops.mesh.primitive_cube_add(size=1)
    ob = bpy.context.object
    ob.name = name
    _bake(ob, Matrix.Diagonal((w * MM, d * MM, h * MM, 1.0)))
    ob.location = ((x + w / 2) * MM, (y + d / 2) * MM, (z + h / 2) * MM)
    return _finish(ob, m, bevel=bevel)


def cyl(x, y, z, r, h, m=None, axis='z', seg=64, name='cyl', bevel=0.0):
    """Cylinder with its base centre at (x, y, z), running along `axis`."""
    bpy.ops.mesh.primitive_cylinder_add(vertices=seg, radius=r * MM, depth=h * MM)
    ob = bpy.context.object
    ob.name = name
    if axis == 'x':
        _bake(ob, Matrix.Rotation(math.radians(90), 4, 'Y'))
        ob.location = ((x + h / 2) * MM, y * MM, z * MM)
    elif axis == 'y':
        _bake(ob, Matrix.Rotation(math.radians(90), 4, 'X'))
        ob.location = (x * MM, (y + h / 2) * MM, z * MM)
    else:
        ob.location = (x * MM, y * MM, (z + h / 2) * MM)
    return _finish(ob, m, shade_smooth=True, bevel=bevel)


def prism_xz(pts_xz, x, y, z, depth, m=None, name='prism_xz', bevel=0.0):
    """Extrude a SIDE profile across the object's width. `pts_xz` is the silhouette you would
    draw looking at the tool from the side, in (along, up) millimetres; it sweeps `depth` in y.

    Most hand tools are shaped in side view — a glue gun's pistol grip, a knife's taper — so
    extruding their outline upward (as prism() does) gives the right silhouette in the wrong plane
    and the tool comes out as a slab.
    """
    import bmesh
    me = bpy.data.meshes.new(name)
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    bm = bmesh.new()
    verts = [bm.verts.new((p[0] * MM, 0.0, p[1] * MM)) for p in pts_xz]
    face = bm.faces.new(verts)
    r = bmesh.ops.extrude_face_region(bm, geom=[face])
    moved = [v for v in r['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, depth * MM, 0), verts=moved)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    bpy.context.view_layer.objects.active = ob
    ob.location = (x * MM, y * MM, z * MM)
    return _finish(ob, m, bevel=bevel)


def revolve(profile, x, y, z, m=None, axis='z', seg=64, name='revolve', smooth=True):
    """Spin a 2-D profile into a solid of revolution — the one operation that makes a hand tool
    look like a hand tool. `profile` is [(radius, height), ...] in mm, measured from the object's
    base at (x, y, z) and running up its axis. Stacking cylinders cannot give you the taper of an
    iron's handle or the swell of a glue-gun nozzle; this can.
    """
    import bmesh
    me = bpy.data.meshes.new(name)
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    bm = bmesh.new()
    verts = [bm.verts.new((r * MM, 0.0, h * MM)) for r, h in profile]
    edges = [bm.edges.new((verts[i], verts[i + 1])) for i in range(len(verts) - 1)]
    bmesh.ops.spin(bm, geom=verts + edges, angle=math.radians(360), steps=seg,
                   axis=(0, 0, 1), cent=(0, 0, 0))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    bpy.context.view_layer.objects.active = ob
    if axis == 'x':
        _bake(ob, Matrix.Rotation(math.radians(90), 4, 'Y'))
    elif axis == 'y':
        _bake(ob, Matrix.Rotation(math.radians(-90), 4, 'X'))
    ob.location = (x * MM, y * MM, z * MM)
    return _finish(ob, m, shade_smooth=smooth)


def helix(x, y, z, r, turns, height, wire_r, m=None, axis='z', name='helix', steps=24):
    """A coiled spring — the iron stand's holder, or wire wound on a reel.

    `axis` is the coil's own axis. It used to be accepted and silently ignored, which meant a
    coil asked for around Y came out around Z and lay across whatever it was meant to wind on."""
    pts = []
    n = int(turns * steps)
    for i in range(n + 1):
        a = 2 * math.pi * (i / steps)
        c, s = math.cos(a) * r, math.sin(a) * r
        run = height * (i / max(1, n))
        if axis == 'z':
            pts.append((x + c, y + s, z + run))
        elif axis == 'y':
            pts.append((x + c, y + run, z + s))
        else:                                   # 'x'
            pts.append((x + run, y + c, z + s))
    return tube(pts, wire_r, m, name=name, seg=10)


def prism(pts2d, z, h, m=None, name='prism', bevel=0.0):
    """Extrude an xy outline upward from z. pts2d is a list of (x, y) in mm."""
    import bmesh
    me = bpy.data.meshes.new(name)
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    bm = bmesh.new()
    verts = [bm.verts.new((p[0] * MM, p[1] * MM, z * MM)) for p in pts2d]
    face = bm.faces.new(verts)
    bmesh.ops.translate(bm, vec=(0, 0, 0), verts=verts)
    r = bmesh.ops.extrude_face_region(bm, geom=[face])
    moved = [v for v in r['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, h * MM), verts=moved)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    bpy.context.view_layer.objects.active = ob
    return _finish(ob, m, bevel=bevel)


def tube(pts3, r, m=None, name='tube', seg=14):
    """A wire through 3-D waypoints in mm, as a real swept curve."""
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.resolution_u = 8
    cu.bevel_depth = r * MM
    cu.bevel_resolution = seg // 2
    cu.use_fill_caps = True
    sp = cu.splines.new('BEZIER')
    sp.bezier_points.add(len(pts3) - 1)
    for bp, p in zip(sp.bezier_points, pts3):
        bp.co = (p[0] * MM, p[1] * MM, p[2] * MM)
        bp.handle_left_type = bp.handle_right_type = 'AUTO'
    ob = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(ob)
    if m:
        ob.data.materials.append(m)
    return ob


def torus(x, y, z, r_major, r_minor, m=None, name='torus'):
    bpy.ops.mesh.primitive_torus_add(major_radius=r_major * MM, minor_radius=r_minor * MM,
                                     major_segments=56, minor_segments=16,
                                     location=(x * MM, y * MM, z * MM))
    ob = bpy.context.object
    ob.name = name
    return _finish(ob, m, shade_smooth=True)


# ---------------------------------------------------------------- studio
def studio(strength=1.0, warm=False):
    """A soft three-light studio plus a neutral world, so parts read without hard speculars."""
    w = bpy.context.scene.world or bpy.data.worlds.new('World')
    bpy.context.scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes['Background']
    bg.inputs[0].default_value = (0.62, 0.65, 0.70, 1.0)
    bg.inputs[1].default_value = 0.46 * strength

    def area(name, loc, rot, size, energy, colour=(1, 1, 1)):
        d = bpy.data.lights.new(name, 'AREA')
        d.shape = 'RECTANGLE'
        d.size, d.size_y = size
        d.energy = energy
        d.color = colour
        ob = bpy.data.objects.new(name, d)
        ob.location = [c * MM for c in loc]
        ob.rotation_euler = [math.radians(a) for a in rot]
        bpy.context.collection.objects.link(ob)
        return ob

    area('key', (-120, -260, 420), (34, 0, -22), (0.62, 0.48), 11 * strength,
         (1.0, 0.97, 0.93) if warm else (1, 1, 1))
    area('fill', (360, -180, 250), (58, 0, 58), (0.7, 0.5), 6 * strength, (0.92, 0.95, 1.0))
    area('rim', (240, 340, 300), (-46, 0, 150), (0.5, 0.4), 9 * strength)


def ground(z=0.0, size=1400, shadow_only=True, colour='#f2efe9'):
    """A floor. shadow_only keeps the page white and catches only the contact shadow."""
    bpy.ops.mesh.primitive_plane_add(size=size * MM, location=(140 * MM, 110 * MM, z * MM))
    ob = bpy.context.object
    ob.name = 'ground'
    if shadow_only:
        ob.is_shadow_catcher = True
    else:
        ob.data.materials.append(mat('ground', hexcol(colour), rough=0.85))
    return ob


def camera(target, distance, azimuth=38.0, elevation=27.0, lens=58.0, shift=(0.0, 0.0)):
    """Put a camera `distance` mm from `target`, orbiting at the given angles."""
    tx, ty, tz = [c * MM for c in target]
    a, e = math.radians(azimuth), math.radians(elevation)
    d = distance * MM
    loc = Vector((tx + d * math.cos(e) * math.cos(a),
                  ty - d * math.cos(e) * math.sin(a),
                  tz + d * math.sin(e)))
    cam = bpy.data.cameras.new('cam')
    cam.lens = lens
    cam.shift_x, cam.shift_y = shift
    ob = bpy.data.objects.new('cam', cam)
    ob.location = loc
    direction = Vector((tx, ty, tz)) - loc
    ob.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.collection.objects.link(ob)
    bpy.context.scene.camera = ob
    return ob


def project_anchors():
    """World mm -> pixel coordinates in the rendered image, y measured from the top."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    cam = sc.camera
    w = int(sc.render.resolution_x * sc.render.resolution_percentage / 100)
    h = int(sc.render.resolution_y * sc.render.resolution_percentage / 100)
    out = {}
    for name, (x, y, z) in ANCHORS.items():
        v = world_to_camera_view(sc, cam, Vector((x * MM, y * MM, z * MM)))
        out[name] = {'x': round(v.x * w, 1), 'y': round((1.0 - v.y) * h, 1),
                     'depth': round(v.z, 4), 'onscreen': 0.0 <= v.x <= 1.0 and 0.0 <= v.y <= 1.0}
    return {'width': w, 'height': h, 'anchors': out}


def render(path):
    import json
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    meta = project_anchors()
    with open(os.path.splitext(path)[0] + '.anchors.json', 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    return path


def ribbon(pts2d, width, z, m=None, name='ribbon', closed=True, thickness=0.3):
    """A flat strip of constant width following a path — a loop of floor tape, a painted lane.

    Built as ONE mesh on purpose. Laid out as a row of little boxes instead, the Freestyle pass
    inks every box separately and a smooth loop of tape comes out looking like a bicycle chain.
    One mesh gives exactly two ink contours: the inner edge and the outer edge.
    """
    import bmesh
    n = len(pts2d)
    me = bpy.data.meshes.new(name)
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    bm = bmesh.new()
    inner, outer = [], []
    for i, (x, y) in enumerate(pts2d):
        if closed:
            px, py = pts2d[(i - 1) % n]
            nx, ny = pts2d[(i + 1) % n]
        else:
            px, py = pts2d[max(i - 1, 0)]
            nx, ny = pts2d[min(i + 1, n - 1)]
        tx, ty = nx - px, ny - py
        L_ = math.hypot(tx, ty) or 1.0
        # the normal to the local tangent; offsetting both ways keeps the width constant
        ux, uy = -ty / L_, tx / L_
        h = width / 2.0
        inner.append(bm.verts.new(((x - ux * h) * MM, (y - uy * h) * MM, z * MM)))
        outer.append(bm.verts.new(((x + ux * h) * MM, (y + uy * h) * MM, z * MM)))
    last = n if closed else n - 1
    for i in range(last):
        j = (i + 1) % n
        bm.faces.new((inner[i], outer[i], outer[j], inner[j]))
    if thickness:
        bmesh.ops.solidify(bm, geom=bm.faces[:] + bm.edges[:] + bm.verts[:],
                           thickness=-thickness * MM)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    bpy.context.view_layer.objects.active = ob
    return _finish(ob, m, bevel=0.0)


def ellipse_pts(cx, cy, rx, ry, n=96, rot=0.0):
    """Points round an ellipse — the path a tape loop follows."""
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = rx * math.cos(a), ry * math.sin(a)
        out.append((cx + x * c - y * s, cy + x * s + y * c))
    return out


def camera_fit(azimuth=44.0, elevation=32.0, lens=56.0, margin=0.075, target=None,
               subject=None, extra=(), lo=120.0, hi=4000.0, shift=(0.0, 0.0)):
    """Place the camera far enough back that EVERY registered anchor lands inside the frame.

    Hand-picked distances are the reason callouts kept getting dropped: compose.js refuses to
    draw a label whose anchor is off-screen, so a bench prop that carries the whole point of a
    card — the closed prop box, the zipped LiPo bag — silently lost its Hebrew. The anchors are
    exactly the things that must be visible, so they are the right thing to frame on.

    `margin` is the fraction of the frame kept clear at each edge for the label boxes.
    `extra` takes further (x, y, z) points in mm that must also be in view.
    """
    pts = [tuple(v) for v in ANCHORS.values()] + [tuple(p) for p in extra]
    if not pts:
        return camera(target or (0, 0, 0), 600, azimuth, elevation, lens, shift)
    xs, ys, zs = zip(*pts)
    mid = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, (min(zs) + max(zs)) / 2)
    if target is None and subject is not None:
        # Aiming straight at the subject wastes half the frame whenever the subject sits at the
        # edge of the content — a front motor, say, with the rest of the aircraft behind it: the
        # fit then has to push back far enough to hold a point a whole wheelbase off-axis.
        # Aiming halfway between the subject and the content's centre keeps the subject
        # prominent without paying for that.
        sp = ANCHORS[subject] if isinstance(subject, str) else tuple(subject)
        target = tuple((a + b) / 2 for a, b in zip(sp, mid))
    if target is None:
        target = mid

    # The projection is worked out here rather than through world_to_camera_view on a temporary
    # camera object. A freshly created object's matrix_world lags the depsgraph, so the search
    # kept measuring the PREVIOUS candidate and converged on a distance far wider than needed —
    # which is exactly how a 100 mm drone ended up as a quarter of the frame.
    sc = bpy.context.scene
    rx, ry = sc.render.resolution_x, sc.render.resolution_y
    tan_x = 18.0 / lens                       # Blender's 36 mm sensor, fit to the long side
    tan_y = tan_x * (ry / rx) if rx >= ry else tan_x
    if rx < ry:
        tan_x = tan_y * (rx / ry)
    tgt = Vector((target[0] * MM, target[1] * MM, target[2] * MM))
    a, e = math.radians(azimuth), math.radians(elevation)
    unit = Vector((math.cos(e) * math.cos(a), -math.cos(e) * math.sin(a), math.sin(e)))
    lim = 1.0 - 2.0 * margin

    def fits(d):
        loc = tgt + unit * (d * MM)
        rot = (tgt - loc).to_track_quat('-Z', 'Y').to_matrix().to_4x4()
        inv = (Matrix.Translation(loc) @ rot).inverted()
        for p in pts:
            v = inv @ Vector((p[0] * MM, p[1] * MM, p[2] * MM))
            depth = -v.z
            if depth <= 1e-6:
                return False
            if abs(v.x) > depth * tan_x * lim or abs(v.y) > depth * tan_y * lim:
                return False
        return True

    # 26 halvings put the answer well under a millimetre, and each step is a handful of
    # matrix multiplies — nothing next to a render
    if not fits(hi):
        return camera(target, hi, azimuth, elevation, lens, shift)
    best = hi
    for _ in range(26):
        mid = (lo + best) / 2
        if fits(mid):
            best = mid
        else:
            lo = mid
    return camera(target, best, azimuth, elevation, lens, shift)


def bbox_pts(x0, y0, z0, x1, y1, z1):
    """The eight corners of a box in mm — hand this to camera_fit's `extra` so the whole of a
    subject stays in frame, not just the details that happen to carry a callout."""
    return [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]


def sphere(x, y, z, r, m=None, seg=24, name='sphere'):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r * MM, segments=seg, ring_count=seg // 2,
                                         location=(x * MM, y * MM, z * MM))
    ob = bpy.context.object
    ob.name = name
    return _finish(ob, m, shade_smooth=True)


def capsule(p0, p1, r, m=None, seg=20, name='capsule'):
    """A rounded rod between two 3-D points. Finger bones are capsules; built as bare cylinders
    they end in hard discs and a hand reads as a bundle of pipes."""
    import bmesh
    ax, ay, az = p0
    bx, by, bz = p1
    d = Vector(((bx - ax) * MM, (by - ay) * MM, (bz - az) * MM))
    length = d.length or 1e-6
    me = bpy.data.meshes.new(name)
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r * MM, radius2=r * MM,
                          depth=length,
                          matrix=Matrix.Translation((0, 0, length / 2)))
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=r * MM)
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=r * MM,
                              matrix=Matrix.Translation((0, 0, length)))
    bm.to_mesh(me)
    bm.free()
    ob.location = (ax * MM, ay * MM, az * MM)
    ob.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
    bpy.context.view_layer.objects.active = ob
    return _finish(ob, m, shade_smooth=True)
