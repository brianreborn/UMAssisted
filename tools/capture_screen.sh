#!/bin/sh
# Passive screenshot: no input injection. Usage: capture_screen.sh <label>
# Saves under screenshots/<subdir or misc>/<timestamp>_<label>.png
set -e
export PATH="${HOME}/japanglify/sdk/platform-tools:${PATH}"
LABEL="${1:-screen}"
SUB="${2:-misc}"
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
DIR="${ROOT}/screenshots/${SUB}"
mkdir -p "$DIR"
TS="$(date +%Y%m%d_%H%M%S)"
OUT="${DIR}/${TS}_${LABEL}.png"
REMOTE="/sdcard/uma_cap_${TS}.png"
adb shell screencap -p "$REMOTE"
adb pull "$REMOTE" "$OUT" >/dev/null
adb shell rm -f "$REMOTE" 2>/dev/null || true
# also dump uiautomator (passive) next to it
DUMP="${DIR}/${TS}_${LABEL}.uixml"
adb shell uiautomator dump /sdcard/uma_ui.xml 2>/dev/null || true
adb pull /sdcard/uma_ui.xml "$DUMP" 2>/dev/null || true
adb shell rm -f /sdcard/uma_ui.xml 2>/dev/null || true
echo "saved $OUT"
# quick package check
adb shell dumpsys window 2>/dev/null | grep -E 'mCurrentFocus|mFocusedApp' | head -3
