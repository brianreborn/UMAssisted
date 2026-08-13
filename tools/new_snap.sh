#!/bin/sh
# Helper: after you take a screenshot (via capture_screen.sh or device system screenshot),
# this creates a skeleton .labels.txt and prints a SESSION_NOTES row template.
#
# Usage:
#   ./tools/new_snap.sh <path-to-png> "space separated labels"
#
# Example:
#   ./tools/new_snap.sh screenshots/shop/20260812_..._shop_list.png "shop_list low_energy unity_cup aoharu_hai"
#
# It does NOT capture — it only helps with the hygiene after you have the file.

set -e

PNG="$1"
LABELS="$2"

if [ -z "$PNG" ] || [ -z "$LABELS" ]; then
  echo "Usage: $0 <png-path> \"label1 label2 ...\""
  exit 1
fi

if [ ! -f "$PNG" ]; then
  echo "File not found: $PNG"
  exit 1
fi

DIR=$(dirname "$PNG")
BASE=$(basename "$PNG" .png)
LABELFILE="${DIR}/${BASE}.labels.txt"

# Create labels file (one line)
printf "%s\n" "$LABELS" > "$LABELFILE"
echo "Created $LABELFILE"

# Print SESSION_NOTES row template (user should fill the description)
TS=$(echo "$BASE" | cut -d_ -f1-2)
FNAME=$(echo "$BASE" | cut -d_ -f3-)
SUB=$(basename "$DIR")

echo
echo "=== Add this row to screenshots/SESSION_NOTES.md (fill in the description) ==="
echo "| \`${SUB}/${BASE}.png\` | **TODO: short title** (e.g. Shop list, low energy); details... Unity Cup / Aoharu Hai. |"
echo
echo "After editing the labels file and notes, run:"
echo "  git status"
echo "  # then commit when ready"
