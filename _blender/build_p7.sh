#!/usr/bin/env bash
# build_p7.sh — render every Project 7 step figure, composite its Hebrew callouts, and publish
# it OVER the filename the cards already reference. Publishing under a new name means the cards
# keep showing the old SVG and none of the work is visible — that failure has happened here once
# already, so the publish map below is the load-bearing part of this file.
#
#   bash _blender/build_p7.sh                 # Cycles, full quality
#   bash _blender/build_p7.sh --eevee         # fast preview
#   bash _blender/build_p7.sh s_power_rails   # just one scene
#   bash _blender/build_p7.sh --compose-only  # re-label without re-rendering
set -u

BLENDER="${BLENDER:-/c/Users/Yon/tools/blender-4.5.12-windows-x64/blender.exe}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
WORK="$HERE/work"
OUT="$REPO/Arduino_Projects/Project_7_Camera_Explorer/images"
ASSETS="$REPO/Arduino_Projects/Project_7_Camera_Explorer/task_cards_he/assets"

EXTRA=""; SAMPLES="96"; ONLY=""; COMPOSE_ONLY=""
while [ $# -gt 0 ]; do
  case "$1" in
    --eevee) EXTRA="--eevee"; SAMPLES="48" ;;
    --samples) shift; SAMPLES="${1:-96}" ;;
    --compose-only) COMPOSE_ONLY=1 ;;
    s_*) ONLY="$1" ;;
  esac
  shift
done

mkdir -p "$WORK" "$OUT" "$ASSETS"

# blender scene  ->  the figure name the cards embed
PUBLISH="
s_ftdi_upload:w_p7_s01_ftdi_upload
s_upload_ritual:w_p7_s02_upload_ritual
s_first_stream:w_p7_s03_first_stream
s_mount_camera:w_p7_s04_mount_camera
s_power_rails:w_p7_s05_power_rails
s_cam_to_driver:w_p7_s06_cam_to_driver
s_drive_from_page:w_p7_s07_drive_from_page
s_drive_by_video:w_p7_s08_drive_by_video
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
echo "now rebuild the bundle:  node build_cards_only.js he 7"
