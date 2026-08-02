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
  it. Sounds smart; the tournament shows it's the weakest non-random brain.
  Cautionary control.
- **greedy** — attacks for max expected damage; defends by predicting the foe's
  *last* color. Strongest of the simple brains.
- **tactician** — greedy's recency-read and aggression, plus two upgrades that
  help without hurting any deck: valuing Axiom's color ban (and an unpreventable
  Spark to finish), and a **situational deck-tracking safety check** — if a color
  the foe needs to beat your attack is fully exhausted into their discard, that
  attack is risk-free (finding 4). **The strongest general brain.**
- **punisher** — the tactician plus card conservation against a color-reliant
  opponent: hoard the counter to their dominant color instead of spending it on
  attacks. Purpose-built to punish stat-maxing (finding 5). Beats the tactician
  only against mono-color foes; ties it otherwise.

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

2. **Raw stats top the ranking; Axiom narrows but doesn't flip it.** Under the
   strongest brain (tactician), the deck ranking is **Steele > Mire > Frost**:

   | | vs Steele | vs Frost | vs Mire |
   |---|:--:|:--:|:--:|
   | **Steele** | — | 66.7% | 60.9% |
   | **Frost**  | 32.6% | — | 39.2% |
   | **Mire**   | 38.6% | 59.7% | — |

   (Mire jumped over Frost once its self-Wound cost was removed — see the Mire
   section. Steele's Body 4 / HP 18 still beat everyone.)

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

4. **Deck-tracking is situational, not predictive — and that distinction is the
   whole finding.** A first attempt used deck-state to *predict* the foe's next
   color (decklist minus discard → what they can still draw). It lost ~85% to the
   recency brain: decks are tiny and reshuffle constantly, so "what's left" barely
   predicts the next draw, and a heavily-played color depletes fastest — fooling
   availability-prediction right before a reshuffle hands it back. Pure tracking
   was removed.

   But tracking has one narrow, *certain* use: **safe-play detection.** If you
   know the foe holds only 2 green cards and you see both in their discard, then
   green is gone from their deck and hand — so any attack green can beat is
   risk-free (it cannot lose the reveal). That check is now folded into the
   tactician (`_color_exhausted`), and it's pure upside: it lifted the tactician
   over greedy across *every* deck (Frost 59%→65%, Mire 50%→58%). The lesson:
   don't track to guess what's coming; track to know when you can't lose.

5. **Stat-maxing is a trap, not a threat — the system self-corrects on two
   independent axes.** A Body-5 (the cap) red-heavy deck, "Volk," is the classic
   dump-everything-in-one-stat build. It *loses*:

   | Volk (Body 5, 7 red) vs | tactician | vs a `punisher` brain |
   |---|:--:|:--:|
   | Frost (balanced 3/3/3) | 21.0% | **9.7%** |
   | Steele (4/3/2)         | 24.2% | 24.0% |
   | Mire (3/3/3)           | 64.7% | 39.9% |

   Two forces punish it at once:
   - **RPS hard-counter.** Spam one color and a defender who holds the counter
     wins *every* reveal. The `punisher` brain (hoard the counter to that color,
     never spend it attacking) takes Frost from 78% to **89%** against Volk —
     Drew's anti-mono idea, and it works.
   - **Wasted off-stat cards.** To stop being predictable you diversify — but on a
     5/2/2 line your blue/green cards hit for Mind/Soul 2. A Body-5 deck with
     *balanced* colors is mediocre too (40–48% vs the field): unpredictable but
     toothless.

   So maxing loses whether you go mono (countered) or diverse (weak off-stat
   cards). **The actually-strong build is Steele's 4/3/2** — a high primary for
   power plus a secondary high enough to keep a second color genuinely
   threatening. That's not maxing, it's a spread. If any allocation is "too
   strong," it's the moderate one, and the lever would be **Body's double-dip**
   (it buys damage *and* HP), not anything about maxing. The stat economy already
   discourages dumping points into one stat — the sim just proved it.

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
| Mire vs Frost  | **Mire 59.7%** |
| Mire vs Steele | Steele 60.9% |
| Mire mirror    | 50/50 |

(Only Wither's Body loss shaves max HP — Body's derived value; Erode drains Soul
and Sunder drains Mind without touching HP. See the Stat Loss rule.)

What it surfaced — including a fix loop that worked:

1. **The sim caught a self-inflicted balance bug, and the fix landed.** When the
   Wound rule changed so Wounds no longer auto-discard (they sit in hand until you
   spend an action), Mire's own **Wither/Erode/Sunder** — which used to shuffle a
   Wound into *your own* deck as a cost — started drowning the deck in its own
   costs. Mire cratered to ~23% vs Frost. The sim flagged it; the self-Wound cost
   was removed from those cards; Mire jumped to **59.7% vs Frost.** A clean
   design-loop: sim surfaces the problem → card change → sim confirms the fix.

2. **Mire is a real PvP deck now — against balance, not against stats.** Freed of
   its self-cost, the Wound-disruption engine (permanent hand-clog + Press the
   Wound + stat erosion) beats Frost's balanced burst. It still loses to Steele —
   Body 4 / HP 18 close the game before attrition matters. Attrition beats
   tempo-neutral decks and loses to raw-stat aggression. That's a healthy,
   legible matchup triangle.

3. **Reader-brain illusion, for the record.** Against the weak `reader` brain Mire
   looked ~even with Steele; under strong play that evaporates. A reminder that
   the policy you test with determines the answer you get.

Takeaway for the table: Mire went from bottom-tier to mid-tier in one card change
the sim identified. Its ceiling is still PvE, where durable monsters give the
Wound engine a long game — but it's no longer a trap pick in a duel.

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
