# Canon Consistency Audits — Design Trail

## What this trail preserves

This is the historical record of repo-wide contradiction hunts and keyword/glossary consistency work — passes that read the content layers against each other (or against the simulator, or against the print pipeline) looking for drift, rather than passes that shaped what any one card or system should be. Distinct from `archives/consolidated/card-pool-evolution.md`, which covers card-pool size/range/color-identity decisions, and from `archives/consolidated/oracle-pool.md`, which covers the Oracle pool's own composition history.

The fixes described here are already live in canon. This file preserves the reasoning trail and the audit method, not a second copy of current rules.

## Contradiction hunt across the non-world files

Drew: *"let's hunt for more contradictions."* An earlier audit had covered `world/` and `mythology/` only; this one covered everything else, read by **seam** — a subject held in more than one file — rather than file by file, because that method is what had found the Seat States divergence: duplication is what drifts, so go looking at the duplicates.

Findings included: one farm carrying two names (Western Property in five places, Well Property in ten, across seven files, with two files using both in the same document — standardized on Western Property, with "the old well property" kept as a genuine local nickname rather than erased); the Hollow's opening narration asserting a cause its own dungeon disproves (reframed as what Briarwatch believes, not flat fact); two stale pointers into content that had moved the same night; and a keyword collision distinct from a longhand one — `bestiary/fogcaller.md` read "Immune to Blind," but Immunity is a defined keyword meaning something else entirely (one-shot negation of the next attack, expiring on use), not permanent immunity to a debuff token. Rewritten to "Blind has no effect on it." A parallel case in `rules/items.md` (a Pell lantern "immune to the Misdirection Trap") was noted and deliberately left alone — out-of-combat prose, not a stat block where keyword parsing matters, and the fix would have been churn.

The Regency's own text was also caught claiming something about seven council members that can only be true of five — Isabella and Percival were recruited after the Pendragon Attempt and can't carry the same scar-tissue titles. Fixed by saying so, which improved the file rather than just patching it.

## World-layer audit: the Scar's taxonomy, and the Seat States "Fading" gap

Prompted by noticing that `verify.py` covers cards, decks, stat blocks, references, the simulator, items, and the glossary — but had no way to know whether the *world* layer contradicted itself, which was precisely the layer that had changed most that session (the In-Between, the Scar, Pendragon).

**The Scar's taxonomy placement was wrong, and self-correcting once checked.** An earlier note had described `world/seats-archons-echoes.md` as "the taxonomy the Scar is conspicuously not in." But that file's own Failed Seat-Takers entry reads: "beings who attempted to claim a Seat and survived the contact without succeeding. The Seat leaves its mark permanently." That's Pendragon exactly, and `the-regency.md` already classes his five companions the same way — the claim was a flourish never checked against the file it named. Corrected, and the correction opened a more interesting question than the error had hidden: the Scar's *stage* is unclear, because the Degrees of Alignment all describe what happens to an *identity*, and the Scar has no identity for a domain to become inseparable from. Written up as off-the-end-of-the-scale rather than outside-the-system, with an explicit instruction not to resolve it just to tidy the taxonomy.

**The Seat States table had already diverged across two files.** `mythology/seats.md` listed four states including **Fading**; `world/seats-archons-echoes.md` listed only three and omitted it — while that same file's own Archon section described an Archon fading "until the Seat stands empty" and cited `mythology/seats.md, Seat States` for the mechanism it had itself dropped. A file contradicting the table it points at. Patched, and `mythology/seats.md` marked canonical so future edits have one home. (The gap resurfaced briefly during a later cosmology-consolidation pass that merged the two files outright — same root cause, closed for good once the duplication itself was removed rather than just patched again.)

The structural finding underneath both: the Echo stages and the Seat States were each written out longhand in two files, which is the exact layering bug the repo's own conventions warn about — and it had produced a real contradiction with nobody touching either file recently. Patching the drift doesn't fix the duplication; that's a separate consolidation call.

## "Items reported missing" — a case-sensitive grep bug, and two real fixes underneath it

