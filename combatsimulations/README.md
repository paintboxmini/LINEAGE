# Combat Simulations

A PvP duel simulator for Tales Untold. It plays Frost vs Steele thousands of
times to surface rules gaps, balance outliers, and emergent tactics that are
hard to see from the table.

This is a **design instrument, not canon.** Nothing here changes the game. Its
output is two things: a list of rulings the written rules don't yet cover (the
errata queue), and statistics about how the two real decks actually behave.

## Running it

```
cd combatsimulations
python3 run.py                          # 20k duels, reader vs reader
python3 run.py 50000 greedy greedy      # pick policies and count
python3 run.py 1 reader reader --sample # one verbose transcript
```

No dependencies. Python 3.8+.

## What's modeled

- The full turn loop: initiative wheel, draw-to-hand-size (including the
  opening-hand-at-initiative rule), one action per turn.
- Attack resolution with **simultaneous, blind reveal** — the defending policy
  never sees the incoming card; it predicts from public history. This is the
  core mechanic and the thing most worth trusting the sim on.
- All four outcomes: attacker win, defender win, tie (Effect then Defensive
  Bonus), and the automatic win when the defender declines.
- Tokens/keywords the two decks use: Resist (stacking, one per attack), Evade,
  Ward, Axiom's color ban (on the next reveal, attack *or* block), unpreventable
  damage, position/range gating, Blood Tithe's ongoing bleed.
- Three decks in the roster: `frost`, `steele`, and `mire` (a Wound-attrition
  build). Ally-only effects are correct no-ops in a duel and are marked DEAD in
  `content.py`.
- Wound mechanics: status cards that clog the hand, shuffle into decks, are
  counted (Press the Wound), and exile; plus combat-duration stat loss, initiative
  shift (Mockery), and targeting locks (Partition).

## Policies (the "brains")

`policies.py` — swap these to ask different questions:

- **random** — legal-but-thoughtless baseline.
- **greedy** — always attacks for max expected damage; defends only when it can
  predict a winning color. No reading, no Axiom exploitation.
- **reader** — punishes the opponent's most frequent attack color, and aims
  Axiom's ban at it.

Add your own by implementing three methods (see the module docstring). The
`reader` is intentionally simple — a level-k or bluff-aware policy is the
obvious next experiment.

## Findings (20k duels per cell, seeds fixed)

Win rates for **Frost**:

| Frost \ Steele | random | greedy | reader |
|----------------|:------:|:------:|:------:|
| **random**     | 53.9%  | 34.5%  | 56.9%  |
| **greedy**     | 67.1%  | 38.8%  | 68.4%  |
| **reader**     | 54.7%  | 64.7%  | 73.4%  |

Three things jumped out:

1. **The matchup inverts with skill.** Under greedy play, Steele's deck wins the
   diagonal (60.6%) — his Body 4 / HP 18 win a raw slugfest. Under reader play,
   Frost wins the diagonal decisively (73.4%). The "better" deck depends entirely
   on how well it's piloted. That's a feature to protect, not a bug to fix.

2. **Reading pays, and Axiom is why.** Frost's win rate climbs random→greedy→
   reader. Steele's deck is 50% Blue; a reader Frost predicts that reliance and
   points **Axiom**'s ban straight at it. This is the empirical version of the
   table hunch that Axiom, not Paradox, is the real power card — the sim backs it.

3. **Initiative is an edge, not a verdict.** Going first wins ~54–59% in
   Frost-favored cells. Real, worth playing around, not deterministic.

Caveat: these numbers are only as good as the policies. They compare decks *at a
given level of play*, and the reader policy is deliberately basic. Treat the
matrix as "how the decks behave under simple brains," not a final power ranking.

## Mire — the Wound-attrition deck (3/3/3)

A third deck (`mire` in the roster): Balance, Wither, Mockery / Rend, Equal
Footing, Press the Wound / Partition, Taint, Erode. Perfectly balanced 3R/3B/3G.
It wins by shuffling Wounds into the opponent's deck (Rend, Taint) and cashing
them in (Press the Wound), while eroding stats for the whole combat (Wither
−Body, Erode −Soul). Adding it forced the engine to grow real Wound mechanics,
combat-duration stat loss, initiative shift, and targeting locks.

Win rates (20k duels each):

| Matchup | greedy vs greedy | reader vs reader |
|---------|:----------------:|:----------------:|
| Mire vs Frost  | Frost 56.6% | Frost 55.6% |
| Mire vs Steele | Steele 67.4% | **49.9% / 49.4% (dead even)** |
| Mire mirror    | 50/50, **37.2 turns** | 50/50, **9.3 turns** |

What it surfaced:

1. **Attrition needs time it doesn't get.** Mire loses to Frost ~56% at *both*
   skill levels — its Wound engine wants a long game, and Frost's burst kills it
   (15 HP) before Wounds pile up. A grinder that can't survive can't grind.

2. **Reading rescues the Steele matchup.** Under greedy play Steele's fat stats
   crush Mire 67%; under reader play Mire pulls dead even. Wound disruption plus
   pattern-punishing exactly offsets Steele's HP/Body edge — the same
   skill-inversion the Frost/Steele pair showed, now with a different mechanism.

3. **The deck is skill-sensitive in *duration*, not just outcome.** The greedy
   mirror drags to 37 turns (neither pilot closes — Equal Footing floors and low
   aggression stall out); the reader mirror ends in 9. A deck whose *game length*
   triples with pilot skill is a genuine design signal.

Takeaway for the table: Mire is matchup-polarized in PvP — it beats grinders and
loses to burst. Its real home is PvE, where durable monsters give the Wound
engine the long game it's built for. That's the sim telling you where the deck
belongs.

## The errata queue

Every assumption the engine made beyond the written rules prints at the end of a
run and is collected in `rulings-log.md`. Some are already resolved (Gambler's
Ruin, Blood Tithe mutual death); others are simplifications flagged for a later
call. That log is the real reason to run this.

## Files

- `engine.py` — combatant state, resolution loop, tokens, dice, ruling log
- `content.py` — the two decks; every card's Effect and Defensive Bonus
- `policies.py` — decision brains
- `run.py` — Monte Carlo runner and reporting
- `rulings-log.md` — assumptions surfaced, resolved and open
