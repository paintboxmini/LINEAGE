# The Compiled Crib

A practical efficiency tool, not one of the canonical domains (`CLAUDE.md`, Canonical Content; the original four-kinds framing is preserved at `archives/four-kinds-of-canon.md`) — it's a precompiled digest of facts the generators would otherwise re-derive from full canon reads every run: engine facts, calibration numbers, format templates. It cuts across Rules, World, and Content for speed; it doesn't hold canon of its own. **This file is a build artifact, not a source of truth** — every fact here has a canonical home, cited inline. When canon changes underneath it, add this file to **Pending Propagation** in `unresolved-concerns.md` and refresh it at the next Sync. If a pattern gets retrieved repeatedly to rediscover it, that's the signal to promote it into this file rather than re-deriving it next time.

For actual best-in-class Tales Untold content — the pieces worth reading to calibrate what excellent looks like — read the content itself or the relevant archive; there's no separate exemplar registry anymore (`agent-tools/design-principles.md`, Use). This file stays a cheat-sheet either way.

Read this + the target's location/bestiary file + anything your specific task actually touches. Go to the full canon files only when the task bends a rule, the crib looks stale, or you're checking a keyword's exact text — the Keyword crib below covers the common cases, and marks which entries have subtleties it doesn't carry.

---

## Engine facts generators always need

*(sources: `rules/combat.md`, `rules/core-rules.md`, `rules/card-glossary.md`)*

- RPS: Blue beats Red beats Green beats Blue. Tie = no damage; attacker's Effect fires first, then Defensive Bonus (damage-amplifying effects do nothing on a tie).
- Reveals are simultaneous and blind. Defending is a prediction, not a reaction.
- **Hand size = Mind, minimum 2.** Blocking spends a card; hand is blocking capacity between turns.
- HP = (3 × Body) + Soul + Mind is the baseline every generator offers; bosses may go bespoke, marked explicitly. **Deck size = total stats** (color counts = each stat; signatures count toward their color). **Creature Threat Rating = total stats** — the difficulty scale; player baseline is 9, scaling with party size (N players ≈ 9N).
- **Range counts derive from the same stat numbers as color counts, reassigned to range buckets**: Mind → Ranged, Body → Melee, Soul → Both. Within each range bucket, color mix should approximate the deck's overall color percentages rather than concentrating one color into one bucket (e.g. every Ranged card also being Blue) — that leaks color from publicly-known range legality during RPS prediction. Default starting point, not a hard constraint — real decks may deviate for a stated reason (Crimson/Sky, `combatsimulations/content.py`, lean into Frontline/Backline specialization on purpose rather than following this default). Worked example, Mind4/Body3/Soul2 (colors Blue4/Red3/Green2): ranges Ranged4/Melee3/Both2, each internally ~4/9 Blue, ~3/9 Red, ~2/9 Green. *(Drew's heuristic, 2026-07-28.)*
- Positions: Frontline / Backline. Melee needs both frontline; ranged needs not-both-frontline; "Both" always legal.
- Initiative: tokens placed clockwise in initiative order; a turn marker starts at 12 o'clock and advances one token per turn. **Wait** = forfeit action, choose a later slot (the party's sequencing tool). **Initiative Shift X** always moves the token the full distance — positive counterclockwise (never later), negative clockwise (never sooner); when that would violate the guarantee, a skip or bonus chip preserves it instead of altering the move. Full mechanic: `rules/combat.md`, `rules/card-glossary.md`; worked cases: `rules/initiative-shift-examples.md`.
- Standard DC 13. Perception modes: Reason (Mind) / Senses (Body) / Read (Soul).
- Status cards (Wound, Exhaust) go into decks — the delayed-consequence system.
- Approved keywords (short forms in the Keyword crib below; canonical texts in `rules/card-glossary.md`; list maintained in `experimental/README.md`): Anchored, Blind, Counter Attack, Deadly, Debuff, Evade, Exile, Protect, Initiative Shift X, Lifesteal, Locked, Obscure, Quick, Resist, Rooted, Rushdown, Scry X, Sealed, Staggered, Thorns X, Unpreventable, Ward, Weak. **No new keywords without discussion.**

## Keyword crib

