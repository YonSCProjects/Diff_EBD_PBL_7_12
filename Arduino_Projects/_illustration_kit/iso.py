"""iso.py — a small isometric SVG engine for the workshop's step illustrations.

Why hand-rolled: the pictures have to be *accurate* (every part at its real millimetre
size and its real place on the chassis template), *consistent* across ~44 cards, and
crisp in print. A vector engine gives all three; it also means a card can be re-rendered
after a hardware change instead of re-photographed.

World units are MILLIMETRES, in the same frame as chassis_template_he.html:
  x = along the car, 23.5 (nose) .. 273.5 (tail)
  y = across the car, 35 (left side) .. 185 (right side)
  z = up from the top face of the plate (negative = below the plate)

Projection is true isometric (30°), light comes from the top-left-front, and every solid
gets three tones of one base colour so shapes read instantly at card size.
"""
import math

COS30 = math.cos(math.radians(30))
SIN30 = 0.5

# ---------------------------------------------------------------- projection

def iso(x, y, z=0.0):
    """World mm -> 2D drawing units (also mm-ish, so stroke widths stay sane)."""
    return ((x - y) * COS30, (x + y) * SIN30 - z)


def depth(x, y, z=0.0):
    """Painter's-algorithm key: bigger = nearer the camera, drawn later."""
    return x + y + z * 0.85


# ---------------------------------------------------------------- colour

def _clamp(v):
    return max(0, min(255, int(round(v))))


def shade(hexcol, f):
    """Multiply a #rrggbb colour by f (f<1 darkens, f>1 lightens toward white)."""
    h = hexcol.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    if f <= 1:
        r, g, b = r * f, g * f, b * f
    else:
        k = f - 1
        r, g, b = r + (255 - r) * k, g + (255 - g) * k, b + (255 - b) * k
    return '#%02x%02x%02x' % (_clamp(r), _clamp(g), _clamp(b))


# Face brightness: top is lit, the two sides fall away. One rule for every solid.
F_TOP, F_LEFT, F_RIGHT = 1.12, 0.74, 0.92


# ---------------------------------------------------------------- primitives

class Scene:
    """Collects drawable items with a depth key, then emits sorted SVG."""

    def __init__(self):
        self.items = []          # (depth, svg string)
        self.overlay = []        # drawn last, in insertion order (labels, arrows)

    def add(self, d, svg, layer=0):
        """layer wins over depth, so a board resting on a big plate is never sorted
        behind it. 0=under-plate far, 1=plate, 2=under-plate near, 3=on-plate,
        4=wires, 5=tools/hands."""
        self.items.append((layer * 100000 + d, svg))

    def over(self, svg):
        self.overlay.append(svg)

    def body(self):
        parts = [s for _, s in sorted(self.items, key=lambda t: t[0])]
        return '\n'.join(parts + self.overlay)


def poly(pts, fill, stroke=None, sw=0.35, extra=''):
    d = ' '.join('%.2f,%.2f' % p for p in pts)
    st = 'stroke:%s;stroke-width:%s;stroke-linejoin:round' % (stroke, sw) if stroke else 'stroke:none'
    return '<polygon points="%s" style="fill:%s;%s%s"/>' % (d, fill, st, (';' + extra) if extra else '')


def cuboid(sc, x, y, z, w, d_, h, col, edge=None, label=None, alpha=None, top_col=None, layer=3):
    """Axis-aligned box: x..x+w along the car, y..y+d_ across, z..z+h up."""
    edge = edge or shade(col, 0.55)
    op = '' if alpha is None else 'fill-opacity:%s' % alpha
    x2, y2, z2 = x + w, y + d_, z + h
    top = [iso(x, y, z2), iso(x2, y, z2), iso(x2, y2, z2), iso(x, y2, z2)]
    left = [iso(x, y2, z2), iso(x2, y2, z2), iso(x2, y2, z), iso(x, y2, z)]     # +y face
    right = [iso(x2, y, z2), iso(x2, y2, z2), iso(x2, y2, z), iso(x2, y, z)]    # +x face
    s = (poly(left, shade(top_col or col, F_LEFT), edge, extra=op)
         + poly(right, shade(top_col or col, F_RIGHT), edge, extra=op)
         + poly(top, shade(top_col or col, F_TOP), edge, extra=op))
    sc.add(depth(x + w / 2, y + d_ / 2, z + h / 2), s, layer)
    if label:
        cx, cy = iso(x + w / 2, y + d_ / 2, z2)
        sc.over('<text x="%.2f" y="%.2f" style="font-family:Rubik,Arial;font-size:%spx;font-weight:700;'
                'fill:%s;text-anchor:middle">%s</text>' % (cx, cy + 1.6, label[1], label[2], label[0]))
    return s


