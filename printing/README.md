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
- **It costs a player something.** Before, anyone could download a
  printable deck straight from GitHub. Now they need Python and Chrome, or
  they need somebody to send them a file. If that becomes the common case,
  the fix is to attach the PDFs to a **GitHub Release** — same download
  link, none of the history cost — rather than to start committing them
  again.

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
