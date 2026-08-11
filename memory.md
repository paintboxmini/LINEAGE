# LINEAGE — Memory

## Memory is a bounded representation

Memory preserves concise historical context for major decisions when that context materially improves future reasoning. A memory entry records the problem, the decisive reasoning or failed alternatives that explain the decision, the resulting principle/rule, and only the minimum provenance necessary to understand why it matters. It does not preserve complete deliberations, chronological work logs, implementation details, or every rejected idea. Those belong in archives.

Memory is not a transcript of how we thought. It is the smallest durable explanation of why the current design is the way it is.

## Branch map

- `Main` — canon. Humans merge to it.
- `claude/general-chat-vwvr1` — Claude's working branch (this log's primary author).
- `claude/crystal-project-chat-76gzcn` 

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
