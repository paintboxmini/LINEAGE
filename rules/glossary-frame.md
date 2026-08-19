# Card Keyword Glossary

Canonical definitions for all keywords and status cards used in Tales Untold. When a card uses a keyword, this is the ruling. Card text that contradicts this file should be treated as an error.

This file is meant to be printed and handed to players. State the rule, plainly, and stop — no *why* it's shaped that way, no *how* the simulator happens to implement it. Most of the time that reasoning doesn't need a home at all; if it's a live design question worth remembering, it goes in `memory.md`, not here.

**Special Rule** — some cards carry a Special Rule line instead of, or alongside, an Effect and Defensive Bonus. It overrides normal resolution exactly as printed on that card.

---

## Keywords

**At the table — status-effect tokens.** A card that grants a temporary status — a Debuff or a Positive Status Effect, landing on you, an ally, or a foe — doesn't need a separate physical token. The card *is* the token: set it face-up in front of whoever it's affecting instead of sending it straight to the discard pile, and discard it for real once the effect resolves, triggers, or expires. Same physical technique Ongoing Effects already use (`rules/combat.md`). Not just a bookkeeping convenience: the card is out of its owner's rotation the whole time it's serving as a token — it isn't in their discard pile, so it isn't coming back on a reshuffle either. That's a real cost on whoever cast it, whether the card debuffed a foe or buffed an ally.

<!-- KEYWORDS -->

---

## Stat Change

Not a keyword — a shared mechanic. Some cards change one of your stats for a combat (Sunder drains Mind, Wither drains Body, Erode drains Soul; other cards may raise a stat). A changed stat uses its new value for everything it governs, in real time:

- **Body** — Red-card damage, and max HP at **3 points per point of Body** (down when lost, up when gained) — the heaviest of the three shares, matching the HP formula's own weighting: (3 × Body) + Soul + Mind.
- **Mind** — Blue-card damage; hand size (equal to Mind, minimum 2 — hand size never drops below 2, however far Mind falls; changes the moment the stat does, and a hand already above the new, lower size is not discarded down, it simply can't draw back up until it naturally falls below the cap); and max HP at **1 point per point of Mind**.
- **Soul** — Green-card damage; initiative (1d6 + Soul, applied to rolls made after the change); and max HP at **1 point per point of Soul**.

**All three stats touch max HP** *(changed 2026-08-06 to match the HP formula's own three-stat shape — Body at 3×, Mind and Soul at 1× each; previously Body was the only stat that did)*. If a loss puts your current HP above the new maximum, current HP falls to the maximum; if your maximum reaches 0 you Collapse. Increasing max HP does not increase current HP.

A stat change lasts for the combat unless a card says otherwise, then the stat — and any max HP, hand size, or initiative it moved — returns to normal. This applies to every current and future stat-changing card; the card only states the stat and amount.

---

---

## Status Cards

Status cards are placed into decks as consequences. They cannot be played. They must be managed.

<!-- STATUS CARDS -->