One line each, for the common cases. **`rules/card-glossary.md` is the ruling** — anything marked † has timing or stacking subtleties this line does not carry, so read the full entry before writing a card that leans on it. Ordered by how often cards actually use them.

| Keyword | Short form |
|---|---|
| **Evade** (56) | 50% to dodge the next attack on you, checked before the defender picks a card. Separate check from Blind; both can apply. |
| **Resist** (52) | Next successful attack on you deals half, rounded down. Expires on that attack. Cancels 1-for-1 with Vulnerable. |
| **Scry X** (31) | Look at the top X of a deck (your own unless stated). Put each on top, on the bottom, or in the discard, in any order. |
| **Rooted** (30) † | Cannot voluntarily change position until end of your next turn. |
| **Initiative Shift X** (25) † | Positive moves the target X counterclockwise on the wheel, negative X clockwise. Positive never makes them act later; negative never sooner. With exactly 3 combatants, reduce the magnitude by 1 first. |
| **Blind** (21) † | 50% to miss. Rolled 1d2 after the attacker commits, before the defender picks. Lasts until end of your next turn. |
| **Staggered** (21) | The next attack you make *or* defense you'd mount is skipped — whichever comes first. Ends the instant it happens. |
| **Thorns X** (21) | Deal X to any enemy that hits you in melee. Stacks additively into one value; not consumed. |
| **Weak** (19) | Subtract an extra d6 from your next damage roll. Each stack covers one future roll. Cancels 1-for-1 with Deadly. |
| **Deadly** (17) | Add an extra d6 to your next damage roll. Each stack covers one future roll. Cancels 1-for-1 with Weak. |
| **Ward** (15) | Prevents the next Debuff applied to you. Automatic, no declaration. Expires on use. |
| **Anchored** (13) † | A stated benefit persists while you do not change position, triggering at the start of each of your turns. Ends immediately if you move or Collapse. The card names who it targets — not always yourself. |
| **Vulnerable** (9) | Next successful attack on you deals 50% more, rounded down. Each stack covers one future attack. Cancels 1-for-1 with Resist. |
| **Exile** (7) | Out of play for the rest of combat — not the discard, not retrievable. Returns to the owner's discard when combat ends. A status card exiled is destroyed outright. |
| **Counter Attack** (6) | Deal this card's Attack damage back to the attacker. |
| **Quick** (5) † | Change position without spending your action. On your turn, usable that turn; gained off-turn, held to end of your next. Fades whether spent or not. |
| **Sealed** (5) | No item use — Action, Item Action, or equipped passive — until end of your next turn. |
| **Armour X** (4) | Reduce all incoming attack damage by X, every attack, whole fight. Not consumed, never expires. Stacks additively. |
| **Lifesteal** (4) | Heal half the damage this attack actually landed on HP, rounded down — measured after Resist and any other reduction. |
| **Rushdown** (4) | Move a target enemy Backline → Frontline. Enemies only, and the user must be in the Frontline. |
| **Unpreventable** (4) † | Ignores every defense that applies to attack damage — Armour, Resist, damage floors, redirects. Thorns, status damage and HP costs are all unpreventable. |
| **Immunity** (3) | The next attack against you fails completely, before any reveal. One use. |
| **Protect** (3) | The next time an ally would take attack damage, you take it instead. |
| **Critical** (1) | Base damage (stat + die, including Deadly/Weak already rolled in) doubled, before any other bonus. Not a carried status — each card states its own trigger. |
| **Locked** (1) | That card cannot be played, until end of combat unless stated otherwise. |
| **Obscure** (1) | Enemies cannot look at or manipulate your hand or deck. Does not stop status cards entering your deck. |
| **Reveal Hand** (1) | State your colour counts, e.g. "2 Red, 1 Blue" — not the cards themselves. |
| **Debuff** | Umbrella: Weak, Blind, Vulnerable, Staggered, Rooted, stat reductions. What Ward and Deflect prevent. |
| **Positive Status Effects** | Umbrella: Evade, Resist, Deadly, Protect, Anchored, Quick, Immunity. A card naming the term means all of them. |

Counts are card usage as of 2026-08-17 and drift; they indicate which keywords are worth knowing cold, not an audit. **Not here on purpose:** Future-Lock X, which is no longer a card keyword — it lives with the only thing that applies it (`bestiary/future-lock-wasp/`).

