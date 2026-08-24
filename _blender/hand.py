"""hand.py — a simplified human hand, at real adult size.

Every card brief in this program describes a hand doing something: a thumb pressing a motor
into a grommet, a finger sweeping four bare shafts, a fingertip on a BOOT button. Figures that
show only the parts turn an instruction into a catalogue, so the hand is worth modelling.

STATUS: modelled, checked with s_handcheck, and NOT yet used in any card figure. The flat and
point poses read as a hand; the curled ones (press, pinch, grip) still read as a mitten with
sticks, and a poor hand in an instruction figure is worse than no hand — it is the first thing
a reader looks at. Finish the curled poses before wiring this into a scene, and when you do,
add it everywhere the briefs call for a hand rather than to two figures out of sixty.

It is deliberately simple — a palm block and capsule phalanges, no knuckle creases, no nails.
Under the Freestyle ink pass that reads as a diagram hand, which is what these figures are.
Trying for realism here would land in the uncanny valley and be worse than no hand at all.

Geometry is adult-average in millimetres:
  palm        95 long x 82 wide x 26 thick at the knuckles
  index       proximal 45, middle 26, distal 21
  middle      proximal 50, middle 30, distal 22
  ring        proximal 46, middle 28, distal 21
  little      proximal 36, middle 21, distal 18
  thumb       metacarpal 46, proximal 33, distal 26, set 55 degrees off the palm axis

The hand is built pointing along +x with the back of the hand up, wrist at the origin. Poses
bend the joints downward, so a hand placed above a part and rotated reaches down to it.
"""
import math
import lib as L
from lib import MM, box, cyl, capsule, sphere, mat, hexcol

_M = None

PALM_L, PALM_W, PALM_T = 95.0, 82.0, 21.0

# knuckle (x, y, base radius, [proximal, middle, distal]). The x values differ on purpose:
# the knuckle line is oblique, index furthest forward and little finger set well back, and a
# straight line of knuckles is most of what made the first version read as a garden rake.
FINGERS = {
    'index':  (94.0, -26.0, 9.2, (45.0, 26.0, 21.0)),
    'middle': (97.0, -8.5, 9.6, (50.0, 30.0, 22.0)),
    'ring':   (92.0, 9.0, 9.0, (46.0, 28.0, 21.0)),
    'little': (83.0, 25.0, 7.8, (36.0, 21.0, 18.0)),
}

# the palm seen from above, wrist at the origin, thumb side at -y
PALM_OUTLINE = [(2, -27), (30, -35), (62, -37), (86, -34), (97, -26),
                (100, -4), (95, 14), (86, 29), (52, 33), (14, 28)]

# joint angles per pose, in degrees, positive = curling toward the palm
POSES = {
    # a flat hand resting on something
    'flat':   {'index': (6, 4, 3), 'middle': (6, 4, 3), 'ring': (7, 5, 3),
               'little': (9, 6, 4), 'thumb': (12, 8)},
    # one finger out, the rest folded away — pointing at a part, or on a button
    'point':  {'index': (4, 3, 2), 'middle': (78, 88, 46), 'ring': (82, 92, 48),
               'little': (86, 94, 50), 'thumb': (30, 34)},
    # thumb pressing straight down, fingers curled clear: the press-fit hand
    'press':  {'index': (52, 74, 40), 'middle': (56, 78, 42), 'ring': (60, 82, 44),
               'little': (64, 86, 46), 'thumb': (8, 6)},
    # holding a slim object between thumb and index
    'pinch':  {'index': (44, 52, 34), 'middle': (66, 80, 44), 'ring': (72, 86, 46),
               'little': (78, 90, 48), 'thumb': (34, 40)},
    # wrapped round a handle
    'grip':   {'index': (62, 84, 46), 'middle': (66, 86, 48), 'ring': (68, 88, 48),
               'little': (70, 90, 50), 'thumb': (40, 46)},
}