During a Release pass, a search of `items/` for "Barbed Wrap" returned nothing, and all three items got logged as referenced across six files with no mechanics behind them. They weren't missing — `items/briarwatch-items.md` had held complete entries for all three the whole time, written as **BARBED WRAP**. The search was case-sensitive against a repo convention of storing card and item names in caps. The lesson was narrow and repeatable: any name search across this repo has to be case-insensitive, or it will hide any item, card, or creature the same way.

There was real work underneath the false alarm, though: **SPLIT WEDGE** read "Gain Anchored — +2 damage this turn," but Anchored is defined as persisting while position is held and re-triggering each turn — a one-turn bonus can't be Anchored. Fixed to grant +2 damage each turn, ending the moment the holder moves, matching the fiction of an iron wedge driven into the ground. **BARBED WRAP** wrote Thorns out by hand, and wider than the keyword — "when you are targeted" rather than on a successful melee hit. Fixed to Thorns 1; a real nerf (melee-only, on-hit-only), flagged for Drew and ratified: *"keep barbed wrap as thorns, that's right."* `verify.py` gained an item-keyword check afterward — every keyword an item names must exist in the glossary, no keyword may be restated longhand, and Anchored may not attach to a one-turn effect — validated against the pre-fix file (where it caught both bugs) before being trusted against the fixed one.

## Release pass: the first real full verification

Six checks green, the ledger empty, 167 sim cards reconciled against canon. Two findings beyond the WATCHES FEET/LIMB-SNAPPER range fix (noted separately below):

**`memory.md`'s own audit found four false claims about live canon**, all the same species — statements true when written, never revisited. Two phantom files that had never existed under the names cited (`places/briarwoods.md`, `items/briarwoods-items.md` — stale artifacts of the Briarwoods → Briarwatch rename); two stale HP figures predating the HP-formula change (Briar Scratcher 9→11, Delve Roller 12→13, both corrected to the formula); a Delve Roller passive still described as "−1 all incoming damage" instead of Armour 1; and a claim that the Elder Tower Creature's stat block was complete, when the file itself opens "Not a combat encounter. An environmental presence" — it should never have one.

**A near-miss on the PDF hash check.** Force-rebuilding all six PDFs reported every one as changed, which nearly got logged as six stale artifacts. Chrome's PDF output isn't byte-deterministic — two rebuilds from identical HTML produce different hashes at identical byte length. Nothing was actually stale; the finding vindicated the print pipeline's own design of diffing HTML and rebuilding PDFs only downstream of a real HTML change, since PDFs can't be compared by hash at all.

## Tags WALLOWS, GLASSLIGHT, and ABYSS ratified

Drew: *"the tags are good, keep all three."* Flagged on the way in because the tag set is deliberately finite and three additions in one pass is a real expansion — approved as a set rather than piecemeal. Tag roster became: ASHFALL, BASIN, BRIARWATCH, COIL, ENGINE, HOLLOW, MASON, MILESTONE, UNHELD, WEALD, WALLOWS, GLASSLIGHT, ABYSS — thirteen total.

## Armour and Thorns ruled to stack additively

Drew: *"armour and thorns stack, update the glossary."* Previously undefined — the four charge-based keywords (Resist, Vulnerable, Deadly, Weak) all state their stacking behavior outright, and these two said nothing, which had already forced design-arounds on other cards. They can't stack the way charge-keywords do: Resist and Vulnerable stack as charges, each spent on one attack, but Armour and Thorns are never consumed and never expire, so charge-stacking is incoherent for them. They stack additively into a single value instead — Armour 2 plus Armour 1 held together is Armour 3 against every attack for the rest of the fight.

This surfaced a live correctness bug: **Armour was not implemented in the simulator at all** — not partial, not inert, absent — despite being a documented step in the fixed damage pipeline and carried by 10+ bestiary creatures, three card sets, the entire equipment tier table, and consumables. Every one of those was being simulated with the wrong damage math. Fixed in both engines, positioned before Resist per the pipeline, additive, clamping at 0 while still counting as a landed hit, bypassed by Unpreventable. Thorns needed no engine work — it was already additive.

## Exhaust ruled able to enter hand or deck

