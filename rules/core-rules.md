# Tales Untold — Quick Reference

---

## Stats

| Stat | Damage | Other |
|------|--------|-------|
| Body | Red cards | Max HP = (2 × Body) + 9 |
| Mind | Blue cards | Hand size = Mind (minimum 2) |
| Soul | Green cards | Initiative = 1d6 + Soul |

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

## Combat — 1 Action Per Turn

| Action | Notes |
|--------|-------|
| Play a Card | Attack using a card from hand |
| Move Position | Frontline ↔ Backline |
| Use an Item | Activate a carried item |
| Rushdown | Move a Backline enemy to the Frontline. You must be in the Frontline to use this action. |
| Take Cover | Backline only; fiction must justify it. Gain Evade until you attack. |
| Interact | Any noncombat action |
| Flee | 2d10 + Soul vs DC 10 + highest enemy Soul, GM-adjusted for fiction |

Draw to hand size when **initiative is rolled**, then at the **start** of each of your turns.

---

## Attack Resolution

1. Attacker plays 1 card, face down.
2. Defender may choose 1 card to defend with, face down — blind, without seeing the attacker's card. The card must meet its own Range requirement for the current positions, same as if the defender were attacking (see Range Matrix below) — no legal card in hand means no legal defense.
3. No defense → attacker wins automatically.
4. Both reveal simultaneously — only now do they become public and move to discard — and resolve RPS:

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
| d6 | Raw power |
| d4 | Utility |
| d2 | Precision & control |

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

- Reach **0 HP** → Collapse (cannot act, cannot defend, auto-hit)
- Reach **−(Max HP ÷ 2, rounded up)** → Death
- Every **3 in-game hours** Collapsed → recover **1d4 HP**
- GM may declare instant death if the fiction demands it

---

## Resting

| Rest | Duration | Effect | Limit |
|------|----------|--------|-------|
| Short | 20 min | 1d6 + Body HP, all Exhaust destroyed | 3/day |
| Long | 7½ hours | Full heal, all Injuries and Exhaust destroyed | Once/day |

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

**Rushdown** — Move a Backline *enemy* to the Frontline. Cannot target allies. You must be in the Frontline.

---

## Stealth & Ambush

Soul check vs DC = 10 + highest Soul on the side being approached. Creatures ambush the same way — the GM rolls their Soul check. On success, first attack auto-hits (no RPS). Then roll initiative for everyone — ambusher included — and play normal combat.

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
Carried items can be used via the Interact action.  
Artifacts are resonant jewelry aligned with a Seat's domain.

See `rules/equipment.md` for the Weapon/Armor tier system and design guidance, and `rules/items.md` for the full catalog of items already in the world.

---

## Advancement

**End of session:** each player runs the Oracle ritual — **Name** (answer her question), **Price** (1 card revealed, then buried back into the pool — seen, not taken), **Distance** (GM reveals 3 → player takes 1). See `locations/island-in-a-ship.md`.  
**Stat increases:** Rare. After pivotal character development. GM's call.  
**Deck changes:** Cards can be added, removed, or forced in as curses/status.

---

## Important Rule

### YOU ARE NOT YOUR OWN ALLY!
