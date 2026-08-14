#!/bin/sh
# Passive screenshot: no input injection. Usage: capture_screen.sh <label>
# Saves under screenshots/<subdir or misc>/<timestamp>_<label>.png
if [ -n "${ANDROID_HOME}" ] && [ -d "${ANDROID_HOME}/platform-tools" ]; then
    export PATH="${ANDROID_HOME}/platform-tools:${PATH}"
elif [ -n "${ANDROID_SDK_ROOT}" ] && [ -d "${ANDROID_SDK_ROOT}/platform-tools" ]; then
    export PATH="${ANDROID_SDK_ROOT}/platform-tools:${PATH}"
elif [ -d "${HOME}/japanglify/sdk/platform-tools" ]; then
    export PATH="${HOME}/japanglify/sdk/platform-tools:${PATH}"
fi

if ! command -v adb >/dev/null 2>&1; then
    echo "ERROR: adb executable not found in PATH or Android SDK platform-tools." >&2
    exit 1
fi
LABEL="${1:-screen}"
SUB="${2:-misc}"
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
DIR="${ROOT}/screenshots/${SUB}"
mkdir -p "$DIR"
TS="$(date +%Y%m%d_%H%M%S)"
OUT="${DIR}/${TS}_${LABEL}.jpg"
TMP_PNG="/tmp/screencap_${TS}.png"

# Fast single-command stream (exec-out) with fallback to remote screencap + pull if needed
if adb exec-out screencap -p > "$TMP_PNG" 2>/dev/null && [ -s "$TMP_PNG" ]; then
    :
else
    REMOTE="/sdcard/uma_cap_${TS}.png"
    adb shell screencap -p "$REMOTE"
    adb pull "$REMOTE" "$TMP_PNG" >/dev/null
    adb shell rm -f "$REMOTE" 2>/dev/null || true
fi

if command -v ffmpeg >/dev/null 2>&1; then
    ffmpeg -y -i "$TMP_PNG" -vf scale=iw/2:ih/2 -q:v 6 "$OUT" >/dev/null 2>&1
    rm -f "$TMP_PNG"
else
    mv "$TMP_PNG" "${DIR}/${TS}_${LABEL}.png"
    OUT="${DIR}/${TS}_${LABEL}.png"
fi

# No uiautomator dump: confirmed the client is one opaque unitySurfaceView, so every
# .uixml ever captured was an empty FrameLayout/LinearLayout shell with zero game
# content — not worth the extra file.
echo "saved $OUT"
# quick package check
adb shell dumpsys window 2>/dev/null | grep -E 'mCurrentFocus|mFocusedApp' | head -3

