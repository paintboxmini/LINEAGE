# Tales Untold — Quick Reference

*Internal reference — GM and design use. **Not** the player-facing document; players receive `rules/player-guide.md` only. Keep this accurate anyway: it feeds new content, so an error here propagates.*

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

## Combat — 1 Action + 1 Item Action Per Turn

| Action | Notes |
|--------|-------|
| Play a Card | Attack using a card from hand |
| Move Position | Frontline ↔ Backline |
| Use an Item | Activate a carried item |
| Rushdown | Move a Backline enemy to the Frontline. You must be in the Frontline to use this action. |
| Take Cover | Backline only; fiction must justify it. Anchored — Evade. Ends when you attack or leave the Backline. |
| Interact | Any noncombat action |
| Wait | Take no action; reinsert yourself anywhere later in the order. Can't be used two turns in a row. See `rules/combat.md` |
| Flee | 2d10 + Soul vs DC 10 + highest enemy Soul, GM-adjusted for fiction |
| Grapple | Contested check to grab and hold an enemy. Both are Rooted and neither may act except to break out |
| Stand Up | Get off the ground while Down (needs HP above 0) |
| Destroy a Wound | Destroy 1 Wound from your hand |
| Rest in Place | Destroy every Exhaust in your hand at once |

Your Item Action does exactly what its name says and nothing else. Your Action may also be spent to Use an Item instead of one of the options above — a combatant who spends both this way uses 2 items in one turn, at the cost of not attacking (or otherwise acting) that turn.

Draw to hand size when **initiative is rolled**, then at the **start** of each of your turns.

---

## Attack Resolution

1. Attacker plays 1 card, face down.
2. Blind (attacker's stack), then Evade (defender's stack) resolve — both before the defender picks a card.
3. Defender may choose 1 card to defend with, face down — blind, without seeing the attacker's card. The card must meet its own Range requirement for the current positions, same as if the defender were attacking (see Range Matrix below) — no legal card in hand means no legal defense.
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
- Reach **−(Max HP ÷ 2, rounded up)** → Death
- Every **3 in-game hours** Collapsed → recover **1d4 HP**
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

**Rushdown** — Move a Backline *enemy* to the Frontline. Cannot target allies. You must be in the Frontline.

---

## Stealth & Ambush

Check vs DC = 10 + highest Soul on the side being approached — Soul is the obvious stat, any arguable one works. Players roll their own; the GM rolls for creatures. On success the first attack auto-hits: no RPS, no defense, no Evade or Protect — reactions need awareness, properties (Armour, Resist, Thorns, Immunity) always apply, and the attacker's own Blind still rolls. **One auto-hit for the side, not one each.** Then roll initiative for everyone, ambusher included. A creature whose entry defines its own ambush uses that instead.

---

## Chase

Track only the distance between them; the fiction sets where it starts. Each exchange, a contested roll (Soul obvious, any arguable stat) — winner moves the distance one step their way. Discard a card whose name fits → Advantage. **Distance 4 = escaped** (pursuer may try the trail after, GM-set DC). **Distance 0 = contact:** the chase ends, no free attack, but the pursuer takes the first turn — then picks: fight, grapple (contested check to grab or pin; `cards/subdue.md` is its card), or use whatever they were chasing with. Starting distance is the difficulty dial: 1 catches three times in four, 2 is even, 3 escapes three times in four.

---

## Cover

Taking cover is an action. You must be in the Backline, and the fiction must justify it — there must be something to take cover behind.

**Anchored — Evade.** One when you take cover, one at the start of each of your turns after. Ends the instant you attack, if you leave the Backline by any means, or if you Collapse.

---

## Equipment Slots

**Weapon / Armor / Artifact**  
Only equipped items have permanent passive effects — everything else about how a character dresses or arms themselves is free, unrestricted fiction.  
Carried items are used via the Use an Item action, or your Item Action.  
Artifacts are resonant jewelry aligned with a Seat's domain.

See `rules/equipment.md` for the Weapon/Armor tier system and design guidance, and `rules/items.md` for the full catalog of items already in the world.

---

## Advancement

**End of session:** each player runs the Oracle ritual — **Name** (answer her question), **Price** (1 card revealed, then buried back into the pool — seen, not taken), **Distance** (GM reveals 3 → player takes 1; the other 2 go back or leave the pool, GM's call). See `places/island-in-a-ship.md`.  
**Stat increases:** Rare. After pivotal character development. GM's call. No stat may exceed another by more than 3 — player characters only; creatures and NPCs are built differently.  
**Deck changes:** Cards can be added, removed, or forced in as curses/status.

---

## Important Rule

### YOU ARE NOT YOUR OWN ALLY!