def cyl_x(sc, x, y, z, length, r, col, edge=None, cap_col=None, steps=22, layer=3):
    """Cylinder whose axis runs along +x (motor bodies, axles)."""
    edge = edge or shade(col, 0.55)
    ring = [(math.cos(2 * math.pi * i / steps) * r, math.sin(2 * math.pi * i / steps) * r) for i in range(steps)]
    near = [iso(x + length, y + dy, z + dz) for dy, dz in ring]
    far = [iso(x, y + dy, z + dz) for dy, dz in ring]
    # side quads, shaded by the ring angle so the top-left is lit
    quads = []
    for i in range(steps):
        j = (i + 1) % steps
        a = 2 * math.pi * (i + 0.5) / steps
        f = 0.72 + 0.42 * max(0.0, math.cos(a - math.radians(215)))
        quads.append((f, poly([far[i], near[i], near[j], far[j]], shade(col, f), None)))
    body = ''.join(s for _, s in quads)
    body += poly(near, shade(cap_col or col, 1.06), edge, 0.3)
    sc.add(depth(x + length / 2, y, z), body, layer)
    return body


def cyl_y(sc, x, y, z, length, r, col, edge=None, cap_col=None, steps=22, layer=3):
    """Cylinder whose axis runs along +y (wheels, axles across the car)."""
    edge = edge or shade(col, 0.55)
    ring = [(math.cos(2 * math.pi * i / steps) * r, math.sin(2 * math.pi * i / steps) * r) for i in range(steps)]
    near = [iso(x + dx, y + length, z + dz) for dx, dz in ring]
    far = [iso(x + dx, y, z + dz) for dx, dz in ring]
    quads = []
    for i in range(steps):
        j = (i + 1) % steps
        a = 2 * math.pi * (i + 0.5) / steps
        f = 0.70 + 0.44 * max(0.0, math.cos(a - math.radians(160)))
        quads.append(poly([far[i], near[i], near[j], far[j]], shade(col, f), None))
    body = ''.join(quads)
    body += poly(near, shade(cap_col or col, 1.05), edge, 0.3)
    sc.add(depth(x, y + length / 2, z), body, layer)
    return body


def cyl_z(sc, x, y, z, height, r, col, edge=None, cap_col=None, steps=26, layer=3, hole=0.0):
    """Cylinder standing on its end (motor cans, standoffs, electrolytics, prop hubs).
    hole > 0 leaves a visible bore in the top cap."""
    edge = edge or shade(col, 0.55)
    ring = [(math.cos(2 * math.pi * i / steps) * r, math.sin(2 * math.pi * i / steps) * r) for i in range(steps)]
    top = [iso(x + dx, y + dy, z + height) for dx, dy in ring]
    bot = [iso(x + dx, y + dy, z) for dx, dy in ring]
    quads = []
    for i in range(steps):
        j = (i + 1) % steps
        a = 2 * math.pi * (i + 0.5) / steps
        # the camera looks from -y/+x, so the wall facing (1,-1) is the lit one
        if math.cos(a - math.radians(-45)) < -0.02:
            continue                                   # back wall, hidden by the top cap
        f = 0.66 + 0.44 * max(0.0, math.cos(a - math.radians(-30)))
        quads.append(poly([top[i], top[j], bot[j], bot[i]], shade(col, f), None))
    s = ''.join(quads)
    s += poly(top, shade(cap_col or col, F_TOP), edge, 0.3)
    if hole > 0:
        hr = [(math.cos(2 * math.pi * i / steps) * hole, math.sin(2 * math.pi * i / steps) * hole)
              for i in range(steps)]
        s += poly([iso(x + dx, y + dy, z + height) for dx, dy in hr], shade(col, 0.42), None)
    sc.add(depth(x, y, z + height / 2), s, layer)
    return s


