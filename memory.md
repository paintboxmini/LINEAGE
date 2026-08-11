# LINEAGE — Memory

**What belongs here:** active threads, mid-session decisions, things in flight that the repo can't capture on its own.

**What doesn't belong here:** keyword definitions (see `rules/card-glossary.md`), workflow rules (see `CLAUDE.md`), location summaries (see `places/`). If it has a canonical home elsewhere, it goes there.

**Timestamps, starting now (2026-07-17, Drew's request):** new entries lead with a real timestamp in Drew's local time — `TZ='America/Chicago' date` (Central, DST-aware — CDT or CST as the calendar actually has it), not a guess. Prospective only; existing entries above this line stay exactly as written, no retroactive stamping.

## Branch map

- `Main` — canon. Humans merge to it.
- `claude/general-chat-vwvr1` — Claude's working branch (this log's primary author).
- `claude/crystal-project-chat-76gzcn` 

## Pending propagation

Stale dependents awaiting a Sync pass (see Work Modes in `CLAUDE.md`). Empty means everything is propagated.

- **Oracle pool, canon vs. code.** `Oracle/baseoracledeck.md` was emptied 2026-08-04 (Drew: hand-building the real pool before Session 1). `combatsimulations/content.py`'s `ORACLE_DECK` and `printing/generate-cards.py`'s oracle card list still hold the old 63-card AI-selected composition — not a normal staleness case, deliberately not synced yet, since there's nothing to sync *to* until Drew's build exists. Do not "fix" this by emptying the code to match; wait for the hand-built list and reconcile all three at once.
- **Stats → Aspects rename, full repo, queued for Sync mode.** Drew: *"Rename stats to Aspects in sync mode."* "The 3 Aspects" was established 2026-08-11 as the canonical name for Mind/Body/Soul in `rules/combat.md`'s Core Combat Philosophy, deliberately scoped narrow at the time — the rest of the repo still says "stat(s)." Real scope, researched ahead of the Sync pass so it doesn't start cold: 86 files, ~514 word-boundary occurrences (not the ~1,417 raw-substring count, which is mostly unrelated `state`/`status`/`static`/`statue`/`estate`). Real complications, not a blind find-replace: Python identifiers (`combatsimulations/`'s `COLOR_TO_STAT`, `Card.stat`, `FROST_STATS`, etc., and `agent-tools/verify.py`'s `check_stat_blocks()`) are explicitly out of scope for this pass — prose only, never code; "Stat Block" (76 occurrences/40 files, the formatted display convention) is a separate naming question from "the 3 stats" and needs Drew's call before touching, not an assumption; three named headings/mechanics (`CLAUDE.md`'s Stat System Quick Reference, `rules/character-creation.md`'s Stat Increases, `rules/card-glossary.md`'s Stat Change — cross-referenced by name from the Future-Lock entry) need considered renames, not mechanical swaps; `combatsimulations/README.md` mixes the stats-sense and the statistics-sense in one file and needs manual handling; must not touch "Status" (an already-established, unrelated keyword family). `rules/combat.md` itself already has both vocabularies coexisting and needs internal reconciliation as part of the pass. Full detail: `archives/key-design-decisions.md`.
- **Echo → Resonant Person rename, character-file half.** 2026-08-10: `mythology/echoes.md` was renamed to `mythology/resonant-people.md` and every core mythology doc (`archons.md`, `resonant-items.md`, `seats.md`, `world/seats-archons-echoes.md`, `world/eclipseria-overview.md`) updated to match — Drew's explicit scope choice was "core docs only." The five character/world files with dead links to the old path (`world/the-regency.md`, `bestiary/fermata.md`, `characters/aege.md`, `characters/thess.md`, `world/the-scar.md`) had their cross-reference *paths* fixed immediately (a broken link is a defect regardless of scope, not staleness to defer) — but their prose still says "Echo"/"Echoes" throughout, which is the deferred half. Fourteen more files reference "Echo" in passing without linking the file directly (`unresolved-concerns.md`, `characters/kaine.md`, `characters/kess.md`, `quests/turnroot-weald-adventure.md`, `items/the-silent-choir-items.md`, `places/the-collection-plate.md`, `rules/items.md`, `items/capital-items.md`, `places/capital/underground-bazaar.md`, `quests/washed-ashore.md`, `bestiary/phase-leach.md`, `quests/the-wallows-descent.md`, `places/turnroot-weald.md`, `items/turnroot-weald-items.md`, `places/capital/capital.md`, `playtesting/first-impressions-sonnet-4-6.md`, `places/abyssal-ruins.md`) — not all of these are guaranteed to be the cosmological sense; each needs a read before editing, not a blind find-replace. `places/fog-basin.md`, `items/fog-basin-items.md`, and `bestiary/echo.md` itself are the unrelated ambient fog-creature "Echo" and should NOT be renamed — the rename removes a real word collision there rather than creating one. `memory.md`'s own older entries that mention `mythology/echoes.md` are deliberately NOT rewritten — this file's own header rule is that existing entries "stay exactly as written" — and this very entry has to name the old path too, to explain what got renamed from what. **Resolved 2026-08-10, same day:** Drew, "echoes md is a bug" — correctly diagnosing this as a tooling gap, not content that needed rewriting. `verify.py`'s `check_refs()` now exempts `memory.md` from the cross-reference check entirely, the same way `archives/` already was — both are historical record by the repo's own stated rules, not live canon prose, so a renamed file mentioned in either was never actually a broken link. 12/12 verify going forward; the character-file half of the actual rename (below) is still real, still open work.

