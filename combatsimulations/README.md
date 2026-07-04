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
- **reader** — predicts the opponent's *most-frequent* attack color and counters
  it. Sounds smart; the tournament shows it's the weakest non-random brain (see
  below). Kept as a cautionary control.
- **greedy** — attacks for max expected damage; defends by predicting the foe's
  *last* color. The strongest of the simple brains.
- **tactician** — greedy's recency-read and aggression, plus the one upgrade that
  helped without hurting any deck: valuing Axiom's color ban (and an unpreventable
  Spark to finish a low foe). The overall strongest brain.

Add your own by implementing three methods (see the module docstring).

## Findings (20k duels per cell, seeds fixed)

A full policy tournament (every brain vs every brain, same deck both sides)
produced three results, one of which reversed an earlier conclusion.

1. **Recency beats frequency — decisively.** The `reader` predicts an opponent's
   *lifetime* most-common color; `greedy` predicts their *last* color. Greedy
   crushes reader head-to-head: **59/41 in the Frost mirror, 90/10 in the Mire
   mirror.** Lifetime frequency goes stale; the last card thrown is a far better
   predictor of the next one. Any real player already knows this — the sim just
   put a number on it. (An earlier draft of this file called reader the strong
   brain. It was never tested head-to-head against greedy. It is not.)

2. **Raw stats win the deck matchup; Axiom narrows but doesn't flip it.** Under
   the strongest brain (tactician), the deck ranking is **Steele > Frost > Mire**:

   | | vs Steele | vs Frost | vs Mire |
   |---|:--:|:--:|:--:|
   | **Steele** | — | 56.5% | 67.0% |
   | **Frost**  | 43.5% | — | 67.1% |
   | **Mire**   | 33.0% | 32.9% | — |

   Steele's Body 4 / HP 18 beat everyone. Valuing **Axiom** is real and
   measurable — it wins the Frost mirror 59/41 and lifts Frost's score vs Steele
   from 38.8% (greedy) to 43.5% (tactician) — but it does **not** overturn
   Steele's stat advantage. Axiom is an edge, not an "I win" button. *(The earlier
   "Frost dominates under skill" claim was an artifact of testing with the weak
   reader brain — corrected here.)*

3. **Anti-read flattening is a trap.** A policy that deliberately varied its own
   attack colors to be unpredictable *lost* — it only helps a deck whose
   off-colors are as strong as its main color (Frost), and for stat-skewed or
   combo decks "unpredictable" just means "playing weak cards." Cut from the
   tactician. Worth knowing at the table: don't sandbag your best color to be
   cute unless your other colors are genuinely as threatening.

Initiative is worth ~52–55% under strong play — an edge, not a verdict.

Caveat that cuts the other way now: these are still just four hand-written
brains. Greedy/tactician are strong but not optimal — a bluff-aware or
lookahead policy could shift the deck ranking again. Treat the numbers as "how
the decks behave under the best brain we've written so far."

## Mire — the Wound-attrition deck (3/3/3)

A third deck (`mire` in the roster): Balance, Wither, Mockery / Rend, Equal
Footing, Press the Wound / Partition, Taint, Erode. Perfectly balanced 3R/3B/3G.
It wins by shuffling Wounds into the opponent's deck (Rend, Taint) and cashing
them in (Press the Wound), while eroding stats for the whole combat (Wither
−Body, Erode −Soul). Adding it forced the engine to grow real Wound mechanics,
combat-duration stat loss, initiative shift, and targeting locks.

Win rates under the strongest brain (tactician, 20k duels each):

| Matchup | result |
|---------|:------:|
| Mire vs Frost  | Frost 67.1% |
| Mire vs Steele | Steele 67.0% |
| Mire mirror    | 50/50, ~9 turns |

(Only Wither's Body loss shaves max HP — Body's derived value; Erode drains Soul
and Sunder drains Mind without touching HP. See the Stat Loss rule.)

What it surfaced:

1. **Attrition needs time it doesn't get.** Under strong play Mire loses ~67% to
   *both* Frost and Steele — its Wound engine wants a long game, and both decks
   close the 15-HP grinder before Wounds pile up. A grinder that can't survive
   can't grind. (Note: against the weak `reader` brain Mire looks competitive —
   even beating Steele — but that's reader mis-defending, not Mire winning. Under
   greedy/tactician the illusion evaporates. A good example of why the policy you
   test with determines the answer you get.)

2. **Wound payoff is too slow for a duel.** Press the Wound scales with Wounds in
   the opponent's deck, but seeding enough of them takes more turns than an
   aggressive opponent grants. The cards are individually fine; the *engine* needs
   a longer game than PvP provides.

Takeaway for the table: Mire is bottom-tier in a duel — it loses to burst and to
raw stats alike. Its real home is PvE, where durable monsters give the Wound
engine the long game it's built for. That's the sim telling you where the deck
belongs, not that the deck is weak.

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
