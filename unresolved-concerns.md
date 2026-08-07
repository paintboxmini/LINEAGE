# Unresolved Concerns

A scannable index of everything currently open that will eventually need a decision or a fix — the things that otherwise sit buried in `memory.md`'s prose (Recently Shipped entries, Standing Reasoning, Pending Propagation) until someone rereads the whole file. **This is an index, not a third home**: each entry is a line or two plus a pointer to where the full trail lives. Add a line when a concern gets flagged; delete the line when it's resolved (`memory.md` keeps the history — this file only ever shows the present).

**What does NOT belong here**: deliberately open questions. This repo keeps quiet doubts and unresolved world-hooks on purpose (`CLAUDE.md`: "the open questions are on purpose") — who bears the Storm Seat, what the Ferryman reads, what's at the Coil's center. Those are design, not debt. This file is for actual debt: flagged issues, known imbalances, deferred decisions that shouldn't be forgotten.

Also not here: **Pending Propagation** (operational staleness — print sheets, sim sync) stays in `memory.md` where the Sync workflow already looks for it. Entries below may point there, but the ledger itself doesn't move.

---

## Mechanics & Balance

**`rules/card-glossary.md`'s per-keyword counts need a real mechanical recount.** The header numbers are a stated snapshot. On 2026-08-03 I wrote a recount script while adding seven cards and it disagreed with the header on **16 keywords, in both directions** — including decreases, which adding cards cannot cause. That means my counting rule differs from whatever produced the header, and I could not tell which was right. I updated only the six keywords the seven new cards demonstrably touch (Initiative Shift +2; Weak, Staggered, Resist, Evade, Thorns +1 each) and left the rest alone rather than overwrite live numbers from an unvalidated regex. Someone should settle the counting rule once and recount properly. `verify.py`'s `check_glossary_count` only checks the block total, not the per-keyword numbers. Trail: `memory.md`, the 2026-08-03 Oracle 12/6/3 entry.

**`verify.py`'s `check_decks` silently skips any bestiary deck line that isn't in the exact `**Deck (N — B Blue / R Red / G Green):** NAME *(color)*` format.** `bestiary/briar-scratcher.md`'s deck line is written as prose ("3 signature + 1 core to fill: ...") instead — it has never matched the regex, so its per-color counts and card names have never actually been machine-validated, and the check reports clean either way (a non-match looks identical to "checked, found nothing wrong"). Found 2026-08-06 while adding Wrackclaw and Hullback, whose first draft copied Briar Scratcher's prose style and got the same silent pass — caught only because the reported deck count didn't move after adding two new files, then fixed by rewriting to the strict format. Briar Scratcher itself left as-is; either reformat its deck line to the checkable style, or make the check flag prose-style lines instead of silently ignoring them. Trail: `memory.md`, the 2026-08-06 Wrackclaw/Hullback entry.

---

## Content & Tone

**`items/consumables.md`'s five oldest entries are stubs, not thin flavor: Echo Shell, Blood Phial, Imprint Sigil, Universal Pin, Phase Draught.** Each has a name, a type tag, and a price — no flavor line, and no effect text even in their own "full entry" file; the actual mechanics only exist one level removed, in `rules/items.md`'s summary bullets. Unlike Harwick Sundries' mystery counter (`locations/vultures-nest.md`), which is unbuilt on purpose and says so, nothing marks these five as deliberately incomplete — they just read that way, and the names themselves ("Universal Pin," "Imprint Sigil") are generic enough to fail the alignment-checker's own "could this exist in any TTRPG" test. Flagged 2026-08-07 in conversation, not fixed — Drew wants them held until development surfaces where each actually belongs (a source, an ecology, a reason it exists) rather than given flavor text cold.

