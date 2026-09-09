# Archives — Cut Cards

Cards that didn't make it to canon. Kept for reference. Some may find solutions later.

---

## Core set — cut in the colour-identity pass

**RALLY**
RED — BODY
Attack: Body + d4
Effect: Pay 5 HP, all allies in Frontline gain Deadly
Defense Effect: Pay 5 HP, all allies in the Backline gain Deadly
Range: Both
*"Blood shared is strength doubled."*

*Cut 2026-09-09, dominated by a card in another colour. WARSONG did everything RALLY did and more — bigger die, no HP cost, every ally rather than one position, and a defence half that wasn't a repeat of its attack half. Rather than nerf WARSONG, WARSONG moved to Red (its name was always martial, and "all allies gain Deadly" is a damage buff) and took RALLY's place. PROVOKE moved with it. Green was handing out Deadly on ten cards to Red's seven, in the colour whose identity is support rather than damage; it now holds eight to Red's nine.*

## Core set — cut as a three-way duplicate

**GIVE WAY**
GREEN — SOUL
Attack: Soul + d4
Effect: Gain Evade.
Defense Effect: Gain Evade.
Range: Both
*"Meet it and you break. Move and it passes."*

*Cut 2026-09-08. GIVE WAY and SHADE AWAY had been identical for as long as both existed — same colour, same die, same range, same text on both halves — and GIVE WAY had already lost its Oracle seat to TWIN STRIKE in the green pass for exactly that reason.*

*SWAY was cut alongside it the same day and for the same reason: its rewrite to "Gain Evade" on both lines made it the third copy. It did not stay cut. Its original text — move the defender to the other position, gain Quick on defence — went to the Root Heart as a signature card (`cards/root-heart-weald.md`), where an Immobile boss that repositions everyone but itself is the better home for it than the core list ever was. It took BRISTLE's slot in that deck.*

*So the core list is down one Evade card, not two, and its Green decklist seats moved: the Haywight took SHADE AWAY, whose Evade its passive already leans on, and the Gluttony Abomination took MIRROR STEP, which closes the distance the way SWAY used to. The Root Heart's "no card moves it" ruling cited SWAY as its example and now cites CALCULATE — the creature holds the card and still cannot be moved by it.*

*Replacing GIVE WAY: GUIDE, the first card in the pool that grants Evade to somebody else. Nine Evade cards existed before it and every one of them pointed at its own caster.*

## Core set — cut with the Critical keyword

**EXPOSED**
BLUE — MIND
Attack: Mind + d4
Effect: If the defender is Staggered, this attack has Critical.
Defense Effect: Gain Evade.
Range: Both
*"You don't need strength. You need them to already be falling."*

*Cut 2026-09-07, and the Critical keyword went with it. EXPOSED was the only card in the entire core pool that used Critical, and it had already been removed from the Oracle in the blue pass — so the glossary was carrying a full definition for something no player would ever meet. A keyword with one user is not a keyword, it is that card's text.*

*The card was also doubly dead in a deck that no longer inflicts Staggered: with the Oracle down to a single gated Staggered card (OFF BALANCE), its attack half almost never fired, leaving a d4 that reads "Gain Evade" on defence and nothing on offence.*

*Critical had three live references outside this card, all in equipment, and all were kept by writing the effect out longhand — "double this attack's base damage" — rather than by keeping the keyword: `rules/equipment.md`'s spiky-effects pricing note and its Tier 3 weapon example, and the design note on THE SILENT BLADE (`items/the-silent-choir-items.md`) that cites that example as precedent. The Trisect's decklist cited EXPOSED and now runs MARKED in the slot (`bestiary/trisect.md`).*

## Core set — cut with Staggered's removal from the Oracle

**FALTER** *(was SECOND GUESS)*
BLUE — MIND
Attack: Mind + d4
Effect: Defender gains Staggered.
Defense Effect: Attacker gains Staggered.
Range: Melee
*"The step that does not land where it meant to."*

*Cut 2026-09-06. Staggered came out of the Oracle entirely that day — a status that eats a whole attack or a whole defence is a swing the starting deck should not hand out freely, and four cards were handing it out. Red keeps one, OFF BALANCE, and only on a clean win. This card had no gate and no colour left to sit in: at d4 Melee it was also Blue paying twice, the smallest die at the tightest range, which is the defect that surfaced it in the first place.*

## Core set — cut as strictly dominated