def disc(sc, x, y, z, r, col, stroke=None, sw=0.35, extra='', layer=3, steps=30, bump=0.0):
    """A flat circle lying in the xy plane (spin discs, scale pans, drill marks)."""
    pts = [iso(x + math.cos(2 * math.pi * i / steps) * r, y + math.sin(2 * math.pi * i / steps) * r, z)
           for i in range(steps)]
    s = poly(pts, col, stroke, sw, extra)
    sc.add(depth(x, y, z) + bump, s, layer)
    return s


def ring_z(sc, x, y, z, r_out, r_in, height, col, edge=None, steps=26, layer=3):
    """An annulus with thickness: the frame's arm rings and their rubber grommets."""
    edge = edge or shade(col, 0.55)
    ro = [(math.cos(2 * math.pi * i / steps) * r_out, math.sin(2 * math.pi * i / steps) * r_out) for i in range(steps)]
    ri = [(math.cos(2 * math.pi * i / steps) * r_in, math.sin(2 * math.pi * i / steps) * r_in) for i in range(steps)]
    topo = [iso(x + dx, y + dy, z + height) for dx, dy in ro]
    boto = [iso(x + dx, y + dy, z) for dx, dy in ro]
    topi = [iso(x + dx, y + dy, z + height) for dx, dy in ri]
    s = ''
    for i in range(steps):                                    # outer wall, front half only
        j = (i + 1) % steps
        a = 2 * math.pi * (i + 0.5) / steps
        if math.cos(a - math.radians(-45)) < -0.02:
            continue
        f = 0.66 + 0.44 * max(0.0, math.cos(a - math.radians(-30)))
        s += poly([topo[i], topo[j], boto[j], boto[i]], shade(col, f), None)
    for i in range(steps):                                    # the flat top, as a fan of quads
        j = (i + 1) % steps
        s += poly([topo[i], topo[j], topi[j], topi[i]], shade(col, F_TOP), None)
    s += poly(topo, 'none', edge, 0.3)
    s += poly(topi, 'none', edge, 0.3)
    sc.add(depth(x, y, z + height / 2), s, layer)
    return s


def prism(sc, pts2d, z, height, col, edge=None, layer=3, top_extra='', key=None):
    """Extrude an arbitrary xy outline upward: the X-shaped carbon plates.
    Winding is normalised here, so callers may list the outline either way round."""
    edge = edge or shade(col, 0.55)
    area = sum(pts2d[i][0] * pts2d[(i + 1) % len(pts2d)][1] - pts2d[(i + 1) % len(pts2d)][0] * pts2d[i][1]
               for i in range(len(pts2d)))
    if area > 0:                     # counter-clockwise in world xy -> flip to clockwise
        pts2d = pts2d[::-1]
    top = [iso(px, py, z + height) for px, py in pts2d]
    bot = [iso(px, py, z) for px, py in pts2d]
    s = ''
    n = len(pts2d)
    for i in range(n):
        j = (i + 1) % n
        (x1, y1), (x2, y2) = pts2d[i], pts2d[j]
        nx, ny = (y2 - y1), -(x2 - x1)                 # outward normal for a CW ring
        if nx + ny <= 0:
            continue                                    # facing away from the camera
        f = F_RIGHT if abs(nx) > abs(ny) else F_LEFT
        s += poly([top[i], top[j], bot[j], bot[i]], shade(col, f), edge, 0.25)
    s += poly(top, shade(col, F_TOP), edge, 0.3, top_extra)
    cx = sum(p[0] for p in pts2d) / n
    cy = sum(p[1] for p in pts2d) / n
    sc.add(key if key is not None else depth(cx, cy, z + height / 2), s, layer)
    return s


