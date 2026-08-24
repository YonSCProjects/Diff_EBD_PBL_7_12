#!/usr/bin/env bash
# preview.sh — fast EEVEE previews of any list of scenes, tiled into one contact sheet.
# The point is a tight look-and-fix loop: a Cycles frame costs about a minute, a preview
# about fifteen seconds, and composition mistakes are visible at either quality.
#
#   bash _blender/preview.sh s_wiring s_track          # two scenes -> work/_sheet.png
#   COLS=2 RES=1100x825 bash _blender/preview.sh s_hero
set -u
BLENDER="${BLENDER:-/c/Users/Yon/tools/blender-4.5.12-windows-x64/blender.exe}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="$HERE/work/preview"
RES="${RES:-900x675}"
COLS="${COLS:-3}"
mkdir -p "$WORK"

LIST=""
for s in "$@"; do
  echo "--- $s"
  "$BLENDER" --background --factory-startup --python "$HERE/render.py" -- \
      "$s" "$WORK/$s.png" --eevee --samples 24 --res "$RES" \
      2>&1 | grep -E "RENDERED|Error|Traceback|no such scene" || true
  LIST="$LIST $s"
done

python - "$WORK" "$COLS" $LIST <<'PY'
import sys, os
from PIL import Image
work, cols = sys.argv[1], int(sys.argv[2])
names = sys.argv[3:]
tw, th = 620, 465
rows = (len(names) + cols - 1) // cols
sheet = Image.new('RGB', (tw * min(cols, len(names)), th * rows), (255, 255, 255))
for i, n in enumerate(names):
    f = os.path.join(work, n + '.png')
    if not os.path.exists(f):
        continue
    im = Image.open(f).convert('RGBA')
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    sheet.paste(bg.convert('RGB').resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
out = os.path.join(os.path.dirname(work), '_sheet.png')
sheet.save(out)
print('sheet:', out)
PY
