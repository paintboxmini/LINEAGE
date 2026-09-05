#!/usr/bin/env bash
# Regenerate EVERY print artifact and report what actually changed.
#
# Why this exists: three Sync passes running, the only stale thing found was a
# card sheet — and every time the miss had the same shape. The session had been
# a rules edit (a keyword rename, a duplicate cleanup, a consumables rescope)
# that touched cards/ or items/ incidentally, the rules PDFs got regenerated
# because those were the artifact in mind, and the card sheets fed by the same
# files were forgotten. Reasoning about "which sheets should have moved" has now
# failed three for three. Rebuilding everything and diffing has caught it three
# for three. So: stop reasoning, run this.
#
# Usage:
#   ./generate-all.sh          → rebuild everything, report changes
#   ./generate-all.sh --check  → same, but exit 1 if anything was stale (CI-ish)

set -uo pipefail
cd "$(dirname "$0")"

CHECK=0
[ "${1:-}" = "--check" ] && CHECK=1

CARD_SETS=(core briarwatch mason frost steele oracle items items-field washed-ashore)
RULES_DOCS=(packet)
CHROME="${CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}"

echo "Regenerating card sheets..."
for s in "${CARD_SETS[@]}"; do
  python3 generate-cards.py "$s" >/dev/null 2>&1 || { echo "  FAILED: $s"; exit 1; }
done

echo "Regenerating rules documents..."
for d in "${RULES_DOCS[@]}"; do
  python3 generate-rules-pdf.py "$d" >/dev/null 2>&1 || { echo "  FAILED: $d"; exit 1; }
done

# Which HTML actually moved? Only rebuild PDFs for those — a Chrome launch each
# is the slow part, and an unchanged sheet doesn't need one.
mapfile -t CHANGED < <(git status --porcelain -- '*.html' | awk '{print $2}')

if [ ${#CHANGED[@]} -eq 0 ]; then
  echo
  echo "Everything already current — nothing was stale."
  exit 0
fi

echo
echo "STALE — these were out of date and have been rebuilt:"
for f in "${CHANGED[@]}"; do echo "  $(basename "$f")"; done

# Regenerate only the PDFs that (a) already exist and (b) whose HTML changed.
echo
echo "Rebuilding affected PDFs..."
for f in "${CHANGED[@]}"; do
  base="$(basename "$f" .html)"
  [ -f "$base.pdf" ] || continue
  if [ ! -x "$CHROME" ]; then
    echo "  ! Chrome not found at $CHROME — skipped $base.pdf"
    continue
  fi
  "$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
    --print-to-pdf="$base.pdf" "file://$(pwd)/$base.html" 2>/dev/null
  echo "  $base.pdf"
done

echo
echo "Done. Review the diff before committing."
[ "$CHECK" -eq 1 ] && exit 1
exit 0