**HESITATE**
BLUE — MIND
Attack: Mind + d4
Effect: Apply Initiative Shift -1 to the defender.
Defense Effect: Apply Initiative Shift -1 to the attacker.
Range: Melee
*"You watched them decide. That took a moment they needed."*

*Cut 2026-09-06: DISTRACT is the same card, better. Same colour, same Melee range, same symmetric Initiative Shift on both halves — but a d6 against HESITATE's d4, and -2 against its -1. Bigger die and bigger effect at once leaves no board state where you would rather hold this one. The pair only collided when DISTRACT was added to the Oracle earlier the same day to fill PREDICT's melee slot; nobody checked it against the melee Initiative Shift card already sitting there.*

---

## Core set — folded into another card

**INTERCEPT**
RED — BODY
Attack: Body + d4
Effect: Gain Protect and Resist 2
Defense Effect: Gain Protect and Resist 2
Range: Melee
*"Stand between the storm and what you protect."*

*Cut 2026-09-06: GUARD absorbed it. GUARD had been "All allies gain Resist" on both halves; it now reads "Gain Protect and Resist" — INTERCEPT's shape at INTERCEPT's die and range — and carries INTERCEPT's flavor text, which was always the better line for the body-blocking card. Two Red d4 Melee cards were doing one job; now one does it.*

---

## Core set — cut as a duplicate

**BRACE** *(green)*
GREEN — SOUL
Attack: Soul + d4
Effect: Gain Resist.
Defense Effect: Gain Resist.
Range: Both
*"Hold."*

*Cut 2026-09-06: two problems, one card. It was mechanically identical to ABIDE (`cards/green-soul.md`) — same colour, stat, die, range, and both effects — and its name collided with the Red BRACE in `cards/red-body.md`, the only duplicate name in the whole card corpus. The collision was created by the SETTLE → BRACE rename on 2026-08-26, which renamed this card onto a name that was already taken. It mattered because `printing/generate-cards.py` resolves a set's fixed card list by name into a dict, so whichever file parses last silently wins; five bestiary decks cite BRACE in their red sections and the Oracle cited it in its green one. The Oracle's green slot now holds ABIDE, which does the same thing under a name that carries the same weight for a noncombat Advantage discard.*

---

## Core set — cut following the keyword-glossary trim

Drew cut Obscure, Reveal Hand, Expose [Color], Locked, Sealed, and Future-Lock X from `rules/card-glossary.md` (2026-09-06). Every core-pool card built on one of those keywords moves here; creature and character decks keep theirs as printed — the cut is a glossary trim, not a retroactive rewrite of everything that ever used the term.

**PREDICT**
BLUE — MIND
Attack: Mind + d6
Effect: Defender gains Sealed
Defense Effect: Attacker gains Sealed
Range: Melee
*"Tomorrow's victory begins with today's preparation."*
*Cut: Removed from `cards/blue-mind.md` — built entirely on Sealed, cut from the glossary.*

---

**VOID**
GREEN — SOUL
Attack: Soul + d6
Effect: Defender gains Sealed
Defense Effect: Attacker discards 1 card at random
Range: Ranged
*"Even emptiness has its own terrible weight."*
*Cut: Removed from `cards/green-soul.md` — same reason as PREDICT, above.*

---

**READ**
GREEN — SOUL
Attack: Soul + d6
Effect: The defender must reveal their hand.
Defense Effect: Name a color then choose a card in the attacker's hand. If colors match, discard it.
Range: Ranged
*"You tell the truth with your eyes."*
*Cut: Removed from `cards/green-soul.md` — its Effect is Reveal Hand in plain English rather than the keyword's own name, which is why the original glossary-trim sweep missed it. Reveal Hand itself is retired outright, not relocated like Locked or Obscure, so this one has no replacement pending — unlike PREDICT and VOID above, which were only cut because Sealed no longer has a core-pool home. `places/the-silent-choir.md`'s "Ringing Silence" section named this card specifically as the reason its silent-hand-reveal house rule exists; that section still needs a look now that the card it was written around is gone.*

---

## Core set — cut during Drew's full card review pass

**SEED**
GREEN — SOUL
Attack: Soul + d4
Effect: Exile 1 card from your hand. Deal its damage in retaliation the next time you are damaged by an attack from the defender.
Defense Effect: Exile 1 card from your discard.
Range: Both
*"What appears lost may simply be waiting for the right season."*
*Cut: Removed from `cards/green-soul.md` by Drew, no reason stated beyond wanting it gone — name and flavor kept for reuse per his explicit request.*

---

