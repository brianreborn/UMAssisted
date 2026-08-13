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
# No uiautomator dump: confirmed the client is one opaque unitySurfaceView, so every
# .uixml ever captured was an empty FrameLayout/LinearLayout shell with zero game
# content — not worth the extra file.
echo "saved $OUT"
# quick package check
adb shell dumpsys window 2>/dev/null | grep -E 'mCurrentFocus|mFocusedApp' | head -3
