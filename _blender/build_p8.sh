#!/usr/bin/env bash
# build_p8.sh — render every Project 8 step figure, composite its Hebrew callouts, and publish
# it OVER the filename the cards already reference. Publishing under a new name means the cards
# keep showing the old SVG and none of the work is visible — that failure has happened here once
# already, so the publish map below is the load-bearing part of this file.
#
#   bash _blender/build_p8.sh                 # Cycles, full quality
#   bash _blender/build_p8.sh --eevee         # fast preview
#   bash _blender/build_p8.sh s_p8_thrust     # just one scene
#   bash _blender/build_p8.sh --compose-only  # re-label without re-rendering
set -u
failed=0

BLENDER="${BLENDER:-/c/Users/Yon/tools/blender-4.5.12-windows-x64/blender.exe}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
WORK="$HERE/work"
OUT="$REPO/Arduino_Projects/Project_8_Tiny_Quadcopter/images"
ASSETS="$REPO/Arduino_Projects/Project_8_Tiny_Quadcopter/task_cards_he/assets"

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
s_p8_parts:w_p8_s01_parts_contract
s_p8_press_fit:w_p8_s02_press_fit_motors
s_p8_meet_board:w_p8_s03_meet_mosfet_board
s_p8_mount:w_p8_s04_mount_electronics
s_p8_power_tree:w_p8_s05_power_tree
s_p8_motor_wiring:w_p8_s06_motor_wiring
s_p8_signal_wiring:w_p8_s07_signal_wiring
s_p8_pre_power:w_p8_s08_pre_power_check
s_p8_upload_test:w_p8_s09_upload_motor_test
s_p8_spin:w_p8_s10_spin_no_props
s_p8_thrust:w_p8_s11_thrust_test
s_p8_upload_flight:w_p8_s12_upload_flight
s_p8_hover:w_p8_s13_tethered_hover
s_p8_post_flight:w_p8_s14_post_flight
s_p8_t2_startup:w_p8_t2_s01_startup
s_p8_t2_solder1:w_p8_t2_s02_solder_channel_1
s_p8_t2_check1:w_p8_t2_s03_check_channel_1
s_p8_t2_solder24:w_p8_t2_s04_solder_channels_2_4
s_p8_t2_tune:w_p8_t2_s05_tune_mt3608
s_p8_t2_mount:w_p8_t2_s06_mount_and_wire
s_p8_t2_pre_power:w_p8_t2_s07_pre_power_check
s_p8_t2_spin:w_p8_t2_s08_upload_and_spin
s_p8_t2_thrust:w_p8_t2_s09_thrust_test
s_p8_t2_choices:w_p8_t2_s10_choices_and_claude
s_p8_t2_hover:w_p8_t2_s11_tethered_hover_tuning
s_p8_t2_sequence:w_p8_t2_s12_flight_sequence
s_p8_t2_signature:w_p8_t2_s13_signature_flight
s_p8_t3_planner:w_p8_t3_planner
"

EMPTY="$WORK/_empty.json"
echo '{"items":[]}' > "$EMPTY"

for pair in $PUBLISH; do
  scene="${pair%%:*}"; name="${pair##*:}"
  [ -n "$ONLY" ] && [ "$scene" != "$ONLY" ] && continue
  echo "--- $scene -> $name"
  if [ -z "$COMPOSE_ONLY" ]; then
    rm -f "$WORK/$name.png" "$WORK/$name.anchors.json"
    "$BLENDER" --background --factory-startup --python "$HERE/render.py" -- \
        "$scene" "$WORK/$name.png" --samples "$SAMPLES" --res 1800x1350 $EXTRA \
        > "$WORK/$name.render.log" 2>&1
    rc=$?
    grep -hE "RENDERED|OCCLUDED|Error|Traceback" "$WORK/$name.render.log" || true
    if [ $rc -ne 0 ] || [ ! -f "$WORK/$name.png" ]; then
      echo "FAILED to render $scene (rc=$rc) — see $WORK/$name.render.log"
      echo "  NOT publishing $name: the old figure stays in place rather than being"
      echo "  overwritten by a re-composite of the previous run's PNG."
      failed=$((failed+1)); continue
    fi
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
[ "$failed" -eq 0 ] || echo "$failed figure(s) FAILED and were not published."
exit $(( failed > 0 ? 1 : 0 ))
echo "now rebuild the bundle:  node build_cards_only.js he 8"
