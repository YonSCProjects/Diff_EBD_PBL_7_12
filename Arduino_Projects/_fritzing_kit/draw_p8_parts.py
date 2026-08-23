"""draw_p8_parts.py — generates the custom Fritzing parts Project 8 needs and nobody publishes:
  parts/motor_8520_cw, parts/motor_8520_ccw  (8.5 x 20 mm coreless motors, side view, lead colours per rotation type)
  parts/mosfet_board_4ch                     (hand-soldered perfboard: 4 x IRLB8721 low-side channels — the tutorial's Task 3 layout)
Run from this folder: python draw_p8_parts.py && python normalize_parts.py
All drawings: solid fills + style= attributes only (Qt SVG in the Fritzing CLI drops gradients/opacity)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

def write_part(dirname, moduleid, title, svg, connectors, desc):
    d = os.path.join(HERE, 'parts', dirname); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f'svg.breadboard.{dirname}_breadboard.svg'), 'w', encoding='utf-8').write(svg)
    for v, layer in (('icon', 'icon'), ('schematic', 'schematic'), ('pcb', 'copper0')):
        open(os.path.join(d, f'svg.{v}.{dirname}_{v}.svg'), 'w', encoding='utf-8').write(svg.replace('id="breadboard"', f'id="{layer}"'))
    conns = ''.join(f'''
        <connector id="connector{i}" type="male" name="{n}">
            <description>{n}</description>
            <views>
                <breadboardView><p layer="breadboard" svgId="connector{i}pin"/></breadboardView>
                <schematicView><p layer="schematic" svgId="connector{i}pin"/></schematicView>
                <pcbView><p layer="copper0" svgId="connector{i}pin"/></pcbView>
            </views>
        </connector>''' for i, n in enumerate(connectors))
    fzp = f'''<?xml version="1.0" encoding="UTF-8"?>
<module fritzingVersion="0.9.4" moduleId="{moduleid}">
    <author>Yon (drawn for the Arduino PBL program, 2026)</author>
    <title>{title}</title>
    <label>P</label>
    <date>2026-08-22</date>
    <tags><tag>quadcopter</tag></tags>
    <properties><property name="family">{title}</property></properties>
    <description>{desc}</description>
    <views>
        <iconView><layers image="icon/{dirname}_icon.svg"><layer layerId="icon"/></layers></iconView>
        <schematicView><layers image="schematic/{dirname}_schematic.svg"><layer layerId="schematic"/></layers></schematicView>
        <pcbView><layers image="pcb/{dirname}_pcb.svg"><layer layerId="copper0"/></layers></pcbView>
        <breadboardView><layers image="breadboard/{dirname}_breadboard.svg"><layer layerId="breadboard"/></layers></breadboardView>
    </views>
    <connectors>{conns}
    </connectors>
</module>
'''
    open(os.path.join(d, f'part.{dirname}.fzp'), 'w', encoding='utf-8').write(fzp)
    print('part', dirname, len(connectors), 'connectors')

def pin(i, x, y, w=1.2, h=1.2):
    return f'<rect id="connector{i}pin" x="{x-w/2:.2f}" y="{y-h/2:.2f}" width="{w}" height="{h}" style="fill:none;stroke:none"/>'

def text(x, y, s, size=2.2, fill='#111', weight='bold', anchor='middle'):
    return f'<text x="{x:.2f}" y="{y:.2f}" style="font-family:Arial;font-size:{size}px;font-weight:{weight};fill:{fill};text-anchor:{anchor}">{s}</text>'

# ------------------------------------------------------------ 8520 coreless motor, side view, 1 unit = 1 mm
def motor_svg(lead_a, lead_b):
    W, H = 34.0, 12.0
    s = ['<?xml version="1.0" encoding="UTF-8"?>',
         f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{W/25.4:.4f}in" height="{H/25.4:.4f}in" viewBox="0 0 {W} {H}">',
         '<g id="breadboard">']
    bx, by = 8.0, 1.75
    s.append(f'<rect x="{bx}" y="{by}" width="20" height="8.5" rx="1.2" style="fill:#b9bcc2;stroke:#6f737a;stroke-width:0.35"/>')
    s.append(f'<rect x="{bx}" y="{by+0.9}" width="20" height="2.2" rx="0.8" style="fill:#dfe2e6;stroke:none"/>')
    s.append(f'<rect x="{bx}" y="{by+6.0}" width="20" height="1.6" rx="0.6" style="fill:#8d9096;stroke:none"/>')
    s.append(f'<rect x="{bx+20}" y="{by+3.75}" width="3.2" height="1.0" style="fill:#9a9ca0;stroke:#55585c;stroke-width:0.2"/>')
    s.append(f'<rect x="{bx+19.2}" y="{by+1.2}" width="1.4" height="6.1" rx="0.4" style="fill:#6f737a;stroke:none"/>')
    s.append(text(bx+10, by+5.6, '8520', 2.4, '#3b3e43'))
    s.append(f'<rect x="{bx-0.6}" y="{by+1.4}" width="1.2" height="5.7" rx="0.3" style="fill:#2b2b2b;stroke:none"/>')
    for y, col in ((by+2.8, lead_a), (by+5.7, lead_b)):
        s.append(f'<path d="M {bx-0.4} {y} C {bx-3} {y}, {bx-4} {y+0.2}, 1.6 {y+0.2}" style="fill:none;stroke:{col};stroke-width:0.9;stroke-linecap:round"/>')
        s.append(f'<line x1="1.7" y1="{y+0.2}" x2="0.6" y2="{y+0.2}" style="stroke:#c9c9c9;stroke-width:0.6;stroke-linecap:round"/>')
    s.append(pin(0, 0.8, by+3.0)); s.append(pin(1, 0.8, by+5.9))
    s.append('</g></svg>')
    return '\n'.join(s)

# ------------------------------------------------------------ 4-channel low-side MOSFET board on a 50 x 40 mm perfboard
def board_svg(diode_label='1N5819'):
    W, H = 72.0, 56.0
    s = ['<?xml version="1.0" encoding="UTF-8"?>',
         f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{W/25.4:.4f}in" height="{H/25.4:.4f}in" viewBox="0 0 {W} {H}">',
         '<g id="breadboard">']
    ox, oy = 1.0, 1.0
    s.append(f'<rect x="{ox}" y="{oy}" width="70" height="50" rx="1.2" style="fill:#d9c39a;stroke:#8a6f3c;stroke-width:0.4"/>')
    for r in range(19):
        for c in range(27):
            s.append(f'<circle cx="{ox+2.2+c*2.54:.2f}" cy="{oy+2.2+r*2.54:.2f}" r="0.42" style="fill:#b39a6a;stroke:none"/>')
    yb = oy + 2.2; yg = oy + 2.2 + 18*2.54
    s.append(f'<rect x="{ox+1.0}" y="{yb-0.9:.2f}" width="68" height="1.8" rx="0.5" style="fill:#c97f3e;stroke:#8a4f1c;stroke-width:0.25"/>')
    s.append(f'<rect x="{ox+1.0}" y="{yg-0.9:.2f}" width="68" height="1.8" rx="0.5" style="fill:#c97f3e;stroke:#8a4f1c;stroke-width:0.25"/>')
    s.append(text(ox+4.8, yb+3.4, 'BAT+', 2.0, '#8a1c1c')); s.append(text(ox+4.4, yg-1.6, 'GND', 2.0, '#111'))
    conns = ['BAT+', 'GND']
    s.append(pin(0, ox+2.2, yb)); s.append(pin(1, ox+2.2, yg))
    ci = 2
    for k in range(4):
        cx = ox + 12.5 + k*14.5
        mp_y = yb + 3.0
        s.append(f'<circle cx="{cx-2.54:.2f}" cy="{mp_y:.2f}" r="0.95" style="fill:#e9c46a;stroke:#8a6f3c;stroke-width:0.25"/>')
        s.append(f'<circle cx="{cx+2.54:.2f}" cy="{mp_y:.2f}" r="0.95" style="fill:#e9c46a;stroke:#8a6f3c;stroke-width:0.25"/>')
        s.append(f'<line x1="{cx-2.54:.2f}" y1="{mp_y:.2f}" x2="{cx-2.54:.2f}" y2="{yb:.2f}" style="stroke:#c97f3e;stroke-width:0.6"/>')
        s.append(text(cx, mp_y+3.0, f'M{k+1}', 2.0, '#333'))
        s.append(text(cx-2.54, mp_y-1.4, '+', 1.8, '#8a1c1c')); s.append(text(cx+2.54, mp_y-1.4, '-', 1.8, '#111'))
        s.append(pin(ci, cx-2.54, mp_y)); conns.append(f'M{k+1}+'); ci += 1
        s.append(pin(ci, cx+2.54, mp_y)); conns.append(f'M{k+1}-'); ci += 1
        dx = cx + 4.6
        s.append(f'<line x1="{dx:.2f}" y1="{yb:.2f}" x2="{dx:.2f}" y2="{mp_y+6.5:.2f}" style="stroke:#999;stroke-width:0.5"/>')
        s.append(f'<rect x="{dx-1.1:.2f}" y="{yb+1.6:.2f}" width="2.2" height="4.6" rx="0.5" style="fill:#1d1d1d;stroke:#000;stroke-width:0.2"/>')
        s.append(f'<rect x="{dx-1.1:.2f}" y="{yb+2.0:.2f}" width="2.2" height="0.7" style="fill:#f2f2f2;stroke:none"/>')
        s.append(f'<line x1="{cx+2.54:.2f}" y1="{mp_y+1.0:.2f}" x2="{dx:.2f}" y2="{mp_y+6.5:.2f}" style="stroke:#c97f3e;stroke-width:0.6"/>')
        tx, ty = cx - 5.0, mp_y + 4.2
        s.append(f'<rect x="{tx:.2f}" y="{ty:.2f}" width="10" height="4.0" style="fill:#c8ccd1;stroke:#7d8288;stroke-width:0.3"/>')
        s.append(f'<circle cx="{tx+5:.2f}" cy="{ty+1.8:.2f}" r="1.1" style="fill:#e9ecef;stroke:#7d8288;stroke-width:0.25"/>')
        s.append(f'<rect x="{tx:.2f}" y="{ty+4.0:.2f}" width="10" height="9.5" rx="0.6" style="fill:#1a1a1a;stroke:#000;stroke-width:0.3"/>')
        s.append(text(tx+5, ty+9.2, 'IRLB', 1.9, '#cfcfcf')); s.append(text(tx+5, ty+11.6, '8721', 1.9, '#cfcfcf'))
        for j, lab in enumerate(('G', 'D', 'S')):
            lx = tx + 2.46 + j*2.54
            s.append(f'<rect x="{lx-0.45:.2f}" y="{ty+13.5:.2f}" width="0.9" height="4.2" style="fill:#b5b5b5;stroke:#666;stroke-width:0.2"/>')
            s.append(text(lx, ty+19.3, lab, 1.7, '#333'))
        gx, dxx, sx = tx+2.46, tx+5.0, tx+7.54
        s.append(f'<path d="M {dxx:.2f} {ty+13.6:.2f} L {dxx:.2f} {ty+2.0:.2f} L {cx+2.54:.2f} {ty+2.0:.2f} L {cx+2.54:.2f} {mp_y+1.0:.2f}" style="fill:none;stroke:#c97f3e;stroke-width:0.6"/>')
        s.append(f'<line x1="{sx:.2f}" y1="{ty+17.7:.2f}" x2="{sx:.2f}" y2="{yg:.2f}" style="stroke:#c97f3e;stroke-width:0.6"/>')
        gp_y = yg - 6.0
        s.append(f'<line x1="{gx:.2f}" y1="{ty+17.7:.2f}" x2="{gx:.2f}" y2="{yg:.2f}" style="stroke:#999;stroke-width:0.45"/>')
        s.append(f'<rect x="{gx-0.9:.2f}" y="{ty+20.6:.2f}" width="1.8" height="4.6" rx="0.7" style="fill:#e8d2a8;stroke:#8a6f3c;stroke-width:0.25"/>')
        for j, col in enumerate(('#7b3f00', '#111111', '#ff8c00')):
            s.append(f'<rect x="{gx-0.9:.2f}" y="{ty+21.5+j*1.0:.2f}" width="1.8" height="0.5" style="fill:{col};stroke:none"/>')
        gpx = cx - 7.8
        s.append(f'<circle cx="{gpx:.2f}" cy="{gp_y:.2f}" r="0.95" style="fill:#e9c46a;stroke:#8a6f3c;stroke-width:0.25"/>')
        s.append(f'<line x1="{gpx+1.0:.2f}" y1="{gp_y:.2f}" x2="{gx:.2f}" y2="{gp_y:.2f}" style="stroke:#999;stroke-width:0.45"/>')
        s.append(f'<rect x="{gpx+1.6:.2f}" y="{gp_y-0.9:.2f}" width="4.0" height="1.8" rx="0.7" style="fill:#e8d2a8;stroke:#8a6f3c;stroke-width:0.25"/>')
        for j, col in enumerate(('#7b3f00', '#111111', '#7b3f00')):
            s.append(f'<rect x="{gpx+2.3+j*0.9:.2f}" y="{gp_y-0.9:.2f}" width="0.5" height="1.8" style="fill:{col};stroke:none"/>')
        s.append(text(gpx, gp_y+3.2, f'G{k+1}', 2.0, '#1f5fa8'))
        s.append(pin(ci, gpx, gp_y)); conns.append(f'G{k+1}'); ci += 1
    cxp, cyp = ox+66.2, oy+24
    s.append(f'<rect x="{cxp-2.2:.2f}" y="{cyp-6:.2f}" width="4.4" height="12" rx="1.4" style="fill:#2b2d6b;stroke:#15163a;stroke-width:0.3"/>')
    s.append(f'<rect x="{cxp-2.2:.2f}" y="{cyp-6:.2f}" width="1.2" height="12" rx="0.6" style="fill:#d7d7d7;stroke:none"/>')
    s.append(f'<line x1="{cxp:.2f}" y1="{cyp-6:.2f}" x2="{cxp:.2f}" y2="{yb:.2f}" style="stroke:#999;stroke-width:0.5"/>')
    s.append(f'<line x1="{cxp:.2f}" y1="{cyp+6:.2f}" x2="{cxp:.2f}" y2="{yg:.2f}" style="stroke:#999;stroke-width:0.5"/>')
    s.append(text(cxp, cyp+0.7, 'C', 2.0, '#ffffff'))
    s.append(text(ox+35, oy+53.2, f'4 x IRLB8721 low-side  |  {diode_label} flyback  |  100 ohm gate  |  10k pull-down', 1.6, '#5a4a2a', 'normal'))
    s.append('</g></svg>')
    return '\n'.join(s), conns

if __name__ == '__main__':
    write_part('motor_8520_cw', 'motor_8520_cw_yon_2026', '8520 coreless motor (CW, red/blue leads)', motor_svg('#cc1414', '#2158c7'), ['+', '-'],
               '8.5 x 20 mm coreless brushed motor, clockwise type: red (+) and blue (-) leads.')
    write_part('motor_8520_ccw', 'motor_8520_ccw_yon_2026', '8520 coreless motor (CCW, white/black leads)', motor_svg('#e8e8e8', '#111111'), ['+', '-'],
               '8.5 x 20 mm coreless brushed motor, counter-clockwise type: white (+) and black (-) leads.')
    svg, conns = board_svg()
    write_part('mosfet_board_4ch', 'mosfet_board_4ch_yon_2026', '4-channel MOSFET motor board (IRLB8721, perfboard)', svg, conns,
               'Hand-soldered perfboard with four IRLB8721 low-side switches, flyback Schottky diodes, 100 ohm gate resistors, 10k pull-downs and a bulk capacitor; pads BAT+, GND, M1..M4 +/-, G1..G4.')

# ------------------------------------------------------------ 1S LiPo 1000 mAh pouch with PH2.0 plug (1 unit = 1 mm)
def lipo_svg():
    W, H = 92.0, 36.0
    s = ['<?xml version="1.0" encoding="UTF-8"?>',
         f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{W/25.4:.4f}in" height="{H/25.4:.4f}in" viewBox="0 0 {W} {H}">',
         '<g id="breadboard">']
    px, py, pw, ph = 1.0, 1.0, 52.0, 34.0
    s.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="2.5" style="fill:#b9bec6;stroke:#6f747c;stroke-width:0.5"/>')
    s.append(f'<rect x="{px+1.5}" y="{py+1.5}" width="{pw-3}" height="{ph-3}" rx="2" style="fill:#cfd4db;stroke:none"/>')
    s.append(f'<rect x="{px+6}" y="{py+8}" width="{pw-12}" height="{ph-16}" rx="1.5" style="fill:#f2c744;stroke:#b48a10;stroke-width:0.4"/>')
    s.append(text(px+pw/2, py+16.2, '1S LiPo 3.7 V', 4.2, '#2b2b2b'))
    s.append(text(px+pw/2, py+22.5, '1000 mAh', 4.6, '#2b2b2b'))
    s.append(text(px+pw/2, py+27.2, '25C  ·  PH2.0', 2.6, '#2b2b2b', 'normal'))
    lx = px + pw; ly1, ly2 = py + 14.5, py + 19.5
    s.append(f'<path d="M {lx} {ly1} C {lx+10} {ly1}, {lx+18} {ly1-1}, {lx+26} {ly1-1}" style="fill:none;stroke:#cc1414;stroke-width:1.6;stroke-linecap:round"/>')
    s.append(f'<path d="M {lx} {ly2} C {lx+10} {ly2}, {lx+18} {ly2+1}, {lx+26} {ly2+1}" style="fill:none;stroke:#111111;stroke-width:1.6;stroke-linecap:round"/>')
    # PH2.0 plug (white housing, two pins)
    hx, hy = lx + 26, py + 11.5
    s.append(f'<rect x="{hx}" y="{hy}" width="8" height="10" rx="1" style="fill:#f4f4f4;stroke:#9a9a9a;stroke-width:0.4"/>')
    s.append(f'<rect x="{hx+1.2}" y="{hy+1.2}" width="5.6" height="7.6" rx="0.6" style="fill:#e2e2e2;stroke:none"/>')
    for yy, col in ((ly1-1, '#cc1414'), (ly2+1, '#111111')):
        s.append(f'<rect x="{hx+8}" y="{yy-0.7}" width="3.2" height="1.4" style="fill:#c9a227;stroke:#8a6f10;stroke-width:0.2"/>')
    s.append(text(hx+4, hy-1.5, 'PH2.0', 2.2, '#444', 'normal'))
    s.append(pin(0, hx+10.6, ly1-1)); s.append(pin(1, hx+10.6, ly2+1))
    s.append(text(hx+13.5, ly1-0.2, '+', 2.6, '#cc1414', 'bold', 'start')); s.append(text(hx+13.5, ly2+1.8, '−', 2.6, '#111', 'bold', 'start'))
    s.append('</g></svg>')
    return '\n'.join(s)

# ------------------------------------------------------------ MT3608 boost module (36 x 17 mm), IN pads left, OUT pads right
def mt3608_svg():
    W, H = 40.0, 21.0
    s = ['<?xml version="1.0" encoding="UTF-8"?>',
         f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{W/25.4:.4f}in" height="{H/25.4:.4f}in" viewBox="0 0 {W} {H}">',
         '<g id="breadboard">']
    bx, by, bw, bh = 2.0, 2.0, 36.0, 17.0
    s.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="1.2" style="fill:#1d5fa8;stroke:#0f3a6b;stroke-width:0.45"/>')
    # inductor (black drum) and the blue trimmer with its screw
    s.append(f'<circle cx="{bx+14}" cy="{by+8.5}" r="5.2" style="fill:#1b1b1b;stroke:#000;stroke-width:0.3"/>')
    s.append(text(bx+14, by+9.8, '4R7', 3.0, '#cfcfcf'))
    s.append(f'<rect x="{bx+22.5}" y="{by+3.0}" width="9.5" height="11" rx="0.8" style="fill:#2f6fc4;stroke:#143a6e;stroke-width:0.35"/>')
    s.append(f'<circle cx="{bx+27.25}" cy="{by+6.2}" r="1.6" style="fill:#c9a227;stroke:#6b5410;stroke-width:0.3"/>')
    s.append(f'<line x1="{bx+26.1}" y1="{by+6.2}" x2="{bx+28.4}" y2="{by+6.2}" style="stroke:#6b5410;stroke-width:0.35"/>')
    s.append(text(bx+27.25, by+12.2, 'ADJ', 2.0, '#dfe8f5', 'normal'))
    s.append(f'<rect x="{bx+8.5}" y="{by+1.2}" width="5" height="3" style="fill:#2a2a2a;stroke:none"/>')   # MT3608 chip
    s.append(text(bx+18, by+16.3, 'MT3608 2A step-up', 1.9, '#dfe8f5', 'normal'))
    # pads: IN+ / IN- on the left edge, OUT+ / OUT- on the right edge
    pads = [('Vin', bx+2.0, by+3.0, 'IN+', '#cc1414'), ('GND', bx+2.0, by+14.0, 'IN−', '#111111'),
            ('Vout', bx+bw-2.0, by+3.0, 'OUT+', '#cc1414'), ('GND*', bx+bw-2.0, by+14.0, 'OUT−', '#111111')]
    conns = []
    for i, (name, x, y, lab, col) in enumerate(pads):
        s.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="1.3" style="fill:#e9c46a;stroke:#8a6f3c;stroke-width:0.3"/>')
        s.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="0.55" style="fill:#5a4a2a;stroke:none"/>')
        anchor = 'start' if x < bx + bw/2 else 'end'; tx = x + 2.2 if anchor == 'start' else x - 2.2
        s.append(text(tx, y + 0.9, lab, 2.1, '#ffffff', 'bold', anchor))
        s.append(pin(i, x, y)); conns.append(name)
    s.append('</g></svg>')
    return '\n'.join(s), conns

if __name__ == '__main__':
    write_part('lipo_1s_1000', 'lipo_1s_1000_yon_2026', '1S LiPo 1000 mAh (PH2.0)', lipo_svg(), ['+', '-'],
               '1S 3.7 V 1000 mAh LiPo pouch with a PH2.0 plug: red (+) and black (-).')
    svg, conns = mt3608_svg()
    write_part('mt3608_module', 'mt3608_module_yon_2026', 'MT3608 step-up module', svg, conns,
               'MT3608 2 A boost converter module: IN+ / IN- pads on the left, OUT+ / OUT- on the right, trimmer to set the output.')
