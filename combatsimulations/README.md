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
- Exactly Frost's and Steele's decklists (`testcampaigndecks/`). Ally-only
  effects are correct no-ops in a duel and are marked DEAD in `content.py`.

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
