#!/usr/bin/env bash
# build_p4_m3.sh — the seven step figures for P4 T1 M3 (assembling the chassis).
#   bash _blender/build_p4_m3.sh                # Cycles
#   bash _blender/build_p4_m3.sh --eevee        # fast preview
#   bash _blender/build_p4_m3.sh --compose-only # re-label without re-rendering
set -u

BLENDER="${BLENDER:-/c/Users/Yon/tools/blender-4.5.12-windows-x64/blender.exe}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
WORK="$HERE/work"
OUT="$REPO/Arduino_Projects/Project_4_Line_Following_Car/images"
ASSETS="$REPO/Arduino_Projects/Project_4_Line_Following_Car/task_cards_he/assets"

EXTRA=""; SAMPLES="96"; ONLY=""; COMPOSE_ONLY=""
while [ $# -gt 0 ]; do
  case "$1" in
    --eevee) EXTRA="--eevee"; SAMPLES="40" ;;
    --samples) shift; SAMPLES="${1:-96}" ;;
    --compose-only) COMPOSE_ONLY=1 ;;
    s_*) ONLY="$1" ;;
  esac
  shift
done

mkdir -p "$WORK" "$OUT" "$ASSETS"
EMPTY="$WORK/_empty.json"; echo '{"items":[]}' > "$EMPTY"

# one figure per numbered step on the card
STEPS="
s_m3_1_template:w_p4_m3_step1
s_m3_2_cut:w_p4_m3_step2
s_m3_3_holes:w_p4_m3_step3
s_m3_4_motors:w_p4_m3_step4
s_m3_5_wheels:w_p4_m3_step5
s_m3_6_boards:w_p4_m3_step6
s_m3_7_sensors:w_p4_m3_step7
"

for pair in $STEPS; do
  scene="${pair%%:*}"; name="${pair##*:}"
  [ -n "$ONLY" ] && [ "$scene" != "$ONLY" ] && continue
  echo "--- $scene -> $name"
  if [ -z "$COMPOSE_ONLY" ]; then
    "$BLENDER" --background --factory-startup --python "$HERE/render.py" -- \
        "$scene" "$WORK/$name.png" --samples "$SAMPLES" --res 1700x1275 $EXTRA \
        2>&1 | grep -E "RENDERED|Error|Traceback" || true
  elif [ ! -f "$WORK/$name.png" ]; then
    echo "    (no render yet — skipping)"; continue
  fi
  callouts="$HERE/callouts/$scene.json"
  [ -f "$callouts" ] || callouts="$EMPTY"
  node "$HERE/compose.js" "$WORK/$name.png" "$callouts" "$OUT/$name.svg"
  cp "$OUT/$name.svg" "$ASSETS/$name.svg"
done

echo
echo "published into $OUT and $ASSETS"