def blade(sc, x, y, z, ang, r_hub, r_tip, col, cw=True, pitch=1.8, layer=3, steps=16, alpha=None):
    """One propeller blade sweeping out from a hub, with enough twist to read as a real prop.
    ang is the blade's root direction in degrees; cw flips the sweep and the twist."""
    sgn = 1.0 if cw else -1.0
    lead, trail = [], []
    for i in range(steps + 1):
        t = i / steps
        r = r_hub + (r_tip - r_hub) * t
        # the blade sweeps back as it goes out, and is widest around mid-span
        a = math.radians(ang + sgn * 26 * t)
        # chord: widest just inboard of mid-span, tapering to a rounded tip
        w = (r_tip - r_hub) * 0.155 * math.sin(math.pi * t ** 0.86) ** 0.6 + 0.45
        p = pitch * math.sin(math.pi * t) * sgn
        ca, sa = math.cos(a), math.sin(a)
        px, py = -sa, ca                                # unit normal to the blade axis
        lead.append(iso(x + ca * r + px * w, y + sa * r + py * w, z + p))
        trail.append(iso(x + ca * r - px * w, y + sa * r - py * w, z - p))
    pts = lead + trail[::-1]
    op = '' if alpha is None else 'fill-opacity:%s' % alpha
    s = poly(pts, shade(col, 1.0), shade(col, 0.55), 0.28, op)
    s += ('<path d="M %s" style="fill:none;stroke:%s;stroke-width:0.35;stroke-opacity:0.55"/>'
          % (' L '.join('%.2f %.2f' % p for p in lead), shade(col, 1.35)))
    sc.add(depth(x + math.cos(math.radians(ang)) * r_tip * 0.5,
                 y + math.sin(math.radians(ang)) * r_tip * 0.5, z), s, layer)
    return s


def spin_arc(sc, x, y, z, r, cw=True, col='#5b6470', layer=5, span=210):
    """The dashed arc + arrowhead that says 'this is turning, and this way round'."""
    a0 = math.radians(-40)
    a1 = a0 + math.radians(span) * (1 if cw else -1)
    pts = []
    n = 30
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        pts.append(iso(x + math.cos(a) * r, y + math.sin(a) * r, z))
    d = 'M ' + ' L '.join('%.2f %.2f' % p for p in pts)
    s = ('<path d="%s" style="fill:none;stroke:%s;stroke-width:1.1;stroke-linecap:round;'
         'stroke-dasharray:3.2 2.4"/>' % (d, col))
    (bx, by), (tx, ty) = pts[-2], pts[-1]
    dx, dy = tx - bx, ty - by
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    hx, hy = -uy, ux
    s += ('<polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f" style="fill:%s"/>'
          % (tx + ux * 3.4, ty + uy * 3.4, tx - ux * 1.6 + hx * 2.5, ty - uy * 1.6 + hy * 2.5,
             tx - ux * 1.6 - hx * 2.5, ty - uy * 1.6 - hy * 2.5, col))
    sc.over(s)
    return s


def plate(sc, z=0.0, thickness=9.0, col='#eef2f6', flutes=True):
    """The polygal chassis plate: 250x150 with 15 mm clipped corners, twin-wall flutes
    running along the car (the template's 'flute direction' arrow)."""
    P = [(38.5, 35), (258.5, 35), (273.5, 50), (273.5, 170), (258.5, 185), (38.5, 185), (23.5, 170), (23.5, 50)]
    top = [iso(px, py, z + thickness) for px, py in P]
    bot = [iso(px, py, z) for px, py in P]
    edge = shade(col, 0.62)
    s = ''
    # side walls: only the two faces that face the camera (+x and +y sides)
    for i in range(len(P)):
        j = (i + 1) % len(P)
        (x1, y1), (x2, y2) = P[i], P[j]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        nx, ny = (y2 - y1), -(x2 - x1)          # outward normal (CW polygon)
        if nx + ny <= 0:
            continue
        f = F_RIGHT if abs(nx) > abs(ny) else F_LEFT
        s += poly([top[i], top[j], bot[j], bot[i]], shade(col, f), edge, 0.3)
    if flutes:
        # inner flute lines on the visible +y wall, hinting twin-wall structure
        for fy in [x for x in range(46, 266, 6)]:
            a = iso(fy, 185, z + thickness * 0.72)
            b = iso(fy + 3.2, 185, z + thickness * 0.72)
            s += '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" style="stroke:%s;stroke-width:0.5"/>' % (
                a[0], a[1], b[0], b[1], shade(col, 0.5))
    s += poly(top, shade(col, F_TOP), edge, 0.4)
    if flutes:
        # twin-wall flute lines across the top face, running along the car (+x)
        import math as _m
        yy = 41.0
        while yy < 179.0:
            a = iso(27.5, yy, z + thickness); b = iso(269.5, yy, z + thickness)
            s += ('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" style="stroke:%s;stroke-width:0.32;stroke-opacity:0.5"/>'
                  % (a[0], a[1], b[0], b[1], shade(col, 0.80)))
            yy += 6.0
    sc.add(depth(148, 110, z), s, 1)
    return s