## Vescal — cut during deck rebalance

**INCENSE WARD**
GREEN — SOUL
Attack: Soul + d6
Effect: Target ally gains Ward.
Defense Effect: Gain Ward.
Range: Both
*"What the smoke touches, the world cannot take."*
*Cut: Vescal's deck ran Green 7/Blue 2/Red 2 against a Mind 3/Body 4/Soul 3 target — Drew picked this one to go rebalancing the color split back to stat totals.*

---

**TOPPLE RESTORED**
GREEN — SOUL
Attack: Soul + d6
Effect: Heal target ally 4 HP. Move them to any position.
Defense Effect: Heal yourself 3 HP.
Range: Both
*"The scales don't care where you're standing."*
*Cut: same rebalance as INCENSE WARD, above.*

---

**OPEN DOOR**
GREEN — SOUL
Attack: Soul + d6
Effect: Target ally draws 1 card and heals 2 HP.
Defense Effect: Draw 1 card.
Range: Ranged
*"The door is always open. That's the point."*
*Cut: same rebalance as INCENSE WARD, above.*

---

## Borrower — Hollow (mediation arc Oracle reward)

**SHORE UP**
RED — BODY — HOLLOW
Attack: Body + d6
Effect: Target ally heals 3 HP.
Defense Effect: Gain Resist.
Range: Melee
*Cut: Passed red team but CRAWL LANE was more interesting as an Oracle reward — teaches movement over raw healing.*

---

**DEEP STOCK**
RED — BODY — HOLLOW
Attack: Body + d6
Effect: If you have 3 or fewer cards in hand, heal 4 HP.
Defense Effect: Draw 1 card.
Range: Both
*Cut: Passed red team. Niche conditional — interesting but not the right fit for 3-card signature set.*

---

**DECOY**
BLUE — MIND — HOLLOW
Attack: Mind + d6
Effect: Force target enemy to attack a different target on their next turn.
Defense Effect: Gain Ward.
Range: Both
*Cut: Passed red team. CLAY BOWL was cleaner and more distinctly Borrower. May find a home later — misdirection mechanic is good.*

---

**REDIRECT**
BLUE — MIND — HOLLOW
Attack: Mind + d6
Effect: Name a color. If target plays that color this round, their attack deals -3 damage.
Defense Effect: Scry 1.
Range: Both
*Cut: Passed red team. Good color-prediction mechanic. Crowded out by CLAY BOWL.*

---

**SOFT STEP**
GREEN — SOUL — HOLLOW
Attack: Soul + d4
Effect: Gain Evade. All allies in your position gain Evade.
Defense Effect: Move to any position.
Range: Both
*Cut: Ruled on by Drew, 2026-08-05 — fine at creature/Borrower power level, too strong for players. Stays out of the Oracle (or any player-facing pool) as written; not a balance failure at the creature level, a player-facing power ceiling issue specifically.*

---

**SOFT WARNING**
GREEN — SOUL — HOLLOW
Attack: Soul + d4
Effect: Name a color. Until start of your next turn, allies take -2 damage from that color.
Defense Effect: One ally draws 1 card.
Range: Both
*Cut: Passed red team. Ongoing color-keyed damage reduction is solid. Crowded out by TUNNEL KNOWLEDGE.*

---

## Rootstalker — Weald

**WOODEN MOCKERY**
GREEN — SOUL — WEALD
Attack: Soul + d8
Effect: Target must discard a card of the same color as the one they just blocked with. If they can't, they must reveal their hand.
Defense Effect: Attacker takes 3 damage.
Range: Both
*"The stalker's face is a knot that mimics your own terror."*
*Cut: Two-condition effect plus non-keyword Defense Effect. Too complex for table use.*

---

## Briarwatch Wardens (exploratory run — naming mixup with Alignment Marshal)

*These cards were generated during a session where "Warden" was used in error instead of "Alignment Marshal." The Marshal set is complete. These are kept in case a Briarwatch Warden encounter is developed later.*

**CAVE PACE**
RED — BODY — BRIARWATCH
Attack: Body + d6
Effect: Shuffle 1 Exhaust into target's deck.
Defense Effect: Gain Resist.
Range: Both
*"Limestone. Water. One more hour."*

---

**THICK SOLE**
RED — BODY — BRIARWATCH
Attack: Body + d6
Effect: Anchored — At the start of your turn, your attacks deal +2 damage.
Defense Effect: Gain Ward.
Range: Melee
*"Plant once. Everything else is noise."*

---

