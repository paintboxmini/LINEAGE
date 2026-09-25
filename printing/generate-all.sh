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

CARD_SETS=(core briarwatch mason oracle oracle-1 oracle-2 oracle-3 oracle-expansion items items-field washed-ashore)
RULES_DOCS=(packet play-reference)

# Which sheets get a PDF. The PDFs are **not** in git — they are build
# output and regenerating them from the markdown is the whole point of this
# script (see README.md in this directory). So this list is what says a PDF
# should exist at all; before the PDFs were untracked the answer was
# "whichever ones happen to be sitting here", which is not an answer.
#
# Four sheets are deliberately not here — briarwatch, mason, items and
# items-field. They have never had a PDF. Add them if you want them; the
# only cost is a Chrome launch each.
PDF_SHEETS=(card-print-core card-print-oracle card-print-oracle-1
            card-print-oracle-2 card-print-oracle-3
            card-print-oracle-expansion card-print-washed-ashore
            character-sheets packet play-reference
            simulator-narrated-cards)

CHROME="${CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}"

echo "Regenerating card sheets..."
for s in "${CARD_SETS[@]}"; do
  python3 generate-cards.py "$s" >/dev/null 2>&1 || { echo "  FAILED: $s"; exit 1; }
done

echo "Regenerating rules documents..."
for d in "${RULES_DOCS[@]}"; do
  python3 generate-rules-pdf.py "$d" >/dev/null 2>&1 || { echo "  FAILED: $d"; exit 1; }
done

# Character sheets recompute HP, hand size, initiative and deck maximum from
# each character's stat table, so a stat change has to come back through here.
echo "Regenerating character sheets..."
python3 generate-sheets.py >/dev/null 2>&1 || { echo "  FAILED: character sheets"; exit 1; }

# Which HTML actually moved? Only rebuild PDFs for those — a Chrome launch each
# is the slow part, and an unchanged sheet doesn't need one.
#
# This used to ask git, which only worked because the HTML was committed. It
# is build output now and is not, so the comparison is against manifest.txt —
# the tracked record of what every artifact last hashed to. Same check, one
# readable line per sheet instead of eight thousand lines of markup, and it
# no longer depends on the working tree being clean to be meaningful.
BEFORE="$(mktemp)"; AFTER="$(mktemp)"
trap 'rm -f "$BEFORE" "$AFTER"' EXIT
[ -f manifest.txt ] && cp manifest.txt "$BEFORE" || : > "$BEFORE"
python3 manifest.py --print > "$AFTER"

mapfile -t CHANGED < <(
  diff --changed-group-format='%>' --unchanged-group-format='' \
       "$BEFORE" "$AFTER" 2>/dev/null | awk '!/^#/ && NF {print $1 ".html"}')

# The HTML is no longer the whole input. Cards reference fonts and stock
# textures out of assets/, so an asset can change while every .html stays
# byte-identical and the PDFs are quietly stale — which is exactly what
# happened the first time the colour wash was restrengthened. If any asset
# moved, every PDF is suspect.
if [ -n "$(git status --porcelain -- assets)" ]; then
  echo
  echo "Assets changed — rebuilding every PDF, not just changed HTML."
  mapfile -t CHANGED < <(ls *.html)
fi

if [ ${#CHANGED[@]} -eq 0 ]; then
  echo
  echo "HTML already current — nothing was stale."
else
  echo
  echo "STALE — these were out of date and have been rebuilt:"
  for f in "${CHANGED[@]}"; do echo "  $(basename "$f")"; done
fi

# A PDF is rebuilt when its HTML moved, or when it simply is not there —
# which on a fresh clone is all of them, since the PDFs are build output
# and are not committed.
NEED=()
for base in "${PDF_SHEETS[@]}"; do
  [ -f "$base.html" ] || { echo "  ! no $base.html to build from"; continue; }
  if [ ! -f "$base.pdf" ]; then
    NEED+=("$base")
    continue
  fi
  for f in "${CHANGED[@]}"; do
    if [ "$(basename "$f" .html)" = "$base" ]; then NEED+=("$base"); break; fi
  done
done

if [ ${#NEED[@]} -gt 0 ]; then
  echo
  echo "Building PDFs..."
  if [ ! -x "$CHROME" ]; then
    echo "  ! Chrome not found at $CHROME — set CHROME=/path/to/chrome." >&2
    echo "  ! ${#NEED[@]} PDF(s) not built." >&2
    exit 2
  fi
  for base in "${NEED[@]}"; do
    "$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
      --print-to-pdf="$base.pdf" "file://$(pwd)/$base.html" 2>/dev/null
    echo "  $base.pdf"
  done
else
  echo
  echo "Every PDF is present and current."
fi

python3 manifest.py >/dev/null
echo
echo "Done. Neither the HTML nor the PDFs are tracked — commit manifest.txt."
# --check is about the committed record, which is manifest.txt. A missing
# PDF is the normal state of a fresh clone, not a finding.
if [ "$CHECK" -eq 1 ] && [ ${#CHANGED[@]} -gt 0 ]; then exit 1; fi
exit 0