def shadow(sc, x, y, w, d_, blur=2.2, op=0.16):
    """Soft contact shadow on the floor plane under a footprint."""
    pts = [iso(x, y, 0), iso(x + w, y, 0), iso(x + w, y + d_, 0), iso(x, y + d_, 0)]
    cx = sum(p[0] for p in pts) / 4
    cy = sum(p[1] for p in pts) / 4
    rx = (max(p[0] for p in pts) - min(p[0] for p in pts)) / 2 * 1.05
    ry = (max(p[1] for p in pts) - min(p[1] for p in pts)) / 2 * 1.05
    sc.add(-9999, '<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" style="fill:#0b1622;fill-opacity:%s;filter:url(#soft)"/>'
           % (cx, cy + 1.2, rx, ry, op))


# ---------------------------------------------------------------- wires

def wire(sc, pts3, col='#cc1414', w=1.5, z_bias=0.0, layer=4):
    """A routed wire through 3-D waypoints, drawn with a dark casing + core + highlight."""
    p2 = [iso(*p) for p in pts3]
    d = 'M ' + ' L '.join('%.2f %.2f' % p for p in p2)
    s = ('<path d="%s" style="fill:none;stroke:%s;stroke-width:%.2f;stroke-linecap:round;stroke-linejoin:round"/>'
         % (d, shade(col, 0.5), w + 0.55))
    s += ('<path d="%s" style="fill:none;stroke:%s;stroke-width:%.2f;stroke-linecap:round;stroke-linejoin:round"/>'
          % (d, col, w))
    s += ('<path d="%s" style="fill:none;stroke:#ffffff;stroke-opacity:0.28;stroke-width:%.2f;stroke-linecap:round"/>'
          % (d, w * 0.3))
    key = max(depth(*p) for p in pts3) + 0.4 + z_bias
    sc.add(key, s, layer)
    return s


def dupont(sc, x, y, z, col='#222', ang='x', layer=4):
    """A little Dupont connector shell where a jumper meets a header."""
    if ang == 'x':
        cuboid(sc, x, y - 1.3, z, 5.5, 2.6, 2.6, col, layer=layer)
    else:
        cuboid(sc, x - 1.3, y, z, 2.6, 5.5, 2.6, col, layer=layer)


# ---------------------------------------------------------------- annotation

def arrow(sc, p_from, p_to, col='#e0651a', w=2.2, head=4.6, curve=0.0):
    """Action arrow in world space (drawn on top of everything)."""
    a, b = iso(*p_from), iso(*p_to)
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    tipx, tipy = b[0], b[1]
    bx, by = tipx - ux * head, tipy - uy * head
    px, py = -uy, ux
    if curve:
        mx, my = (a[0] + b[0]) / 2 + px * curve, (a[1] + b[1]) / 2 + py * curve
        d = 'M %.2f %.2f Q %.2f %.2f %.2f %.2f' % (a[0], a[1], mx, my, bx, by)
    else:
        d = 'M %.2f %.2f L %.2f %.2f' % (a[0], a[1], bx, by)
    s = ('<path d="%s" style="fill:none;stroke:#ffffff;stroke-width:%.2f;stroke-linecap:round"/>'
         % (d, w + 1.8))
    s += ('<path d="%s" style="fill:none;stroke:%s;stroke-width:%.2f;stroke-linecap:round"/>' % (d, col, w))
    s += ('<polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f" style="fill:%s;stroke:#fff;stroke-width:0.7;stroke-linejoin:round"/>'
          % (tipx, tipy, bx + px * head * 0.42, by + py * head * 0.42,
             bx - px * head * 0.42, by - py * head * 0.42, col))
    sc.over(s)


