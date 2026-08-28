"""quality.py — the shading half of the pipeline, brought up to product-render standard.

The geometry was never the reason the figures read as toys. Three things were:

  * a flat grey world, so every reflective surface reflected the same flat grey and nothing
    looked round or made of anything;
  * materials that were a single base colour with one roughness number, so plastic, painted
    metal and PCB all had the same dead, even sheen;
  * a Freestyle ink line of uniform thickness on every silhouette, crease and material boundary,
    which at 1700 px is a heavy black sticker outline around every object.

None of that is fixed by changing renderer. It is fixed here.
"""
import math
import bpy
from lib import MM


def world_dome(strength=1.0, top='#eef2f7', horizon='#c9ccd2', floor='#8d8f95'):
    """A gradient environment instead of a flat colour.

    A product render gets most of its shape from what the surfaces reflect. Reflecting one
    constant grey is the same as reflecting nothing: edges stop turning, metal reads as grey
    plastic. A bright top, a cooler horizon and a darker floor give every curved surface a
    gradient to run across, which is what makes it look solid.
    """
    w = bpy.context.scene.world or bpy.data.worlds.new('World')
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_WORLD':
            nt.nodes.remove(n)
    out = next(n for n in nt.nodes if n.type == 'OUTPUT_WORLD')

    tex = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    bg = nt.nodes.new('ShaderNodeBackground')
    nt.links.new(tex.outputs['Generated'], sep.inputs['Vector'])
    nt.links.new(sep.outputs['Z'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bg.inputs['Color'])
    nt.links.new(bg.outputs['Background'], out.inputs['Surface'])

    def rgb(h):
        h = h.lstrip('#')
        return tuple((int(h[i:i+2], 16) / 255.0) ** 2.2 for i in (0, 2, 4)) + (1.0,)

    e = ramp.color_ramp.elements
    e[0].position, e[0].color = 0.0, rgb(floor)
    e[1].position, e[1].color = 1.0, rgb(top)
    m = ramp.color_ramp.elements.new(0.52)
    m.color = rgb(horizon)
    bg.inputs[1].default_value = 0.5 * strength
    return w


def softbox(strength=1.0):
    """Key, fill and a low bounce — sized and placed like a tabletop product shoot.

    The key is large and close, which is what gives a soft, wide highlight down a plastic case
    instead of a hot dot. The bounce underneath stops the undersides going to black.
    """
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

    # sizes are up on the originals (a larger source = a softer, wider highlight) but the
    # energies are matched to the old three-light rig, not raised. Brighter is not better.
    area('key',    (-120, -260, 420), (34, 0, -22), (1.05, 0.80), 11 * strength, (1.0, 0.985, 0.96))
    area('fill',   (360, -180, 250),  (58, 0, 58),  (0.95, 0.70), 6 * strength, (0.93, 0.96, 1.0))
    area('rim',    (240, 340, 300),   (-46, 0, 150), (0.62, 0.48), 9 * strength, (0.98, 0.99, 1.0))
    area('bounce', (60, 40, -240),    (180, 0, 0),  (1.5, 1.1),   1.2 * strength, (1.0, 0.98, 0.95))


def dress_materials(bump=0.00018, rough_var=0.06):
    """Give every opaque material a micro-surface and a little roughness variation.

    A single roughness number is what makes a render look like a diagram: real mouldings, paint
    and solder mask all scatter unevenly, and the eye reads that unevenness as material. This
    adds a very fine noise bump and a matching roughness break-up. Glass, emitters and anything
    already transmissive are left alone — they are correct as authored.
    """
    touched = 0
    for m in bpy.data.materials:
        if not m.use_nodes:
            continue
        nt = m.node_tree
        b = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if b is None or any(n.type == 'TEX_NOISE' for n in nt.nodes):
            continue
        trans = b.inputs.get('Transmission Weight') or b.inputs.get('Transmission')
        if trans is not None and trans.default_value > 0.05:
            continue
        emis = b.inputs.get('Emission Strength')
        if emis is not None and emis.default_value > 0.05:
            continue
        # an image-textured face (the silkscreens) keeps its colour; it still gets the surface
        base_linked = b.inputs['Base Color'].is_linked

        coord = nt.nodes.new('ShaderNodeTexCoord')
        noise = nt.nodes.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = 95.0
        noise.inputs['Detail'].default_value = 3.0
        noise.inputs['Roughness'].default_value = 0.62
        nt.links.new(coord.outputs['Object'], noise.inputs['Vector'])

        bmp = nt.nodes.new('ShaderNodeBump')
        bmp.inputs['Strength'].default_value = 0.08
        bmp.inputs['Distance'].default_value = bump
        nt.links.new(noise.outputs['Fac'], bmp.inputs['Height'])
        nt.links.new(bmp.outputs['Normal'], b.inputs['Normal'])

        r0 = b.inputs['Roughness'].default_value
        if not b.inputs['Roughness'].is_linked:
            mixr = nt.nodes.new('ShaderNodeMapRange')
            mixr.inputs['From Min'].default_value = 0.0
            mixr.inputs['From Max'].default_value = 1.0
            mixr.inputs['To Min'].default_value = max(0.03, r0 - rough_var)
            mixr.inputs['To Max'].default_value = min(0.98, r0 + rough_var)
            nt.links.new(noise.outputs['Fac'], mixr.inputs['Value'])
            nt.links.new(mixr.outputs['Result'], b.inputs['Roughness'])

        # a touch of coat on anything glossy reads as moulded plastic rather than paint
        coat = b.inputs.get('Coat Weight')
        if coat is not None and r0 < 0.55 and not base_linked:
            coat.default_value = max(coat.default_value, 0.16)
        touched += 1
    return touched


def ink(thickness=0.80, silhouette_only=True):
    """A lighter, more selective ink line.

    The original pass inked silhouette, border, crease AND material boundary at a uniform
    res/700 px -- 2.4 px at 1700 -- which is a heavy black sticker outline around every object,
    and was by far the biggest single reason these figures read as cartoons rather than as
    hardware. Keeping silhouette and border only, at a third of that weight, still separates a
    pale part from a pale bench without drawing the whole scene twice.

    NOTE for anyone editing render.py: this lineset is installed by quality.apply(), and
    Freestyle keeps only ONE lineset per view layer. Any later call to lib.outlines() replaces
    it wholesale and silently restores the heavy look. render.py guards against exactly that.
    """
    sc = bpy.context.scene
    sc.render.use_freestyle = thickness > 0
    if thickness <= 0:
        return
    sc.render.line_thickness_mode = 'ABSOLUTE'
    sc.render.line_thickness = thickness
    for vl in sc.view_layers:
        vl.use_freestyle = True
        fs = vl.freestyle_settings
        while fs.linesets:
            fs.linesets.remove(fs.linesets[0])
        ls = fs.linesets.new('ink')
        ls.select_silhouette = True
        ls.select_border = True
        ls.select_crease = not silhouette_only
        ls.select_material_boundary = not silhouette_only
        ls.select_edge_mark = False
        ls.linestyle.color = (0.06, 0.07, 0.09)
        ls.linestyle.thickness = thickness
        ls.linestyle.caps = 'ROUND'


def apply(level='product', strength=1.0):
    """Swap the diagram look for a product-render look, after the scene is built.

    level: 'world'  — gradient environment + softbox rig only
           'micro'  — the above plus a micro-surface on every opaque material
           'product'— the above plus a lighter, silhouette-only ink line
           'photo'  — the above with no ink at all
    """
    for ob in list(bpy.data.objects):
        if ob.type == 'LIGHT':
            bpy.data.objects.remove(ob, do_unlink=True)
    world_dome(strength)
    softbox(strength)
    n = dress_materials() if level in ('micro', 'product', 'photo') else 0
    if level in ('world', 'micro'):
        pass                       # keep the original ink so the change is isolated
    else:
        ink(0.0 if level == 'photo' else 0.80, silhouette_only=True)
    sc = bpy.context.scene
    sc.view_settings.exposure = -0.45   # unchanged from the original grade; do not brighten
    if sc.render.engine == 'CYCLES':
        sc.cycles.max_bounces = 12
        sc.cycles.use_denoising = True
    return n
