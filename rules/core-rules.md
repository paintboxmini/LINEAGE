# Tales Untold — Quick Reference

---

## Stats

| Stat | Damage | Other |
|------|--------|-------|
| Body | Red cards | Max HP = (3 × Body) + Soul + Mind |
| Mind | Blue cards | Hand size = Mind (minimum 2); also feeds Max HP |
| Soul | Green cards | Initiative = 1d6 + Soul; also feeds Max HP |

---

## Difficulty Classes

| Difficulty | DC |
|------------|----|
| Easy | 11 |
| Normal | 13 |
| Hard | 16 |
| Extreme | 19 |

Roll **2d10 + relevant stat.** Meet or beat the DC.  
Discard a card whose name supports the action → Advantage (roll 3d10, drop lowest)

---

## Combat — 1 Action per turn

| Action | Notes |
|--------|-------|
| Play a Card | Attack using a card from hand |
| Move Position | Frontline ↔ Backline, or Rushdown - reposition a Backline enemy to Frontline (this counts as you moving, not the enemy) |
| Use an Item | Activate a carried item |
| Take Cover | Backline only; fiction must justify it. Gain Evade until you attack. |
| Interact | Any noncombat action |
| Flee | 2d10 + Soul vs DC 10 + highest enemy Soul, GM-adjusted for fiction |

Draw to hand size when **initiative is rolled**, then at the **start** of each of your turns.

---

## Attack Resolution

1. Attacker plays 1 card, face down.
2. Defender may choose 1 card to defend with, face down — **The chosen card must satisfy its own Range requirement for the current positions, exactly as if the defender were attacking the attacker** — a Melee card cannot defend unless both combatants are Frontline; Ranged cards can't be used to block a Melee attack while on the Frontline.
3. **Blind, then Evade, resolve next** — Blind checks the attacker's own stack; Blind and Evade checks the defender's.
4. No defense → attacker wins automatically.
5. Both reveal simultaneously — only now do they become public and move to discard — and resolve RPS:

```
Blue (Mind)  beats  Red   (Body)
Red  (Body)  beats  Green (Soul)
Green (Soul) beats  Blue  (Mind)
```

**Attacker wins** → damage + Effect  
**Defender wins** → no damage + Defensive Bonus  
**Tie** → no damage. Attacker's Effect still triggers, then Defensive Bonus triggers. If the Effect cancels the Defensive Bonus, Defensive Bonus does not trigger. (An Effect that only adds to *this attack's damage* — exploding dice, "+X damage" — does nothing on a tie; there's no damage to add to.)

---

## Card Anatomy

**Name / Color — Stat / Attack: Stat + die / Effect / Defensive Bonus / Range: (ranged/melee/both) / Flavor**

| Die | Philosophy |
|-----|------------|
| d8 | Raw power |
| d6 | Utility |
| d4 | Precision & control |

*(d10 exists on a small number of cards as a deliberate outlier above this scale — never a fourth named tier.)*

| Range Term | Meaning |
|------------|---------|
| Melee | You and the target must be in Frontline |
| Ranged | Works only while not in Melee range with the target |
| Both | Either position valid |

---

## Perception Modes

| Mode | Stat | Use When... |
|------|------|-------------|
| Reason | Mind | Noticing *what* something is |
| Senses | Body | Noticing *when or where* something happens |
| Read | Soul | Noticing *what something intends or signifies* |

*(Renamed 2026-07-22 — "Observe" implied eyesight specifically, which reads as Body's territory, not Mind's; "Sense" (singular) risked blurring with Soul's own mode. Mind is reasoning/deduction, Body is the physical senses, Soul is instinct/intuition — that line is now sharp in the names themselves, not just the "Use When" column.)*

---

## Collapse & Death

- Reach **0 HP** → Collapse. You are on the ground — **Down**
- While Down: cannot attack, cannot defend (attacks auto-hit), cannot change position
- Healing above 0 ends the Collapse but does not stand you up — **standing costs your action**
-  2 follow up hits after Collapse → Death
- GM may declare instant death if the fiction demands it

---

## Resting

| Rest | Duration | Effect | Limit |
|------|----------|--------|-------|
| Short | 20 min | 2d6 + Body HP, all Exhaust removed (hand/deck/discard) | 3/day |
| Long | 7½ hours | Full heal, all Wounds and all Exhaust removed (hand/deck/discard) | Once/day |

Short rests can be chained. Long rests require genuine safety.

A rest of either length reshuffles your discard pile into your deck and refreshes your hand to full.

---

## Positioning

Every combatant occupies **Frontline** or **Backline**. Each side has its own Frontline and Backline — the two Frontlines face each other at the center of combat. Both are abstract zones — any number of characters can share either position. Moving costs your action for the turn.

### Range Matrix

| Attacker | Target | Melee | Ranged | Both |
|----------|--------|-------|--------|------|
| Frontline | Frontline | ✓ | ✗ | ✓ |
| Frontline | Backline | ✗ | ✓ | ✓ |
| Backline | Frontline | ✗ | ✓ | ✓ |
| Backline | Backline | ✗ | ✓ | ✓ |

Melee requires both characters in the Frontline. The Frontline does not protect the Backline from being targeted.

---

## Stealth & Ambush

Soul check vs DC = 10 + highest Soul on the side being approached. On success, first attack auto-hits (no RPS). Then roll initiative for everyone — ambusher included — and play normal combat.

---

## Chase

Two-marker track. Fleeing party starts at a position equal to their head start in exchanges; pursuer starts at 0. Standard track is 5 steps past the fleeing party's start — extend for larger gaps. Each exchange: contested Soul (2d10 + Soul), winner advances 1 step. Caught = pursuer reaches them. Escaped = fleeing party reaches the end of the track.

Discard a card whose name fits → Advantage.

---

## Cover

Taking cover is an action. You must be in the Backline, and the fiction must justify it — there must be something to take cover behind.

While in cover, you gain **Evade** (see `rules/card-glossary.md`). Making an attack drops cover immediately.

---

## Equipment Slots

**Weapon / Armor / Artifact**  
Only equipped items have permanent passive effects — everything else about how a character dresses or arms themselves is free, unrestricted fiction.  
Carried items are used via the Use an Item action, or your Item Action.  
Artifacts are resonant jewelry aligned with a Seat's domain.

See `rules/equipment.md` for the Weapon/Armor tier system and design guidance, and `rules/items.md` for the full catalog of items already in the world.

---

## Advancement

**End of session:** each player gains a new card from the Oracle deck.  
**Stat increases:** Rare. After pivotal character development. GM's call.  

---

## Important Rule

### YOU ARE NOT YOUR OWN ALLY!
