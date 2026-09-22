# printing

Turns the markdown into things you can hold: card sheets, character sheets,
and the two rules documents. **The markdown is the source** — nothing in
here is edited by hand except the scripts themselves.

## Building everything

```
./generate-all.sh            # rebuild every artifact, report what moved
./generate-all.sh --check    # same, but exit 1 if any HTML was stale
```

That is the whole workflow. It regenerates the HTML from `cards/`, `rules/`
and `characters/`, then builds a PDF for anything whose HTML changed or
whose PDF is missing.

**It needs headless Chrome for the PDF step**, and nothing else — the
Python is standard library only, same as `combat-simulations/`. Point it
somewhere if the default is wrong:

```
CHROME=/path/to/chrome ./generate-all.sh
```

Without Chrome the HTML still regenerates and the script says which PDFs it
could not build, exiting 2. The HTML sheets print acceptably from a browser
if you need a sheet and have no Chrome to script.

## PDF format conventions — the part the repo actually needs to keep

**Drew's workflow, stated 2026-09-22: the PDFs get generated in chat, not here.** He is on a phone and has no terminal, so `./generate-all.sh` is something an agent runs, never him. **What this repo has to preserve is the recipe**, so that a PDF built in a chat session six months from now comes out looking like the ones built today.

*Everything below is the recipe. None of it needs a shell to read.*

### Which generator makes what

| Generator | Produces | From |
|---|---|---|
| `generate-cards.py` | the card sheets, 3×3 to a page for sleeves | `cards/`, seated set lists in the script |
| `generate-sheets.py` | `character-sheets.html` | `characters/` |
| `generate-rules-pdf.py` | any `rules/*.md` as a flowing document | `rules/` |
| `generate-blanks.py` | blank card stock | nothing — it is geometry |
| `make-grain.py` | the paper texture, once | nothing — it is noise |

**`generate-rules-pdf.py` takes a bare filename** and will take a stem as well — the items catalog answers to either spelling.

### Print settings — these three, every time

**Margins = None. Background graphics = On. Scale = 100%.** *The script prints them on every run for a reason: background graphics off loses every card border and the paper texture, and any scale but 100% breaks the sleeve fit that `card-styling-notes.md` measured.*

### The headless Chrome invocation

```
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome

"$CHROME" --headless --disable-gpu --no-sandbox \
    --no-pdf-header-footer \
    --print-to-pdf=OUT.pdf "file://ABSOLUTE/PATH/IN.html"
```

**`--no-pdf-header-footer` is not optional** — without it every page gets a URL and a date printed into the margin, which is exactly the margin the card geometry needs.

*It writes an SSL handshake error to stderr and produces a correct PDF anyway. Ignore it.*

### Two traps, both hit for real

**`generate-rules-pdf.py` writes its HTML next to itself, not next to your working directory.** Run it from anywhere and the output lands in `printing/`. *This dropped a stray `items.html` into the repo on 2026-09-22.* **Generate into a scratch directory and move the output there before doing anything else**, or check `git status` after.

**Nothing generated for chat belongs in the repo.** The tracked HTML in this folder is the format, regenerated from the markdown by the scripts above. A one-off catalog or a single rules document built for somebody to read is output, and it goes to the person rather than into the tree.

### What the tracked HTML is for

**The 15 HTML files in this folder are the conventions, in executable form.** They are derived from the markdown and they are in git so that a change to a card is visible as a change to the sheet that prints it. *That is also what `./generate-all.sh` is really for — not the PDFs. Reasoning about which sheets should have moved after a rules edit has failed three times out of three, and rebuilding everything and diffing has caught it three out of three.* **The staleness check is the load-bearing half of that script and it does not need Chrome.**

---

## The PDFs are not in git

**They are build output.** `.gitignore` excludes `printing/*.pdf`, and
`generate-all.sh` is what puts them back.

The reason is how git stores things. Every commit of a file stores a fresh
compressed copy of it; for prose that is nearly free, because git packs
similar text against its neighbours and a changed paragraph costs a few
hundred bytes. **A PDF cannot be stored that way.** It is already
compressed binary, so changing one sentence in a rules file scrambles the
whole output and the next commit stores another full copy. The eleven
sheets here are 11 MB, and every rebuild that got committed added that
again, permanently.

Two things worth knowing about that decision:

- **It does not shrink the repository.** Every copy already committed is
  still in the history and always will be; removing a file going forward
  only stops *new* ones being added. Reclaiming the old ones would mean
  rewriting history, which breaks every existing clone, and is not worth it
  for a repository this size.
- **A player still gets a download, and it comes out of a chat session**
  (PDF format conventions, above). Drew asks, an agent builds it from the
  markdown and hands over the file. **No release page, no tags, no CI** —
  that path existed until 2026-09-22 and was retired unused.

## There is no release path, deliberately

**Retired 2026-09-22.** A `v*` tag used to build every PDF in CI and attach
them to a GitHub Release, and a second shell script built the card sheets on
their own. **Both are deleted and neither was ever used.**

*The reasoning behind them was sound and simply did not match the workflow:*
the thought was that somebody without Python or Chrome needs a download, and
a release page is how they get one. **What actually happens is that Drew asks
in chat and gets the file back** — he has no terminal, tags and releases are
conventions he has said he does not use, and a build he cannot trigger or
inspect is worse than no build.

**So the repo keeps the format and not the delivery** (PDF format
conventions, above). *If a release path is ever wanted again it is a small
file and the history has it.*

**The consistency scripts in `agent-tools/` are run by hand, on purpose**
(`CLAUDE.md`, Checking work). *There is now nothing here that could gate on
them even if somebody wanted it to, which is the convention holding rather
than a gap.*

## What is here

| | |
|---|---|
| `generate-all.sh` | The entry point. Rebuilds everything and reports what moved. |
| `generate-cards.py` | Card sheets. **Holds the seated set lists** — which cards are in the Oracle, the expansion and each encounter set. |
| `generate-rules-pdf.py` | `packet` and `play-reference`. |
| `generate-sheets.py` | Character sheets. Recomputes HP, hand size, initiative and deck maximum from each stat table, so a stat change has to come back through here. |
| `generate-blanks.py`, `make-grain.py` | Blank stock and the paper-grain textures in `assets/`. |
| `assets/` | Fonts and grain textures. **Inputs, and tracked** — an asset changing makes every PDF stale, which `generate-all.sh` checks for. |
| `*.html` | Generated, and **tracked**: they are text, they diff cheaply, and they are what the staleness check compares against. |
| `card-art-prompts.md`, `sheet-art-prompts.md`, `card-styling-notes.md` | Working notes for the art and the layout. |

**`generate-all.sh` builds print artifacts and nothing else, deliberately.**
Don't wire checks or linting into it — the consistency scripts live in
`agent-tools/` and are run separately.

## Which sheets get a PDF

`PDF_SHEETS` in `generate-all.sh` says. Four card sheets are deliberately
not in it — `briarwatch`, `mason`, `items` and `items-field` — because they
have never had one. Add them to the list if you want them; the only cost is
a Chrome launch each.
