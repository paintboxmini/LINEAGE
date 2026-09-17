# Card Tiers

Three pools, in order of when a table meets them. A card sits in exactly one.

| Tier | File | What it holds |
|------|------|---------------|
| Beginner | `beginner.md` | Cards cleared for a first campaign. The Oracle 63 and the expansion 21. |
| Middle | `middle.md` | Cards that are good and are not beginner cards. Most are legal under every rule and simply hit too hard, too early. |
| High | *not built* | Reserved. Nothing has been written for it. |

**The tiers are about when, not about quality.** A card in `middle.md` is not a worse card than one in `beginner.md` — usually it is a better one. TURN redirects an incoming attack onto somebody else and spends the attacker's buffs doing it, which is a more interesting card than most of the beginner pool. It is in the middle tier precisely because it is that good.

**Everything that fails the beginner screen lands here.** The screen and its four bars live in `rules/early-campaign-cards.md`; this directory holds the lists it produces. A card that fails a bar is not cut — it moves. That is the whole point of having a second tier: the older answer to "too strong to start" was to rewrite the card until it was weak enough, and that is how TURN lost its redirect for a year and became unresolvable in the process.

**Moving a card between tiers.** Change it here, and check three things: whether it is seated in a set (`printing/generate-cards.py`), whether any creature or character deck runs it (`bestiary/`, `characters/`), and whether the keyword counts in `rules/card-glossary.md` still hold. A tier move on its own changes none of those — tiers are about eligibility, not about where a card is printed — but a card usually moves tiers because its text changed, and text changes do move all three.

**What is not here.** A card that is beginner-legal but simply has no seat in a set is still a beginner card — PRESSURE and INTERCEPT are both eligible and both unseated. And 82 cards in the core lists have never been screened at all, so neither list is finished. Blue dominates `middle.md` for exactly that reason: it is the only colour that has been read end to end.

---

## Related Documents

- `rules/early-campaign-cards.md` — the screen, its four bars, and the evidence each one was tested against
- `rules/cards.md` — the Oracle content rule, which is bar 3, and the colour conventions
- `printing/generate-cards.py` — which cards are actually seated in a printed set