Drew: *"let the ashfall exhaust go into decks, update the glossary."* The glossary previously said Exhaust "goes directly into your hand when applied — not into the deck," and used exactly that line as the stated difference from a Wound. But six Ashfall files were already built on deck-insertion — the Tithe Engine, all three Ashgrazer Exhaust cards, CORRECTION LOAD, the Alignment Marshal's passive, and the Trisect's Fuel Seed — and it wasn't drift, it was a designed subsystem (the Tithe Engine seeds decks, Ashgrazers hunt the seeded Exhaust as a prey-signal). Canon widened rather than six files rewritten.

Widening it destroyed the old Exhaust/Wound distinction, so a new one had to replace it: **Exhaust clears in bulk, a Wound comes off one at a time.** One rest removes every Exhaust carried, wherever it sits; Wounds are answered individually, one per action, one per short rest. That distinction is durable — it doesn't depend on where either one entered. Two files carrying the old rule as text were fixed: `cards/tithe-engine-ashfall.md` had printed its own local EXHAUST definition that said hand-only, while the same file's own card shuffled Exhaust into decks — self-contradictory inside one file, and a keyword definition living somewhere other than the glossary. Replaced with a pointer.

## New-player read-through: glossary clarifications

Drew asked what questions a new player would have from a cold read of `rules/core-rules.md` and `rules/card-glossary.md`, then ruled on each finding. Eleven candidate confusions surfaced; Drew ruled on nine, corrected one premise outright, and left one open.

**Corrected, not executed:** Drew asked to cut Advantage (Damage) / Disadvantage (Damage) as apparently unused. Checked before cutting rather than complying reflexively — it wasn't unused, it was the Defensive Bonus or Effect on at least eight live cards plus bestiary flavor text and two player-facing passives. Cutting it would have orphaned every one of those cards' rules text, so it wasn't cut; flagged back to Drew instead.