---

## Campaign Status

**Intended session spine (Drew, 2026-08-02)** — the shape the gold pacing is calibrated against:

| Session | Where |
|---|---|
| 1 | Unheld Ocean shoreline → Roadhouse → Briarwatch, ending at the ruins about to go into the burrows *(was Vulture's Nest → Roadhouse → Briarwatch; retired 2026-08-06, `archives/key-design-decisions.md`)* |
| 2 | The Hollow solved |
| 3 | Turnroot Weald |
| 4 | Turnroot finished |
| 5 | Eclipseria — the capital |

This is why gear pacing targets five sessions to a first Tier 1 item **per character**: it lands each character's first real equipment at roughly the moment the campaign reaches the city that sells it. Not a schedule to enforce — a reference the economy was built against.

---

## Active Pending Threads

Possible future connections noticed while doing other work, that don't require answering them (Drew). If something here actually needs an answer for current work to tie into the repo correctly, that's debt, not this — it belongs in `unresolved-concerns.md` instead.

**ARCHITECTURAL NORTH STAR — typed modifiers, Step 3.** Step 2 shipped 2026-08-05/06 (typed modifiers with lifetimes for `axiom_ban`, `cannot_defend`, `staggered`, plus the AXIOM attacker-side gap closed same week — full reasoning archived, `archives/key-design-decisions.md`). Step 3 — the full policy stack — remains explicitly deferred, not abandoned: only worth building once a modifier-as-special-case has become genuinely painful. This is the only live pointer to that sequencing call left after the 2026-08-11 restructure moved Step 2's reasoning trail to archives.

**B thread — Quartermaster Voss**
Secondary hook, only activates if party explored the Roadhouse barracks and found the posting order. Unsigned line: "anything from the docks that isn't in the manifest." Points to unsanctioned smuggling from Vulture's Nest to the capital. Voss is at Eclipsera South Gate. Voss's intake reports are cross-referenced against Jonas's ledger — condoned goods appear in both. The supply chain that doesn't appear in either is the FourthEye thread. Don't develop until party pulls on it.

**FourthEye pipeline**
Drug spreading through Eclipsera's Underground Bazaar (Giblets' stall is the bazaar-end node). Supply chain runs from Vulture's Nest, bypasses Jonas's ledger entirely, never appears in Voss's intake. Masaharu is at the Nest tracing it backward. Identity of the Nest-side operator: unknown. Giblets' "plan connected to someone he used to work with" is the forward-pointing thread. Three Regency hard lines violated: too addictive, too destructive, council gets no cut. **The Cellar Custodians are the last link before it reaches the Bazaar** (Drew, 2026-08-05) — the deep tunnels they patrol are the same ones the drug has to move through to reach the Bazaar's hidden pocket. Who's actually dirty and how far up it goes stays unestablished, same as the Nest-side operator. See `places/vultures-nest.md` (Masaharu, Rumors), `places/capital/underground-bazaar.md` (Giblets), `factions/the-cellar-custodians.md` (GM Secret).

**Bazaar uprising thread** (future)
Kess is positioned as a future organizer: Cartographers Guild network, grandmother's intelligence cache, personal grievance, methodical temperament. Moth as wildcard (nothing to lose). FourthEye pipeline crossing Regency hard lines as potential lever. Don't develop without Drew — flag as long thread.

---

## Active Reasoning

