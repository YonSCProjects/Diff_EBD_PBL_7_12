"""normalize_parts.py — make every part under ./parts/ CLI-safe: file names,
fzp image references and moduleIds must not contain spaces (the Fritzing CLI
silently drops bundled parts whose svg file names contain spaces)."""
import os, re, glob
HERE = os.path.dirname(os.path.abspath(__file__))
for d in sorted(glob.glob(os.path.join(HERE, 'parts', '*'))):
    if not os.path.isdir(d): continue
    fzp = glob.glob(os.path.join(d, 'part.*.fzp'))[0]
    txt = open(fzp, encoding='utf-8').read()
    changed = False
    for f in os.listdir(d):
        if ' ' in f:
            nf = f.replace(' ', '_')
            os.rename(os.path.join(d, f), os.path.join(d, nf))
            if f.startswith('part.'): fzp = os.path.join(d, nf)
            changed = True
    new = re.sub(r'image="([^"]*)"', lambda m: 'image="%s"' % m.group(1).replace(' ', '_'), txt)
    new = re.sub(r'moduleId=(["\'])([^"\']*)\1', lambda m: 'moduleId=%s%s%s' % (m.group(1), m.group(2).replace(' ', '_'), m.group(1)), new)
    if new != txt:
        open(fzp, 'w', encoding='utf-8').write(new); changed = True
    print(('normalized ' if changed else 'ok         ') + os.path.basename(d))

# --- second pass: every breadboard SVG needs a <g id="breadboard"> layer group,
# otherwise the Fritzing CLI export silently omits the part.
for svg in glob.glob(os.path.join(HERE, 'parts', '*', 'svg.breadboard.*.svg')):
    s = open(svg, encoding='utf-8').read()
    if 'id="breadboard"' in s: continue
    m = re.search(r'<svg\b[^>]*>', s)
    end = s.rfind('</svg>')
    s = s[:m.end()] + '\n<g id="breadboard">' + s[m.end():end] + '</g>\n' + s[end:]
    open(svg, 'w', encoding='utf-8').write(s)
    print('wrapped breadboard layer:', os.path.basename(os.path.dirname(svg)))
