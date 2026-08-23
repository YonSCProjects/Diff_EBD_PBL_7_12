"""tools.py — the hand tools the Project 4 cards show, modelled properly.

These are the objects a student actually holds, so they carry most of the "this is a real bench"
weight in a figure.

Two shaping rules do most of the work here:
  * anything rotationally symmetric is LATHED (`revolve`) — an iron's handle taper, a nozzle's
    swell, a spool's flange. Stacked cylinders cannot give you those.
  * anything shaped in side view is a SIDE PROFILE swept across its width (`prism_xz`) — a glue
    gun's pistol grip, a knife's nose. Extruding those outlines upward instead gives the right
    silhouette in the wrong plane and the tool comes out a slab.

Real sizes, because a tool at the wrong scale beside a 250 mm chassis reads as a toy:
  soldering iron  ~190 mm overall, 22 mm handle, 4 mm tip
  iron stand      105 x 82 base, coiled holder, sponge tray
  solder spool    72 mm flange, 1 mm wire
  snap-off knife  146 x 25, 18 mm blade leaving the nose at 30 degrees
  glue gun        140 long x 78 tall, 11 mm stick
"""
import math
import lib as L
from lib import MM, box, cyl, prism, prism_xz, tube, torus, revolve, helix, mat, hexcol

_M = None


def materials():
    global _M
    if _M is None:
        _M = dict(
            handle_blue=mat('t_handle_blue', hexcol('#1a3f6e'), rough=0.48, clearcoat=0.12),
            handle_dark=mat('t_handle_dark', hexcol('#1a1d22'), rough=0.54),
            grip=mat('t_grip', hexcol('#a8451a'), rough=0.66),
            chrome=mat('t_chrome', hexcol('#c6cbd2'), rough=0.20, metal=1.0),
            steel=mat('t_steel', hexcol('#9aa1a9'), rough=0.30, metal=1.0),
            blade=mat('t_blade', hexcol('#d7dbe0'), rough=0.14, metal=1.0),
            brass=mat('t_brass', hexcol('#9c6d34'), rough=0.32, metal=1.0),
            tip_hot=mat('t_tip', hexcol('#4a3a2a'), rough=0.44, metal=0.7),
            solder=mat('t_solder', hexcol('#aeb4bb'), rough=0.26, metal=1.0),
            spool=mat('t_spool', hexcol('#2b3038'), rough=0.58),
            cast_iron=mat('t_cast', hexcol('#343940'), rough=0.62, metal=0.3),
            sponge=mat('t_sponge', hexcol('#6ea87a'), rough=0.95),
            cable=mat('t_cable', hexcol('#15181c'), rough=0.64),
            glue_body=mat('t_glue', hexcol('#c25415'), rough=0.52, clearcoat=0.14),
            glue_grey=mat('t_glue_grey', hexcol('#3a4048'), rough=0.52),
            glue_stick=mat('t_stick', hexcol('#eef2f4'), rough=0.25, transmission=0.55, ior=1.46),
            lens=mat('t_lens', hexcol('#8fb6cf'), rough=0.05, transmission=0.82, ior=1.52),
            goggle_frame=mat('t_goggle', hexcol('#16457c'), rough=0.55),
            strap=mat('t_strap', hexcol('#22262b'), rough=0.85),
            shrink=mat('t_shrink', hexcol('#1b2b6b'), rough=0.52),
            mat_dark=mat('t_mat', hexcol('#2f3a44'), rough=0.86),
            paper=mat('t_paper', hexcol('#fffdf7'), rough=0.9),
            copper=mat('t_copper', hexcol('#a3672e'), rough=0.34, metal=1.0),
            laptop_body=mat('t_laptop', hexcol('#7f868e'), rough=0.38, metal=0.55),
            screen=mat('t_screen', hexcol('#0d1520'), rough=0.14,
                       emission=hexcol('#16283a'), emission_strength=0.7),
            riser_box=mat('t_riser', hexcol('#a8916b'), rough=0.84),
            ruler_clear=mat('t_ruler', hexcol('#dfe9ee'), rough=0.12, transmission=0.72, ior=1.49),
            pencil_body=mat('t_pencil', hexcol('#c9a227'), rough=0.44),
            pencil_wood=mat('t_wood', hexcol('#c9a578'), rough=0.72),
            eraser=mat('t_eraser', hexcol('#c98f8f'), rough=0.86),
            sd_handle=mat('t_sd', hexcol('#b02a24'), rough=0.44, clearcoat=0.18),
            sd_grip=mat('t_sdgrip', hexcol('#20242a'), rough=0.7),
            drill_body=mat('t_drill', hexcol('#1c5f9c'), rough=0.48, clearcoat=0.12),
            drill_grey=mat('t_drillg', hexcol('#2b3038'), rough=0.56),
            chuck=mat('t_chuck', hexcol('#42474e'), rough=0.34, metal=0.8),
            ziptie=mat('t_ziptie', hexcol('#e8eaec'), rough=0.42),
            masking=mat('t_masking', hexcol('#d8b874'), rough=0.78),
            bench_hole=mat('t_hole', hexcol('#8a8172'), rough=0.9),
        )
    return _M