Reasoning that's currently being used or actively improved on — not a running history of what's already settled (2026-08-11, Drew's restructure: *"active reasoning is for the most current work, for reasoning that is currently being used/improved on, not for reasoning that's resolved and not being used currently."*). Standing rules, heuristics, and evaluative frameworks belong here for as long as they're still the working rule; once something's fully absorbed into canon or superseded, it moves to `archives/key-design-decisions.md`.

**Wheel is a TEAM instrument; duels accepted as degenerate (Drew ruling).** Drew noticed the wheel "has problems in duels." Diagnosis (translated): a 2-seat wheel has no INTERIOR — repositioning needs seats to move among, and with only two seats the only place to move is across the marker, which is a crossing by definition. So in a duel every Initiative Shift collapses to one of three extremes — no-op, bonus turn, or skip — and the rich middle (subtle reposition) doesn't exist. Not a bug; geometry. The wheel's richness scales with seat count. DECISION: stick with the wheel as-is for team fights; **real table combat is always ≥4 combatants** (even the 2-player test party fights enemies, so its wheel has 3-4 seats), and pure 1v1 is essentially the simulator's domain, not real play. Duels don't matter right now; bespoke duel rules can come later if 1v1 sparring ever becomes a real mode. No fragmentation of the ruleset — one wheel, optimized for the play pattern the game actually uses.

**Correction/refinement, live 2v2 test night: 4 seats is the peak, not just "big enough."** Reading this entry, I extrapolated that impact keeps climbing past the ≥4 threshold — it doesn't say that, and it's wrong. Drew, direct: "initiative shifting is at its highest impact in a 4 combatant fight. 3 and shifts get reduced. 1v1 will probably end up with an extra ruling eventually if shifting becomes degenerate." So the real shape is a peak at 4, not a floor: 2 seats (duel) is degenerate as already established, 3 is reduced from peak, 4 is where Initiative Shift does its best work, and nothing here claims what happens past 4. Matters because the live 2v2 test WAS a 4-seat fight — the sweet spot, not a still-too-small one — and both sides still built decks with essentially zero Initiative Shift cards in them (Garnet's one copy of MOCKERY never even fired its shift). Drew's read, not mine: "if we passed on it in the format where it has the most impact then the cards might be underpowered. not saying they are" — a real, open finding, not resolved here. Next step, his own plan: run more live tests deliberately building decks that invest in all three pillars on purpose, rather than whatever a normal deckbuilding pass organically produces, specifically to find out where combat shines and where it needs polish. Also noted for next time, deliberately not chased tonight: Drew "was kinda tempted to take some noncombat actions" during the fight but stuck to pure combat mechanics on purpose — scope worth keeping in mind for whichever test picks this up next, not a gap in tonight's.

**A keyword should never be a card's whole idea — only where the idea lands, after everything else about the card has already made it distinct (Drew, confirmed: "that's the shape I'm pointing at").** Surfaced from a real worry, not a specific bug: Drew flagged that keywords (Deadly, Resist, Weak, Blind...) are vague enough to fit a lot of circumstances, and leaning on them as the default toolkit risks flattening genuinely different fictional behaviors into the same mechanical output — "if every poison and toxin puts weak on an enemy they'll lose their distinction." First floated as a possible fix: require keyword diversity when building cards. Talked through and landed somewhere sharper instead — diversity-as-a-rule risks its own failure mode (inventing new keywords just to avoid reusing old ones, which is the same "one category doing another category's job" mistake this repo has already made twice, just at the keyword-vocabulary layer instead of invariants/design-principles). The actual test: after landing on a keyword, ask what the card is doing *besides* granting it — a real trigger condition, a cost, a pillar interaction (RPS/Initiative/Position — `rules/combat.md`, Core Combat Philosophy) — something that gives the fictional behavior its own shape even if the mechanical resolution is shared. Two poison cards can both grant Weak and still read as completely different if one's a slow bleed on a clean win and the other's a one-time burst gated on a specific condition. If the honest answer to "what else is this card doing" is nothing, that's fine sometimes too — a cheap filler card doesn't need to be forced into more than it is, just don't mistake "it grants Weak" for the card's actual identity. **Worth naming precisely: Drew walked back the claim that this happened tonight ("I spoke too fast") — the worry is a real, standing pattern-recognition instinct ("sometimes I just see the same keyword over and over and I worry things are flat"), not a diagnosis of any specific card built this session.**

**Design note for future Masons content, not canon text:** if more Mason content gets built, the Abhorsen throughline to lean into is competence-under-personal-risk in a place normal people can't safely enter, not generic "monster hunter" (trimmed from the full 2026-08-04 MASONS SHARPENED entry, archived in full — `archives/key-design-decisions.md`).

---

## Multi-Agent Notes

Different agents naturally specialize based on which parts of the repo they engage with. Drew is content adjudicator. Don't pre-define agent roles — the environment does that work.

The repo IS the persistent memory. This file captures what the repo can't — mid-session decisions and active threads.

New agents: read `CLAUDE.md` first, then this file. The experimental folder and archives show design process history.

Full session-by-session history archived at `archives/multi-agent-notes.md`.
