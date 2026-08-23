#!/usr/bin/env bash
# build_p4.sh — render every Project 4 step figure, composite its Hebrew callouts, and publish
# it OVER the filename the cards already reference. Publishing under a new name means the cards
# keep showing the old SVG and none of the work is visible, which is exactly what happened once.
#
#   bash _blender/build_p4.sh                 # Cycles, full quality
#   bash _blender/build_p4.sh --eevee         # fast preview
#   bash _blender/build_p4.sh s_wiring        # just one scene
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
    --eevee) EXTRA="--eevee"; SAMPLES="48" ;;
    --samples) shift; SAMPLES="${1:-96}" ;;
    # re-label without re-rendering: the reason the render is hardware-only and the Hebrew is
    # composited afterwards. A wording change costs seconds instead of a minute a frame.
    --compose-only) COMPOSE_ONLY=1 ;;
    s_*) ONLY="$1" ;;
  esac
  shift
done

mkdir -p "$WORK" "$OUT" "$ASSETS"

# blender scene  ->  the figure name the cards embed
PUBLISH="
s_soldering_station:w_p4_s01_soldering_station
s_solder_motor_leads:w_p4_s02_solder_motor_leads
s_cut_plate:w_p4_s03a_cut_plate
s_glue_motors:w_p4_s03b_glue_motors
s_wheels_on:w_p4_s03c_wheels_on
s_wiring:w_p4_s04_wiring
s_wheels_in_air:w_p4_s05_wheels_in_air
s_sensor_test:w_p4_s06_sensor_test
s_track:w_p4_s07_track
s_first_run:w_p4_s08_first_run
"

EMPTY="$WORK/_empty.json"
echo '{"items":[]}' > "$EMPTY"

for pair in $PUBLISH; do
  scene="${pair%%:*}"; name="${pair##*:}"
  [ -n "$ONLY" ] && [ "$scene" != "$ONLY" ] && continue
  echo "--- $scene -> $name"
  if [ -z "$COMPOSE_ONLY" ]; then
    "$BLENDER" --background --factory-startup --python "$HERE/render.py" -- \
        "$scene" "$WORK/$name.png" --samples "$SAMPLES" --res 1800x1350 $EXTRA \
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
echo "now rebuild the bundle:  node build_cards_only.js he 4"