**Do not inline these onto cards.** Measured 2026-08-17: putting each definition on every card that uses it duplicates ~92,000 characters against a glossary of 18,000 read once, and an agent reads decks and buckets rather than single cards. `agent-tools/card-creation.md` forbids it, and Expose was retired partly for exactly that drift.

## Creature Threat Rating calibration (real anchors)

*(sources: `CLAUDE.md` Stat Blocks; the bestiary files named. Creature Threat Rating = total stats; player baseline 9.)*

| Creature Threat Rating | Reads as | Anchors |
|---|---|---|
| 4–6 | teaching creatures: one lesson, simple loop, often disengages | Scratcher 4 · Jackalope 5 · Borrower 6 |
| 8–10 | a real fight: defining passive, interacting cards | Stonecoil 8 · Fogcaller 9 · Tollbird 9 · Vescal 10 |
| 11+ | above a player: named threats and bosses; toughness comes from stats | Orin Vane 11 · Root Heart 11 · Masaharu 12 · Minotaur 14 · Trisect 15 |

Stats read Mind/Body/Soul. If the brief doesn't state a target Creature Threat Rating, ask before building.

## Card format + two calibrated exemplars

*(sources: `CLAUDE.md` card format; `cards/buckets/green.md`; `cards/tollbird.md`)*

Core card (universal — no tag; die philosophy: d8 power / d6 utility / d4 precision):

```
**SUPPORT**
GREEN — SOUL
Attack: Soul + d4
Effect: Target ally gains Deadly
Defensive Bonus: Target ally draws 2
Range: Ranged
*"Strength flows to those who share it."*
```

Signature card (one source tag = where it's obtained, per `world/lineage.md`; tighter identity — an effect only this creature would have; Effect ≠ Defensive Bonus):

```
**WATCHFUL PERCH**
GREEN — SOUL — BRIARWATCH
Attack: Soul + d6
Effect: Move to the Backline and gain Evade.
Defensive Bonus: Apply Initiative Shift +2 to yourself.
Range: Both
*"Still is not the same as gone."*
```

Enemy deck: **size = total stats, color counts = each stat** (signatures count toward their color); 3 signature + core to fill. Range counts derive the same way — see Engine Facts above. "Ally" wording must survive **You Are Not Your Own Ally** (`rules/cards.md`) — no color is exempt.

## Stat block skeleton

```
**Mind X / Body X / Soul X — HP X**
**Creature Threat Rating:** N
```

Bestiary files open with `**Cards:** \`cards/name.md\`` when signature cards exist, and should list a **recommended full deck** (3 signature + core picks, sized and colored to the stat line — see `bestiary/tollbird/README.md` for the full pattern; backfilling older entries is queued work). Named people go in `characters/`, never `bestiary/`.

## Encounter skeleton

*(exemplars: `quests/hollow-below-briarwatch.md` — Surface Layer, `places/briarwatch.md` — The Larder Fence)*

`# Name` → *italic one-line placement note* → **Intent** (what it teaches, through play not explanation) → **Setup** (environment, positioning constraints) → **Enemies** (who + deck) → **GM notes** (behavior, triggers, when to let the lesson land) → **Win Condition** → **Related Documents**.

## NPC voice (Function / Pressure / Hook)

*(exemplars: Aege/Bartho/Kino in `places/vultures-nest.md`; Weck in `characters/weck/README.md`)*

Four lines of Weck, as the register to hit: *a cart that doesn't smell like animals; buys culls at fair prices, never early, never late; will buy one Wound for coin and your name in his ledger, in your own hand; answers questions honestly and unhelpfully, which is worse.* — Function (buyer), Pressure (the terms), Hook (the ledger, deliberately unanswered). Refusing is always a complete answer. NPCs embody rules; they never explain them.

## Tone in one breath

*(source: `world/tonal-bible.md`)*

Horror comes from comprehension, not confusion. Beauty and wrongness occupy the same space. The mundane and mythic coexist without the world pausing to notice. Sacrifice costs something the world doesn't refund. Not grimdark, not heroic fantasy, not whimsy — the world was never organized around you.