**Left open:** whether a card played as a *defense* must satisfy its own Range requirement, same as it would as an attack — this was later resolved (defense is now range-gated; see the range-pass material in `card-pool-evolution.md`'s neighboring trail and `rules/combat.md` for the live rule).

**Ruled and executed:** Blind and Evade now share a resolution moment, both rolling immediately after the attacker's card is committed rather than Blind rolling earlier, and a Blind-caused miss now discards the attacker's card, matching the Evade ruling. Rooted only blocks voluntary Move Position — forced repositioning still works on a Rooted target. Quick grants a free move *in addition to* the normal action, not a substitute for it. Ward triggers automatically the instant a qualifying debuff would land. WOUND was redesigned around a genuine gap — the old "use your action to discard" option didn't actually solve anything, since a merely-discarded Wound would eventually reshuffle back in; replaced with permanently destroying one Wound from hand via an action, alongside the unchanged once-per-short-rest destroy option. **EXHAUST was fully simplified** in the same pass, ahead of the hand-or-deck ruling above: cut from three disposal paths down to one — use your action to permanently remove all Exhaust from hand.

## CERTAIN CONTACT renamed to CERTAIN STRIKE; UNMAKE's redundant Ward phrase removed

Drew: *"rename CERTAIN CONTACT to CERTAIN STRIKE. remove the ward phrase."* Both were prior suggestions rather than reported bugs, so before executing either, the bar was confirming the suggestion still held up under a second look rather than just complying.

**UNMAKE's fix was checked before being applied.** The original suggestion had been hedged: the qualifier might be redundant, or it might be signaling a real, undocumented Ward interaction, in which case the fix belonged in the glossary rather than on one card. Checked directly: `remove_positive_status()` has no Ward check anywhere in its body, and UNMAKE's own effect and defense call it plain, with no bypass layered on top. "Ignoring Ward" was never live behavior for any card. The phrase was safe to delete outright, and the code needed no change — which is itself the confirmation the suggestion was right, not an assumption that it was.

**The rename swept eight files**, not one: `cards/red-body.md`, four bestiary decks, `cards/wall-reader.md` and `bestiary/wall-reader.md`'s promotion history, and both simulator engine files (the `add()` call, the function name, two comments, one frozenset entry). Wall-Reader's own file already carried a layered rename history from an earlier promotion; the old name stayed visible in exactly the two spots making a historical claim, swapped everywhere else — the same precedent as the SIDESTEP/SWAY/DUST starter-card renames.

## GORE and CENSER SWING: a vacuous condition, found twice

**GORE's fix is already covered in full in `archives/consolidated/oracle-pool.md`** (its own section, "GORE, the pinned slot, and a condition that was never real") — the card's Effect checked "if target is Frontline" on a Range-Melee card, where Melee's own legality already guarantees the target is Frontline, so the condition could never resolve false. Noted here only because CENSER SWING was found as its twin during that same diagnosis and is written in full below rather than duplicated there.

**CENSER SWING fixed the same way, at a proportionally smaller die cut.** Drew: *"go ahead and fix CENSER SWING."* `cards/vescal.md`'s CENSER SWING had the identical shape — Range Melee, "If target is Frontline, deal +2 damage" — the same vacuous check, same root cause. The range fix was identical and non-optional: Melee → Both is the only change that makes the sentence true instead of decorative. The die cut was not copied wholesale from GORE, and that distinction mattered: GORE's kicker was a `+d6` (average 3.5), so losing it roughly half the time cost about 1.75 average damage, matched by Drew's own two-step d8→d4 cut removing 2.0 average from the base. CENSER SWING's kicker is a flat `+2`, so the same reasoning caps the compensating cut at roughly 1.0 average — one die step (d8→d6), not two. Cutting to d4 anyway just because GORE did would have imported GORE's specific balance answer onto a card with a differently-sized problem. No simulator involvement was needed — Vescal's deck has no `add()` calls or damage functions in the simulator at all, so this was a canon-text-only fix.

## Weak, Blind, and Deadly: an under-representation census

A keyword census taken during a bestiary deck-backfill pass found Weak (4 cards), Blind (7), and Deadly (7) as the least-represented keywords in the game, against Evade (17 cards) and Resist (13) as the most common by a wide margin. Recorded as a standing note for future bestiary deck-building rather than a one-time fix: *"let's make a note to try and use them next time we are making bestiary decks."* Lean toward these three when a creature's kit has room, rather than defaulting back to Evade/Resist.

## Noted in passing: WATCHES FEET and LIMB-SNAPPER's Range correction

During the Release pass above, WATCHES FEET (`cards/aege.md`) and LIMB-SNAPPER (`cards/rootstalker-weald.md`) were both found printing `Range: Melee, hits Backline` — a combination that made their own Effects unreachable, since Melee against a Backline target is illegal under the Range Matrix. Corrected to **Both**, the only value in the vocabulary that makes the printed Effect legal to fire. This was flagged in-text as "very slightly wider than the longhand appears to intend" — Both also legalizes a Backline attacker, which the original phrasing may not have meant to license — with a note that reverting is one edit if Drew reads it differently. That note was not one of the questions put to Drew this session. It ships as-is: low-stakes, easily revisited later, not an open flag waiting on an answer.

## Durable audit lessons

- Read by seam (a subject duplicated across files), not file by file — duplication is what drifts, so that's where contradictions surface first.
- A word can be a real, defined keyword used for something it isn't ("Immune to Blind" reads as the Immunity keyword but means a debuff-token immunity) — this is a different species of bug than an invented keyword or a longhand restatement, and no automated check catches it.
- Any name search across this repo must be case-insensitive; card, item, and creature names are stored in caps, and a case-sensitive grep will silently report real content as missing.
- Charge-based keywords (Resist, Vulnerable, Deadly, Weak) and always-on keywords (Armour, Thorns) stack under different rules — a reader who pattern-matches one family onto the other gets it wrong, so both families need their stacking rule stated explicitly on the keyword itself.
- A canon widening (Exhaust into decks) that breaks an existing distinction needs a replacement distinction stated at the same time, not just a deletion.
- A hedged suggestion ("this might be redundant, or might signal something real") should be checked against the actual implementation before being executed, even when Drew has already approved it in principle.
