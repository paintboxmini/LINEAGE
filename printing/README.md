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
- **A player still gets a download**, just not from the file tree. Tagging
  a version builds the sheets and attaches them to a **GitHub Release** —
  see below. Same link to hand somebody, none of the history cost.

## Releases

**Tag a version and the sheets come out the far end as downloads.**

```
git tag v2026.09.20
git push origin v2026.09.20
```

`.github/workflows/print-release.yml` checks out that tag, builds every
PDF from its own source, and attaches them to a GitHub Release. Nobody
needs Python or Chrome on their own machine to print a deck — they need
the release page.

The workflow can also be run by hand from the Actions tab without tagging,
which uploads the sheets as a build artifact (kept 30 days) and creates no
release. That is the way to check a build before committing to a version.

Two things it does that are worth knowing:

- **It refuses to release from stale sheets.** The build runs with
  `--check`, so if any HTML is out of date against the markdown the
  workflow fails and no release is created. Regenerate, commit, re-tag.
- **It looks at the PDFs before shipping them.** Headless Chrome can exit 0
  and leave a stub behind, so every file is checked for a `%PDF-` header
  and a plausible size, and the count is checked against the expected
  eleven. A silent empty sheet is the failure this is for.

**The consistency scripts in `agent-tools/` are deliberately not wired into
it.** They are run by hand, on purpose (`CLAUDE.md`, Checking work), and a
release gate is exactly the kind of enforcement that convention is about.
Adding them is three lines if that changes.

## What is here

| | |
|---|---|
| `generate-all.sh` | The entry point. Rebuilds everything and reports what moved. |
| `generate-cards.py` | Card sheets. **Holds the seated set lists** — which cards are in the Oracle, the expansion and each encounter set. |
| `generate-rules-pdf.py` | `packet` and `play-reference`. |
| `generate-sheets.py` | Character sheets. Recomputes HP, hand size, initiative and deck maximum from each stat table, so a stat change has to come back through here. |
| `generate-pdfs.sh` | Card sheets to PDF only, with an optional output directory. `generate-all.sh` does not use it. |
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
