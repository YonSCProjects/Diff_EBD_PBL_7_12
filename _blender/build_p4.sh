#!/usr/bin/env bash
# build_p4.sh — render every Project 4 step figure and composite its Hebrew callouts.
#   bash _blender/build_p4.sh            # Cycles, full quality
#   bash _blender/build_p4.sh --eevee    # fast preview
set -u

BLENDER="${BLENDER:-/c/Users/Yon/tools/blender-4.5.12-windows-x64/blender.exe}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
WORK="$HERE/work"
OUT="$REPO/Arduino_Projects/Project_4_Line_Following_Car/images"
ASSETS="$REPO/Arduino_Projects/Project_4_Line_Following_Car/task_cards_he/assets"

EXTRA=""
SAMPLES="96"
for a in "$@"; do
  case "$a" in
    --eevee) EXTRA="--eevee"; SAMPLES="48" ;;
    --samples) shift; SAMPLES="${1:-96}" ;;
  esac
done

mkdir -p "$WORK" "$OUT" "$ASSETS"

# scene            -> published figure name
SCENES="
s_cut_plate:w_p4_r01_cut_plate
s_glue_motors:w_p4_r02_glue_motors
s_wheels_on:w_p4_r03_wheels_on
s_wiring:w_p4_r04_wiring
s_wheels_in_air:w_p4_r05_wheels_in_air
s_sensor_test:w_p4_r06_sensor_test
s_first_run:w_p4_r07_first_run
"

for pair in $SCENES; do
  scene="${pair%%:*}"; name="${pair##*:}"
  echo "--- $scene -> $name"
  "$BLENDER" --background --factory-startup --python "$HERE/render.py" -- \
      "$scene" "$WORK/$name.png" --samples "$SAMPLES" --res 1800x1350 $EXTRA \
      2>&1 | grep -E "RENDERED|Error|Traceback" || true
  callouts="$HERE/callouts/$scene.json"
  if [ -f "$callouts" ]; then
    node "$HERE/compose.js" "$WORK/$name.png" "$callouts" "$OUT/$name.svg"
  else
    echo "    (no callouts yet — publishing the bare render)"
    node "$HERE/compose.js" "$WORK/$name.png" <(echo '{"items":[]}') "$OUT/$name.svg"
  fi
  cp "$OUT/$name.svg" "$ASSETS/$name.svg"
done

echo "done -> $OUT"
