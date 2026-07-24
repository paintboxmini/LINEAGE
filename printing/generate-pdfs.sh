#!/usr/bin/env bash
# Converts every card-print-*.html sheet to PDF via headless Chrome, since
# Drew can't reliably open the HTML sheets directly (2026-07-24, mobile).
# Run this after regenerate-cards.py any time the .html sheets change.
#
# Usage: ./generate-pdfs.sh [output-dir]   (default: this directory)

set -euo pipefail
cd "$(dirname "$0")"

CHROME="${CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}"
OUT="${1:-.}"

if [ ! -x "$CHROME" ]; then
  echo "Chrome not found at $CHROME — set CHROME=/path/to/chrome to override." >&2
  exit 1
fi

for f in card-print-*.html; do
  name="${f%.html}"
  "$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
    --print-to-pdf="$OUT/$name.pdf" "file://$(pwd)/$f" 2>/dev/null
  echo "$name.pdf"
done