def reset():
    global _M
    _M = None


def _group(objs, name):
    import bpy
    g = bpy.data.objects.new(name, None)
    g.empty_display_size = 0.01
    bpy.context.collection.objects.link(g)
    for o in objs:
        if o is not None and o.parent is None:
            o.parent = g
    return g


# ---------------------------------------------------------------- soldering iron
def soldering_iron(x, y, z, ang=0.0, tilt=0.0, cable=True):
    """A pencil iron, tip toward +x. Lathed, so the handle actually tapers and swells."""
    m = materials()
    parts = [
        revolve([(0.35, 0), (1.4, 9), (2.1, 16), (2.4, 24)], 0, 0, 0, m['tip_hot'],
                axis='x', name='iron_tip'),
        revolve([(2.4, 0), (5.0, 4), (5.2, 30), (7.4, 34), (7.2, 42)], 24, 0, 0,
                m['chrome'], axis='x', name='iron_barrel'),
        revolve([(7.2, 0), (10.4, 6), (11.0, 28), (10.2, 58), (10.8, 70),
                 (9.2, 86), (6.0, 94), (5.4, 98)], 66, 0, 0,
                m['handle_blue'], axis='x', name='iron_handle'),
        revolve([(5.4, 0), (4.2, 8), (3.0, 15)], 164, 0, 0, m['handle_dark'],
                axis='x', name='iron_boot'),
    ]
    for i in range(4):                                    # the moulded grip rings
        r = torus(66 + 30 + i * 9, 0, 0, 10.7 - i * 0.14, 0.85, m['handle_dark'], name='iron_ring')
        r.rotation_euler = (0, math.radians(90), 0)
        parts.append(r)
    if cable:
        parts.append(tube([(179, 0, 0), (204, 5, -3), (238, 24, -6), (256, 58, -7)],
                          2.4, m['cable'], name='iron_cable'))
    g = _group(parts, 'iron')
    g.rotation_euler = (0, math.radians(tilt), math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


def iron_stand(x, y, z, ang=0.0):
    """Heavy base, coiled holder on a post, damp sponge in its tray."""
    m = materials()
    parts = [
        box(0, 0, 0, 105, 82, 5, m['cast_iron'], bevel=1.6, name='stand_base'),
        box(4, 46, 5, 62, 32, 3, m['cast_iron'], bevel=1.0, name='sponge_tray'),
        box(7, 49, 8, 56, 26, 7, m['sponge'], bevel=1.8, name='sponge'),
        box(74, 28, 5, 14, 14, 34, m['cast_iron'], bevel=1.4, name='stand_post'),
    ]
    coil = helix(56, 35, 42, 15, 3.2, 32, 1.7, m['steel'], name='stand_coil')
    coil.rotation_euler = (math.radians(74), 0, 0)
    parts.append(coil)
    g = _group(parts, 'stand')
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


def solder_spool(x, y, z, ang=0.0):
    """A 72 mm spool of 1 mm solder on its side, with a free end pulled off."""
    m = materials()
    parts = [
        cyl(0, 0, 36, 36, 2.5, m['spool'], axis='y', name='spool_flange_a'),
        cyl(0, 21.5, 36, 36, 2.5, m['spool'], axis='y', name='spool_flange_b'),
        cyl(0, 2.5, 36, 13, 19, m['spool'], axis='y', name='spool_hub'),
        cyl(0, 4.0, 36, 33.0, 16, m['solder'], axis='y', name='spool_wire'),
        cyl(0, -0.5, 36, 6.5, 25, m['handle_dark'], axis='y', name='spool_bore'),
        tube([(0, 12, 69), (18, 13, 62), (44, 14, 26), (62, 15, 3)],
             0.55, m['solder'], name='solder_tail'),
    ]
    g = _group(parts, 'spool')
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


def heat_shrink(x, y, z, length=18.0, r=2.2, ang=0.0):
    m = materials()
    ob = revolve([(r, 0), (r, length)], 0, 0, 0, m['shrink'], axis='x', name='shrink')
    ob.rotation_euler = (0, 0, math.radians(ang))
    ob.location = (x * MM, y * MM, z * MM)
    return ob


# ---------------------------------------------------------------- craft knife
def craft_knife(x, y, z, ang=0.0, tilt=0.0):
    """A snap-off utility knife in side view: tapered body, thumb slider, and an 18 mm blade
    leaving the nose at the angle it actually leaves at."""
    m = materials()
    parts = [
        prism_xz([(0, 1), (6, 0), (120, 0), (140, 4), (146, 9),
                  (140, 15), (120, 19), (6, 19), (0, 18)],
                 0, 0, 0, 25, m['grip'], name='knife_body', bevel=1.6),
        prism_xz([(8, 15), (124, 15), (136, 12.5), (124, 20.5), (8, 20.5)],
                 0, 1.5, 0, 22, m['handle_dark'], name='knife_spine', bevel=0.6),
        prism_xz([(0, 0), (28, 0), (28, 5), (0, 5)], 34, 3.5, 19, 18,
                 m['handle_dark'], name='knife_slider', bevel=0.7),
    ]
    for i in range(4):
        parts.append(box(37 + i * 5.5, 5.5, 23.4, 2.2, 14, 1.4, m['handle_dark'],
                         bevel=0.25, name='knurl'))
    blade = prism_xz([(0, 0), (52, 0), (52, 17.5), (0, 17.5)], 0, 0, 0, 0.5,
                     m['blade'], name='knife_blade', bevel=0.1)
    blade.location = (140 * MM, 12.2 * MM, 4 * MM)
    blade.rotation_euler = (0, math.radians(-30), 0)
    parts.append(blade)
    for i in range(3):                                   # snap-off score lines
        sc = prism_xz([(0, 0), (0.6, 0), (0.6, 15), (0, 15)], 0, 0, 0, 0.62,
                      m['handle_dark'], name='score', bevel=0)
        sc.location = ((140 + 11 + i * 11) * MM, 12.14 * MM, 4 * MM)
        sc.rotation_euler = (0, math.radians(-30), 0)
        parts.append(sc)
    g = _group(parts, 'knife')
    g.rotation_euler = (0, math.radians(tilt), math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


# ---------------------------------------------------------------- hot glue gun
def glue_gun(x, y, z, ang=0.0, stand=True):
    """A 20 W craft gun. Its shape only exists in side view — barrel forward, grip down — so the
    body is a side profile swept across its width, with the nozzle lathed onto the front."""
    m = materials()
    W = 42.0
    # barrel on top, pistol grip reaching properly down to the bench — a short foot instead
    # reads as a lump rather than something you hold
    side = [(0, 46), (0, 58), (12, 74), (96, 78), (128, 72), (140, 62), (140, 44),
            (126, 36), (96, 32), (78, 32), (72, 6), (58, 0), (40, 2), (36, 22),
            (32, 33), (8, 40)]
    parts = [
        prism_xz(side, 0, 0, 0, W, m['glue_body'], name='glue_shell', bevel=2.4),
        prism_xz([(20, 40), (94, 44), (122, 40), (94, 34), (20, 36)],
                 0, -0.6, 0, W + 1.2, m['glue_grey'], name='glue_seam', bevel=0.6),
        revolve([(13, 0), (14, 5), (11, 18), (7, 28), (3.4, 36), (1.8, 41)],
                138, W / 2, 54, m['brass'], axis='x', name='glue_nozzle'),
        revolve([(17, 0), (18, 7), (14, 15)], 126, W / 2, 54, m['glue_grey'],
                axis='x', name='glue_shroud'),
        prism_xz([(0, 0), (7, 2), (9, 20), (2, 22), (0, 16)], 62, 9, 14, W - 18,
                 m['glue_grey'], name='glue_trigger', bevel=1.0),
        revolve([(5.6, 0), (5.6, 66)], -4, W / 2, 60, m['glue_stick'],
                axis='x', name='glue_stick'),
        tube([(-62, W / 2, 60), (-92, W / 2 + 14, 48), (-124, W / 2 + 44, 22)],
             2.4, m['cable'], name='glue_cable'),
    ]
    if stand:
        parts.append(prism_xz([(0, 0), (40, 0), (40, 3), (0, 3)], 84, 4, 0, W - 8,
                              m['glue_grey'], name='glue_stand', bevel=0.6))
    g = _group(parts, 'gluegun')
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


# ---------------------------------------------------------------- safety goggles
def goggles(x, y, z, ang=0.0):
    """Wrap-around safety glasses: a curved lens in a frame, arms folded back."""
    m = materials()
    # A swept arc profile kept coming apart from its frame. At bench scale a heavily bevelled
    # lozenge reads as safety glasses just as well and holds together.
    # the frame is a RIM sitting above the lens, not a box over it — an oversized frame just
    # swallows the glass and the whole thing reads as a blue slab
    parts = [
        box(0, 0, 0, 118, 30, 22, m['lens'], bevel=8.0, name='goggle_lens'),
        box(-2, -1, 20, 122, 32, 4, m['goggle_frame'], bevel=1.8, name='goggle_brow'),
        box(-2, -1, -1, 122, 32, 3, m['goggle_frame'], bevel=1.8, name='goggle_sill'),
        box(53, 1, 3, 12, 28, 7, m['goggle_frame'], bevel=2.5, name='goggle_bridge'),
    ]
    for sy in (1.0, 33.0):
        off = -13 if sy < 3 else 13
        parts.append(tube([(6, sy, 22), (-14, sy + off * 0.6, 19), (-50, sy + off, 11)],
                          2.4, m['goggle_frame'], name='goggle_arm'))
    g = _group(parts, 'goggles')
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


# ---------------------------------------------------------------- bench props
def heat_mat(x, y, z, w=210, d=150):
    return box(x, y, z, w, d, 1.4, materials()['mat_dark'], bevel=1.0, name='heatmat')


def rules_card(x, y, z, w=64, d=48, ang=0.0):
    c = box(x, y, z, w, d, 0.5, materials()['paper'], bevel=0, name='card')
    c.rotation_euler = (0, 0, math.radians(ang))
    return c


def riser(x, y, z, w=110, d=88, h=60):
    return box(x, y, z, w, d, h, materials()['riser_box'], bevel=1.6, name='riser')


def laptop(x, y, z, ang=0.0, lid=100.0):
    """Open laptop: base, keyboard well, lid hinged `lid` degrees off the base."""
    m = materials()
    parts = [
        box(0, 0, 0, 300, 210, 12, m['laptop_body'], bevel=2.0, name='lt_base'),
        box(24, 34, 12, 252, 110, 0.8, m['handle_dark'], bevel=0.4, name='lt_keys'),
        box(104, 152, 12, 92, 46, 0.6, m['glue_grey'], bevel=0.4, name='lt_pad'),
    ]
    lid_g = _group([box(0, 0, 0, 300, 200, 8, m['laptop_body'], bevel=2.0, name='lt_lid'),
                    box(10, 9, 8, 280, 182, 0.6, m['screen'], bevel=0, name='lt_screen')],
                   'lt_lidg')
    lid_g.location = (0, 0, 12 * MM)
    lid_g.rotation_euler = (math.radians(lid), 0, 0)
    g = _group(parts, 'laptop')
    lid_g.parent = g
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


# ================================================================ the chassis-build tools
def ruler(x, y, z, ang=0.0, length=200.0):
    """A clear 200 mm plastic ruler with real graduations — the card has the student check the
    template's 5 cm strip against it, so the scale has to be legible."""
    m = materials()
    parts = [box(0, 0, 0, length + 20, 32, 2.2, m['ruler_clear'], bevel=1.0, name='ruler')]
    for i in range(0, int(length) + 1, 5):
        long_ = (i % 50 == 0)
        h = 11 if long_ else (7 if i % 10 == 0 else 4)
        parts.append(box(10 + i - 0.25, 32 - h, 2.2, 0.5, h, 0.25,
                         m['handle_dark'], bevel=0, name='tick'))
    g = _group(parts, 'ruler_g')
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


def pencil(x, y, z, ang=0.0, tilt=0.0):
    """A hexagonal HB pencil. revolve() with six segments IS a hex prism, which is neater than
    trying to extrude one."""
    m = materials()
    parts = [
        revolve([(4.0, 0), (4.0, 150)], 0, 0, 0, m['pencil_body'], axis='x',
                seg=6, name='pencil_barrel', smooth=False),
        revolve([(4.0, 0), (2.4, 12), (0.9, 17)], -17, 0, 0, m['pencil_wood'], axis='x',
                seg=6, name='pencil_cone', smooth=False),
        revolve([(0.9, 0), (0.15, 4)], -21, 0, 0, m['handle_dark'], axis='x',
                name='pencil_lead'),
        revolve([(4.1, 0), (4.1, 9)], 150, 0, 0, m['chrome'], axis='x', seg=6,
                name='pencil_ferrule', smooth=False),
        revolve([(3.8, 0), (3.6, 7)], 159, 0, 0, m['eraser'], axis='x', name='pencil_eraser'),
    ]
    g = _group(parts, 'pencil')
    g.rotation_euler = (0, math.radians(tilt), math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


def screwdriver(x, y, z, ang=0.0, tilt=0.0):
    """A pozidriv driver: steel shaft with a cross tip, and a lathed handle whose grip swells
    are in the profile rather than bolted on as separate pieces."""
    m = materials()
    parts = [
        revolve([(0, 0), (1.2, 2), (2.6, 6), (2.6, 92)], 0, 0, 0, m['steel'],
                axis='x', name='sd_shaft'),
        revolve([(2.6, 0), (7, 3), (11, 10), (12.5, 22), (11.4, 34), (12.6, 44),
                 (11.4, 56), (12.6, 66), (11.0, 80), (7.5, 92), (4.0, 96)],
                92, 0, 0, m['sd_handle'], axis='x', name='sd_handle'),
        revolve([(12.7, 0), (12.7, 4)], 112, 0, 0, m['sd_grip'], axis='x', name='sd_band'),
    ]
    g = _group(parts, 'screwdriver')
    g.rotation_euler = (0, math.radians(tilt), math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


def drill(x, y, z, ang=0.0, bit=60.0, tilt=0.0):
    """A cordless drill: side profile with a lathed chuck and bit, barrel forward along +x.
    tilt=-90 stands it on its nose, which is how it looks drilling into a plate — at tilt 0 it
    reads as lying on the bench pointing sideways."""
    m = materials()
    W = 46.0
    side = [(0, 62), (14, 84), (86, 88), (116, 82), (128, 70), (128, 44), (114, 34),
            (86, 30), (68, 30), (62, 4), (46, -18), (24, -14), (26, 10), (24, 30), (6, 40)]
    parts = [
        prism_xz(side, 0, 0, 0, W, m['drill_body'], name='drill_shell', bevel=2.6),
        prism_xz([(18, 34), (84, 38), (112, 34), (84, 28), (18, 30)],
                 0, -0.7, 0, W + 1.4, m['drill_grey'], name='drill_seam', bevel=0.6),
        # battery pack on the bottom of the grip
        prism_xz([(0, 0), (44, 0), (44, 22), (0, 22)], 18, 3, -40, W - 6,
                 m['drill_grey'], name='drill_batt', bevel=2.0),
        # chuck and bit
        revolve([(19, 0), (20, 6), (19, 26), (13, 34)], 126, W / 2, 58, m['chuck'],
                axis='x', name='drill_chuck'),
        revolve([(2.0, 0), (2.0, bit)], 158, W / 2, 58, m['steel'], axis='x', name='drill_bit'),
        prism_xz([(0, 0), (10, 2), (12, 18), (2, 20)], 56, 12, 44, W - 20,
                 m['drill_grey'], name='drill_trigger', bevel=0.8),
    ]
    g = _group(parts, 'drill')
    g.rotation_euler = (0, math.radians(tilt), math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


def m3_screw(x, y, z, length=30.0, axis='z', head=True, down=True):
    """An M3 machine screw with its HEAD at (x, y, z). `down` runs the shank away from the
    viewer's side of the plate, which is where a screw actually goes; running it the other way
    leaves the figure looking like a bed of nails."""
    m = materials()
    sgn = -1.0 if down else 1.0
    parts = []
    if head:
        parts.append(revolve([(0, 0), (2.9, 0), (2.9, 2.0 * sgn), (2.4, 2.4 * sgn)],
                             x, y, z, m['steel'], axis=axis, name='screw_head'))
    parts.append(revolve([(1.5, 2.0 * sgn), (1.5, (length - 2) * sgn), (0.8, length * sgn)],
                         x, y, z, m['steel'], axis=axis, name='screw_shank'))
    return _group(parts, 'm3screw')


def m3_nut(x, y, z, axis='z'):
    m = materials()
    return revolve([(2.75, 0), (2.75, 2.4)], x, y, z, m['steel'], axis=axis, seg=6,
                   name='m3nut', smooth=False)


def zip_tie(x, y, z, w, d, h, ang=0.0):
    """A cable tie wrapped around a w x d footprint of height h, head on the near side."""
    m = materials()
    parts = [
        box(0, 0, 0, 2.6, d, 1.2, m['ziptie'], bevel=0.3, name='zt_bottom'),
        box(0, 0, 0, 2.6, 1.2, h, m['ziptie'], bevel=0.3, name='zt_side_a'),
        box(0, d - 1.2, 0, 2.6, 1.2, h, m['ziptie'], bevel=0.3, name='zt_side_b'),
        box(0, 0, h, 2.6, d, 1.2, m['ziptie'], bevel=0.3, name='zt_top'),
        box(-1.4, d - 4, h - 1, 5.4, 6, 4.4, m['ziptie'], bevel=0.8, name='zt_head'),
    ]
    g = _group(parts, 'ziptie')
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


def tape_roll(x, y, z, ang=0.0):
    """A roll of masking tape on its side. Cylinders, not a self-closing lathe profile —
    a profile whose last point returns to its first folds in on itself."""
    m = materials()
    parts = [
        cyl(0, 0, 48, 48, 24, m['masking'], axis='y', name='tape_roll'),
        cyl(0, -0.5, 48, 26, 25, m['paper'], axis='y', name='tape_core'),
        cyl(0, 1.0, 48, 25.4, 22, m['bench_hole'], axis='y', name='tape_bore'),
    ]
    g = _group(parts, 'tape_roll_g')
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g