def tag(sc, p_world, text, dx=0.0, dy=-14.0, size=6.4, fill='#ffffff', stroke='#2a3442',
        color='#16202c', leader=True, bold=True, anchor='middle'):
    """A callout label pinned to a world point, with a leader line."""
    ax, ay = iso(*p_world)
    tx, ty = ax + dx, ay + dy
    lines = text.split('\n')
    wch = size * 0.60
    w = max(len(l) for l in lines) * wch + size * 1.15
    h = len(lines) * size * 1.28 + size * 0.62
    bx = tx - w / 2 if anchor == 'middle' else (tx if anchor == 'start' else tx - w)
    by = ty - h / 2
    s = ''
    if leader:
        s += ('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" style="stroke:%s;stroke-width:0.7;'
              'stroke-dasharray:2.2 1.8;stroke-opacity:0.85"/>' % (ax, ay, tx, ty, stroke))
        s += '<circle cx="%.2f" cy="%.2f" r="1.35" style="fill:none;stroke:%s;stroke-width:0.85"/>' % (ax, ay, stroke)
    if fill != 'none':
        s += ('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" style="fill:%s;stroke:%s;'
              'stroke-width:0.7;fill-opacity:0.97"/>' % (bx, by, w, h, size * 0.42, fill, stroke))
    for i, l in enumerate(lines):
        ly = by + size * 0.62 + size * 1.28 * i + size * 0.78
        s += ('<text x="%.2f" y="%.2f" style="font-family:Rubik,Arial;font-size:%spx;font-weight:%s;'
              'fill:%s;text-anchor:middle">%s</text>' % (tx, ly, size, 700 if bold else 500, color, esc(l)))
    sc.over(s)


def esc(t):
    return (str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


# ---------------------------------------------------------------- output

def render(sc, out_path, pad=16, width_px=1500, title=None):
    """Emit the scene as a standalone SVG, auto-fitting the viewBox."""
    import re
    body = sc.body()
    nums = [float(v) for v in re.findall(r'-?\d+\.?\d*(?=[, ])', '')]  # placeholder, real bounds below
    xs, ys = [], []
    for m in re.finditer(r'(?:points|d)="([^"]+)"', body):
        for pair in re.finditer(r'(-?\d+\.?\d*)[ ,](-?\d+\.?\d*)', m.group(1)):
            xs.append(float(pair.group(1))); ys.append(float(pair.group(2)))
    for m in re.finditer(r'<(?:circle|ellipse)[^>]*cx="(-?\d+\.?\d*)"[^>]*cy="(-?\d+\.?\d*)"[^>]*?(?:r|rx)="(\d+\.?\d*)"', body):
        cx, cy, r = float(m.group(1)), float(m.group(2)), float(m.group(3))
        xs += [cx - r, cx + r]; ys += [cy - r, cy + r]
    for m in re.finditer(r'<rect[^>]*x="(-?\d+\.?\d*)"[^>]*y="(-?\d+\.?\d*)"[^>]*width="(\d+\.?\d*)"[^>]*height="(\d+\.?\d*)"', body):
        x, y, w, h = (float(m.group(i)) for i in (1, 2, 3, 4))
        xs += [x, x + w]; ys += [y, y + h]
    for m in re.finditer(r'<(?:text|line)[^>]*x1?="(-?\d+\.?\d*)"[^>]*y1?="(-?\d+\.?\d*)"', body):
        xs.append(float(m.group(1))); ys.append(float(m.group(2)))
    for m in re.finditer(r'<line[^>]*x2="(-?\d+\.?\d*)"[^>]*y2="(-?\d+\.?\d*)"', body):
        xs.append(float(m.group(1))); ys.append(float(m.group(2)))
    x0, x1 = min(xs) - pad, max(xs) + pad
    y0, y1 = min(ys) - pad, max(ys) + pad
    w, h = x1 - x0, y1 - y0
    head = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%.2f %.2f %.2f %.2f" width="%d" height="%d">'
            % (x0, y0, w, h, width_px, int(width_px * h / w)))
    defs = ('<defs><filter id="soft" x="-30%" y="-30%" width="160%" height="160%">'
            '<feGaussianBlur stdDeviation="1.9"/></filter></defs>')
    bg = '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" style="fill:#ffffff"/>' % (x0, y0, w, h)
    ttl = ''
    if title:
        ttl = ('<text x="%.2f" y="%.2f" style="font-family:Rubik,Arial;font-size:7.5px;font-weight:700;'
               'fill:#5a6674;text-anchor:end">%s</text>' % (x1 - 3, y1 - 3.5, esc(title)))
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(head + defs + bg + body + ttl + '</svg>\n')
    return out_path