def materials():
    global _M
    if _M is None:
        _M = dict(
            skin=mat('h_skin', hexcol('#cf9068'), rough=0.66, clearcoat=0.05),
            cuff=mat('h_cuff', hexcol('#3d5a80'), rough=0.78),
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


def _chain(x, y, z, lengths, radii, angles, m, name='digit'):
    """Walk a finger out from its knuckle, bending down by each joint angle in turn."""
    out = []
    ang = 0.0
    px, py, pz = x, y, z
    for i, (ln, r) in enumerate(zip(lengths, radii)):
        ang += math.radians(angles[i])
        nx = px + ln * math.cos(ang)
        nz = pz - ln * math.sin(ang)
        out.append(capsule((px, py, pz), (nx, py, nz), r, m, name=name))
        px, pz = nx, nz
    return out, (px, py, pz)


def hand(x, y, z, ang=0.0, pitch=0.0, roll=0.0, pose='flat', side='right', cuff=True):
    """A hand, wrist at (x, y, z), pointing along +x before `ang` turns it about Z.

    `pitch` tips the whole hand nose-down (negative reaches down onto the bench), `roll` turns
    it about its own axis — a hand pressing a button from above is pitch=-70.
    """
    m = materials()
    P = POSES.get(pose, POSES['flat'])
    sgn = 1.0 if side == 'right' else -1.0
    parts = []
    # the palm as one tapered prism, heavily bevelled. Two axis-aligned boxes gave a brick, and
    # no amount of finger detail rescues a brick.
    pts = [(x, sgn * y) for x, y in PALM_OUTLINE]
    if sgn < 0:
        pts.reverse()
    parts.append(L.prism(pts, -PALM_T / 2, PALM_T, m['skin'], name='palm', bevel=5.5))
    # the thenar pad, the fleshy mound at the base of the thumb: without it the palm reads flat
    parts.append(capsule((22, sgn * -20, -3), (52, sgn * -27, -1), 12.0, m['skin'],
                         name='thenar'))
    if cuff:
        parts.append(box(-30, sgn * -30, -PALM_T / 2 - 3, 32, 60, PALM_T + 6,
                         m['cuff'], bevel=7.0, name='cuff'))
    for nm, (kx, fy, r, lens) in FINGERS.items():
        # a real finger is 18-20 mm across, so the capsule radius is the knuckle radius
        # itself, not half of it. Half-width fingers were most of why the first hand
        # read as a rake: the palm was right and the digits were doll-sized.
        radii = (r, r * 0.9, r * 0.8)
        segs, tip = _chain(kx, sgn * fy, 0.0, lens, radii, P[nm], m['skin'], name='phalanx')
        parts += segs
        parts.append(sphere(tip[0], tip[1], tip[2], radii[-1] * 0.97, m['skin'], name='tip'))
    # the thumb leaves the palm side-on and forward, so it works against the fingers
    ta = math.radians(55.0)
    tx0, ty0 = 34.0, sgn * -31.0
    tm_len = 46.0
    tx1 = tx0 + tm_len * math.cos(ta)
    ty1 = ty0 - sgn * tm_len * math.sin(ta)
    parts.append(capsule((tx0, ty0, -4), (tx1, ty1, -2), 11.5, m['skin'], name='thumb_meta'))
    a1, a2 = (math.radians(v) for v in P['thumb'])
    tx2 = tx1 + 33.0 * math.cos(ta) * math.cos(a1)
    ty2 = ty1 - sgn * 33.0 * math.sin(ta) * math.cos(a1)
    tz2 = -2 - 33.0 * math.sin(a1)
    parts.append(capsule((tx1, ty1, -2), (tx2, ty2, tz2), 10.2, m['skin'], name='thumb_prox'))
    tx3 = tx2 + 26.0 * math.cos(ta) * math.cos(a1 + a2)
    ty3 = ty2 - sgn * 26.0 * math.sin(ta) * math.cos(a1 + a2)
    tz3 = tz2 - 26.0 * math.sin(a1 + a2)
    parts.append(capsule((tx2, ty2, tz2), (tx3, ty3, tz3), 9.0, m['skin'], name='thumb_dist'))
    parts.append(sphere(tx3, ty3, tz3, 8.6, m['skin'], name='thumb_tip'))

    g = _group(parts, 'hand')
    g.rotation_euler = (math.radians(roll), math.radians(pitch), math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    g['tip'] = (tx3, ty3, tz3)
    return g
