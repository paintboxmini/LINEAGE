# binder

**Player pages for the bestiary binder Chris keeps** *(Drew, 2026-10-08)*. **The players never see this repo** — everything they hold is printed, and a creature's page is earned at the table (`CLAUDE.md`, Conventions worth knowing before you edit).

**These are not the bestiary files.** `bestiary/` is written for the GM — tactics, how to beat it, win rates, traits the party may never see. **A page here is written fresh, for players, and holds only what the party could know.** *Never copy a bestiary file in; write the player page from it and leave everything else behind.*

**Two pages per creature, each with its own `# ` heading so it prints on its own sheet:**

| Page | Handed over | What is on it |
|---|---|---|
| **Field notes** | After the party's first real encounter with it | What it looks like and what anyone would notice, **plus blank lines** for the note-taker to fill in |
| **Measured** | **When MEASURE (or anything that reveals stats) lands on one** | **Stats, HP, Skills, Traits and Passives**, and for a simple creature run from a blank deck, **its signature cards** (`rules/card-glossary.md`, Reveal stats) |

*Field notes can be handed over without the Measured page ever following — a creature nobody measured stays a page of the party's own guesses, which is the point.*

**Not part of `printing/generate-all.sh`.** A page goes out when something happens at the table, not when the repo changes, so it is built on request: `printing/generate-rules-pdf.py` finds files in this folder, and the PDF goes to Drew in chat like every other printed artifact (`printing/README.md`).

## Pages

| Creature | Field notes | Measured |
|---|---|---|
| Wrackclaw | `binder/wrackclaw.md` | same file |
