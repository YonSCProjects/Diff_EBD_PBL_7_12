"""make_fzz.py <spec.json> <out.fzz>

Builds a Fritzing .fzz sketch from a figure spec, bundling any community part
(fzp + svg files from ./parts/<name>/) inside the archive so Fritzing — GUI or
CLI export — can load it without installing parts.

spec.instances[] = {
  "id": "esp",                       # short handle used by wires/labels
  "part": "<dir under parts/>"       # community part (bundled), OR
  "core": "<fzp basename in fritzing-parts/core>"   # built-in part
  "x": 100, "y": 100,                # breadboard-view position, px (90 px = 1 in)
  "title": "ESP32",                  # instance title shown in Fritzing
  "rotation": 0                      # optional, degrees CW; pivot = part origin (see below)
}
"""
import json, os, sys, zipfile, re, glob, math

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = os.path.join(HERE, 'parts')
CORE = os.environ.get('FRITZING_PATH', 'C:/Program Files/Fritzing') + '/fritzing-parts/core'

def main(spec_path, out):
    spec = json.load(open(spec_path, encoding='utf-8'))
    inst_xml, bundle = [], {}
    for i, ins in enumerate(spec['instances']):
        mi = 1001 + i
        ins['modelIndex'] = mi
        if 'part' in ins:
            d = os.path.join(PARTS, ins['part'])
            fzp = glob.glob(os.path.join(d, 'part.*.fzp'))[0]
            for f in os.listdir(d):
                if f.startswith('part.') or f.startswith('svg.'):
                    bundle[f] = os.path.join(d, f)
            path = os.path.basename(fzp)
        else:
            fzp = os.path.join(CORE, ins['core'] + '.fzp')
            path = fzp.replace(chr(92), '/')
        txt = open(fzp, encoding='utf-8').read()
        mid = re.search(r'moduleId=["\']([^"\']+)["\']', txt).group(1)
        x, y = ins['x'], ins['y']
        title = ins.get('title', ins.get('part', ins.get('core')))
        rot = ins.get('rotation', 0)
        tr = ''
        if rot:
            # pivot = the part's own origin (top-left of its unrotated SVG). A part rotated
            # 180 deg therefore occupies (x - w, y - h) .. (x, y); 90 deg: (x - h, y) .. (x, y + w).
            a = math.radians(rot); c, s = math.cos(a), math.sin(a)
            tr = f'<transform m11="{c:.6f}" m12="{s:.6f}" m13="0" m21="{-s:.6f}" m22="{c:.6f}" m23="0" m31="0" m32="0" m33="1" />'
        props = ''.join(f'<property name="{k}" value="{v}" />' for k, v in ins.get('properties', {}).items())
        inst_xml.append(
            f'<instance moduleIdRef="{mid}" modelIndex="{mi}" path="{path}">{props}<title>{title}</title><views>'
            f'<breadboardView layer="breadboard"><geometry z="{ins.get("z", 2.5)}" x="{x}" y="{y}">{tr}</geometry></breadboardView>'
            f'<schematicView layer="schematic"><geometry z="2.5" x="{x}" y="{y}" /></schematicView>'
            f'<pcbView layer="copper0"><geometry z="2.5" x="{x}" y="{y}" /></pcbView></views></instance>')
    fz = f'''<?xml version='1.0' encoding='utf-8'?>
<module fritzingVersion="1.0.3" icon=".png">
    <project_properties />
    <boards>
        <board moduleId="pcb-arduino-r3-shield" title="Arduino Shield PCB" instance="PCB1" width="6.88566cm" height="5.36311cm" />
    </boards>
    <views>
        <view name="breadboardView" backgroundColor="#ffffff" gridSize="0.1in" showGrid="1" alignToGrid="0" viewFromBelow="0" />
        <view name="schematicView" backgroundColor="#ffffff" gridSize="0.1in" showGrid="1" alignToGrid="1" viewFromBelow="0" />
        <view name="pcbView" backgroundColor="#333333" gridSize="0.05in" showGrid="1" alignToGrid="1" viewFromBelow="0" />
    </views>
    <instances>
    {''.join(inst_xml)}
    </instances>
</module>
'''
    base = os.path.splitext(os.path.basename(out))[0]
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr(base + '.fz', fz)
        for name, p in bundle.items():
            z.write(p, name)
    print('wrote', out, '| instances', len(inst_xml), '| bundled files', len(bundle))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
