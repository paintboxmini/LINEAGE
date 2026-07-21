# Live 2v2 Mechanics Test — Sky & Crimson vs. Moss & Garnet

**Date:** 2026-07-20
**Players:** Drew (Sky, Crimson), Claude (Moss, Garnet), played turn-by-turn over chat
**Length:** 18 turns to Moss's Collapse; called there rather than played to resolution (Garnet alone, 1v2, estimated 3–6 turns from a loss)
**Full turn-by-turn record:** `playtesting/live-test-2v2.md`

This wasn't run to find out who wins. It was a live test of protocol pieces that had never been exercised outside the simulator: an async blind-reveal sequence over text, hidden stats/HP with public status markers, and — the reason it existed at all — a direct look at the Soul/Initiative structural gap from earlier the same night.

---

## The Setup

**Sky** (Mind 4/Body 3/Soul 2) and **Crimson** (Mind 3/Body 4/Soul 2) — Drew's, CTR 9 each, real numbers shared before the fight so a matched opponent could be built, never referenced at the table during play.

**Moss** (Soul 4/Body 3/Mind 2, mirrors the sim's ADEPT spread) and **Garnet** (Body 4/Mind 3/Soul 2, mirrors STEELE) — built deliberately as a direct test of the Soul-payout question: Moss was the Green-leaning half of the pair on purpose.

**Reveal protocol:** the defender (or, on an attacking turn, whoever's not initiating) commits their card first, unseen, signals ready — then the other side announces blind, and the first side reveals. Held up cleanly for the entire test.

**Hidden info:** Mind/Body/Soul values and HP totals stayed private to each side; positions, initiative order, and status markers were public throughout, per Drew's call going in.

---

## Result

| | Start HP | End HP | Status |
|--|----------|--------|--------|
| Moss | 15 | 0 | **Collapsed**, turn 18 |
| Garnet | 17 | 8 | Standing, alone vs. 2 |
| Crimson | 17 | 12 | Standing |
| Sky | 15 | 15 | Standing, full |

Damage dealt by Claude's side: 10 (5 to Crimson, 5 to Sky). Damage dealt by Drew's side: 19 (4 to Garnet, 15 to Moss) plus Garnet's own 5 HP self-cost from RALLY's Effect. Moss took six real hits before finally going down exactly on her last 3 HP — no overkill, no clamp needed.

---

## Real Findings

**STRIKE's Defensive Bonus had drifted from its own implementation.** Drew remembered it as a free Counter Attack; canon said flat 2 damage. Checked BREAK before picking a fix — it already owns free-Counter-Attack-on-a-clean-win, and giving STRIKE the same payoff on top of the best base die in the set would have made BREAK pointless. Landed on 3 damage, unpreventable, instead — and found the sim had already been treating it as unpreventable while the card text never said so. Fixed in both places. See `memory.md`.

**The Range-legality rule had a real gap: no ruling for a mistaken illegal pick.** Came up more than once — WITNESS played into a Melee-illegal position after FORGET was already revealed blind. New rule, added mid-test and then refined once more the same night: caught before the opponent's card is known, swap freely, no penalty; caught after, it resolves as no legal defense, but the misplayed card returns to hand, not discard — the attacker already gets the real cost of seeing what it was, losing the card too would be one penalty stacked on another for an honest mistake. Now in `rules/combat.md`.

**Range legality tripped up careful play repeatedly — five separate incidents across 18 turns**, including the designer's own. Worth flagging as a possible clarity gap, not just bad luck: Melee needs *both* sides Frontline (attacker included, not just the target), and that's easy to misjudge mid-game when position's been shifting. Might be worth a callout box or reminder in the player-facing rules, not just the GM's.

**ROOTED OATH's Anchored Effect looked like a strong, uninterruptible engine — walked back after review.** Grants Deadly to an ally every turn the caster stays anchored, and nothing in Garnet's hand could force a reposition to break it. Flagged at the time as worth a second look. Drew's read afterward: this is matchup-specific, not a card-level problem — Garnet's build simply had zero tools against the Position pillar (see "The three core pillars," Standing Reasoning), which is exactly the kind of intentional risk a build takes on when it skips one of the three (RPS/Initiative/Position) entirely. Most real teams carry an answer to at least one. Also missed the first time: Deadly doesn't apply the instant ROOTED OATH is cast — the first tick lands on the caster's *next* turn, a real tempo cost the "free loop" framing undersold. Correction, not a retraction of what was observed — the loop is real, it just isn't evidence of a balance problem on its own.

**Resist earned its keep as a real sustain tool, no healing required.** Moss survived four separate hits well past when she looked done, purely off Resist stacked from repeated GUARD ties. She lasted 18 turns on a kit with zero self-healing in hand when she finally went down — longer than either side expected going in.

**The Soul/Initiative question itself:** inconclusive by design — the scrapped stat-scaling Initiative Shift card never got tested since it was cut before the fight started. What this test *did* show: Moss's Soul lead (4, the highest single stat on the board) bought her the first turn of the game and nothing else measurable afterward. The structural point from earlier — Soul's payout is front-loaded, Body's and Mind's are felt every turn — held up in actual play, for whatever one 18-turn sample is worth.

**Wheel-shrinking on Collapse worked exactly as documented.** Moss leaving the fight dropped the wheel from 4 seats to 3 with no fuss — Crimson → Sky → Garnet, cleanly.

---

## Not Resolved, Not Needed

The fight was called with Garnet facing 1v2 and no realistic path back — three real findings already banked, and continuing to an actual loss wouldn't have taught the protocol anything the last six turns hadn't already shown. Formality, not a cliffhanger.