**GROUND HOLD**
RED — BODY — BRIARWATCH
Attack: Body + d8
Effect: Target gains Rooted.
Defense Effect: Anchored — At the start of your turn, heal 2.
Range: Melee
*"Once a Warden grabs you, the cave has you."*

---

**WARDEN'S READ**
BLUE — MIND — BRIARWATCH
Attack: Mind + d6
Effect: Expose Red — target gains Blind.
Defense Effect: Scry 2.
Range: Both
*"They watched you pick up that rock three steps back."*

---

**TRACK SIGN**
BLUE — MIND — BRIARWATCH
Attack: Mind + d6
Effect: Scry 2.
Defense Effect: Target gains Blind.
Range: Both
*"Scratch marks at knee height. Wet limestone. They know exactly what moved through here."*

---

**WARDEN'S MARK**
BLUE — MIND — BRIARWATCH
Attack: Mind + d4
Effect: If target has Exhaust in their deck, deal +4 damage.
Defense Effect: Gain Evade.
Range: Both
*"They knew before you did."*

---

**WARDEN INSTINCT**
GREEN — SOUL — BRIARWATCH
Attack: Soul + d6
Effect: Move to Backline.
Defense Effect: Scry 1.
Range: Both
*"They stopped returning from the Weald. The ones who stayed learned to read when to step back."*

---

**HOLD YOUR POST**
GREEN — SOUL — BRIARWATCH
Attack: Soul + d6
Effect: An ally may reposition freely.
Defense Effect: Gain Resist.
Range: Both
*"No signal needed. They already know."*

---

**QUIET SIGNAL**
GREEN — SOUL — BRIARWATCH
Attack: Soul + d4
Effect: One ally gains Evade.
Defense Effect: Gain Evade.
Range: Both
*"A look. That's all."*

---

## Stonecoil — Hollow (stress test run, 9-card batch)

**TERRITORIAL SWEEP**
RED — BODY — HOLLOW
Attack: Body + d6
Effect: If target attempts to move this round, deal +3 damage.
Defense Effect: Counter Attack.
Range: Melee
*Cut: Timing unresolvable. Condition checks a future event within the same resolution window.*

---

**DEAD AIR**
BLUE — MIND — HOLLOW
Attack: Mind + d4
Effect: Target discards 1 card at random.
Defense Effect: Gain Ward.
Range: Ranged
*Cut: Duplicates BLANK (blue-mind.md).*

---

**CHOKE POINT** *(v1)*
BLUE — MIND — HOLLOW
Attack: Mind + d6
Effect: Target cannot move to Backline until end of your next turn.
Defense Effect: Gain Evade.
Range: Melee
*Cut: Mechanically equivalent to Rooted in extra words.*

---

**STONE PATIENCE** *(v1)*
GREEN — SOUL — HOLLOW
Attack: Soul + d6
Effect: Anchored — your attacks deal +2 damage.
Defense Effect: Apply Rooted to attacker.
Range: Melee
*Cut: Duplicates DIG IN (red-body.md) — only color differs.*

---

**SCENT OF FEAR**
GREEN — SOUL — HOLLOW
Attack: Soul + d6
Effect: If target has fewer cards in hand than you, deal +3 damage.
Defense Effect: All enemies in Frontline gain Blind until start of your next turn.
Range: Melee
*Cut: Mass Blind defense effect duplicates FOGBURST. Hand-count condition also complex to track for a small creature deck.*


---

## Alignment Marshal — dropped in the canon revision (salvaged from experimental/alignment-marshal-cards.md before cleanup)

**CORRECTIVE MEASURE**
GREEN — SOUL — ENGINE
Attack: Soul + d4
Effect: Gain Evade.
Defense Effect: Gain Resist.
Range: Both
*"The correction mechanism corrects itself."*

---

**PLATFORM SHOVE**
RED — BODY — ENGINE
Attack: Body + d6
Effect: Target moves to Frontline.
Defense Effect: Anchored — Your attacks deal +2 damage.
Range: Both
*"Interference is relocated, not removed."*

---

**SEQUENCE LOCK**
BLUE — MIND — ENGINE
Attack: Mind + d4
Effect: Target gains Debuff.
Defense Effect: Gain Ward.
Range: Both
*"The sequence will not be interrupted."*

---

**TRAJECTORY HOLD**
GREEN — SOUL — ENGINE
Attack: Soul + d4
Effect: Gain Ward.
Defense Effect: Gain Resist.
Range: Both
*"It does not deviate."*
