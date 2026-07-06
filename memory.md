# LINEAGE — Memory

**What belongs here:** active threads, mid-session decisions, things in flight that the repo can't capture on its own.

**How to write entries — this is a THRESHOLD log, not a changelog.** Every entry records the *crossing*: what the thing WAS before, WHY it changed, and what it became. A bare "X is now Y" is incomplete — the value is in the before-state and the reasoning, so a later reader (or a reversal) can see the pressure that moved it. Prefer "was A because P; changed to B because Q" over "is B."

**What doesn't belong here:** keyword definitions (see `rules/card-glossary.md`), workflow rules (see `CLAUDE.md`), location summaries (see `locations/`). If it has a canonical home elsewhere, it goes there.

---

## Campaign Status

**Session 1 played.** Party: Frost (Ollie, Mind 3/Body 3/Soul 3, HP 15) and Steele (Kevin, Mind 3/Body 4/Soul 2, HP 17 under new HP formula) — two members, test run. They made it halfway to Briarwatch. Decklists recorded in `testcampaigndecks/frost.md` and `testcampaigndecks/steele.md`, Oracle picks logged (Frost: Spark of Violence; Steele: Paradox). Directory holds this campaign's decks only: players, Oracle pool, campaign-specific NPCs.

**Combat simulator** (`combatsimulations/`)
PvP duel engine, Python, no dependencies. Roster: frost, steele, mire (pluggable via `ROSTER` in content.py; run.py takes deckA polA deckB polB). Four brains: random/reader/greedy/tactician. Design instrument only — not canon. Outputs: errata queue (`rulings-log.md`, printed each run) + balance stats.

Corrected findings (an earlier draft tested with the weak `reader` brain and wrongly concluded Frost dominates):
- **Recency beats frequency.** greedy (predicts foe's LAST color) crushes reader (predicts MOST-COMMON color) head to head — 59/41 Frost mirror, 90/10 Mire mirror. reader is the weakest non-random brain.
- **Deck ranking under strongest brain (tactician): Steele > Mire > Frost.** Steele's Body 4 raw stats win (red damage + balanced colors, not HP).
- **Axiom is a real edge, not an "I win."** Valuing Axiom wins the Frost mirror 59% and lifts Frost vs Steele 38.8%→43.5%, but does NOT flip Steele's stat advantage. (Earlier "Axiom > Paradox, Frost dominates" was overstated — Axiom helps, stats win.)
- **Anti-read color flattening FAILS** — only helps a deck whose off-colors are as strong as its main color; cut from tactician.
- Initiative ~52–55% under strong play.
- **Mire is bottom-tier in PvP** (loses ~70% to both Frost and Steele). Home is PvE, where durable enemies give the Wound engine its long game.
- **Deck-tracking is situational, not predictive.** A pure `tracker` brain (predict next color from deck-minus-discard) FAILED (~85% loss) — tiny reshuffling decks make "what's left" a bad predictor. Removed. But tracking's narrow CERTAIN use — safe-play detection (if all copies of a color are visible in the foe's discard, an attack that color can't beat is risk-free) — is real: folded into the tactician (`_color_exhausted`), lifted it over greedy across every deck (Frost 59→65%, Mire 50→58%). Lesson: track to know when you can't lose, not to guess what's coming.
tactician = best brain (greedy recency-read + aggression + Axiom/Spark weighting + situational exhaustion safe-play).

**Wound rule (Drew):** Wounds no longer auto-discard — sit in hand occupying a slot until an action discards one (→ discard pile) or short rest. Short-rest removal: permanently destroy 1 Wound from HAND or DISCARD only (never deck — no tracking/searching hidden Wounds). Press the Wound counts HAND + DISCARD only (not deck), for the same reason. Debuff scope: stat reduction + status-card infliction ARE debuffs (Ward blocks); discard + scry-your-deck are NOT (ignore Ward; Obscure answers those). Stat change drives derived value live: Body→maxHP (only Body touches HP), Mind→hand size (forces discard if over), Soul→initiative; both directions. All in glossary + sim.

**Self-Wound cost REMOVED from stat-reduction cards (Drew):** Sunder (Mind), Erode (Soul), Wither (Body) no longer "Shuffle 1 Wound into your deck" — that self-cost was crippling under persistent Wounds. Sim confirmed: Mire went ~23% → 59.7% vs Frost. New deck ranking under tactician: Steele > Mire > Frost (Mire jumped Frost). Wound-removal cards (Press def, Taint def, Field Medicine, Shed Skin) now say "destroy" (permanent) not "exile" (which returns at combat end), and remove from hand/discard only. Clean design loop: sim flagged bug → card fix → sim confirmed.

**Stat-maxing finding:** stat-maxing is a TRAP, not a balance problem — the system self-corrects on two axes. Tested a Body-5 red-heavy deck ("volk" in roster): loses to balanced Frost 21%, crushed 89% by the anti-mono `punisher` brain (hoards the counter color to the foe's dominant color — Drew's idea, it works). Mono-color → hard-countered by RPS. Balanced colors on a 5/2/2 line → off-stat cards hit for Mind/Soul 2, toothless (~40-48% vs field). The actually-strong build is Steele's 4/3/2 (high primary + viable secondary color), which is a spread, not a max. If anything's too strong it's the moderate spread, and the lever would be Body's double-dip (damage + HP), not stat allocation. `punisher` and `volk` added to sim.

**Sim next step:** the real goal is a full TEAM-vs-TEAM simulator. Current 1v1 is step one — some cards (Mockery taunt, Partition shield, ally buffs) correctly do nothing in a duel and wait for the team sim. Not expanding to teams yet.

---

## Active Pending Threads

**SOFT STEP** (Borrower card, `experimental/archives/cut-cards.md`)
Mass Evade for position-mates. Passed red team but flagged as strong — needs Drew's deliberate sign-off before entering the Oracle. Don't promote to canon without asking.

**Pendragon Arc** (`world/the-regency.md`, `mythology/seats.md`)
Bones are in place. What's locked: five original council members + Pendragon attempted Seat of Love/Binding, failed, Aurora held. Pendragon didn't die — became something. Connection to Gluttony Abomination in bestiary is a possible thread, not confirmed. Whether the council turned on him or he paid the full price is unresolved. Don't develop further without Drew.

**Gluttony Abomination** (`bestiary/gluttony-abomination.md`)
Raw content. Tales Untold adaptation pending. Possible Pendragon connection. Don't develop without Drew.

**Phase-Leach** (`bestiary/phase-leach.md`)
Stat block pending. Six-legged panther of violet smoke, blinks/teleports, feeds on arcane energy. No mechanics yet.

**Roadhouse → Turnroot Weald hook**
After the party resolves the Hollow Below Briarwatch, Aege (the Carrion Guide) hands them a sealed letter pointing them to the Turnroot Weald — four days west. Hook: her family says the forest's predators are acting strange. She can't go herself. She watched the party on the road and decided they move carefully enough to trust. See `locations/vultures-nest.md` for the full letter and "Finding Aege" GM guidance.

**B thread — Quartermaster Voss**
Secondary hook, only activates if party explored the Roadhouse barracks and found the posting order. Unsigned line: "anything from the docks that isn't in the manifest." Points to unsanctioned smuggling from Vulture's Nest to the capital. Voss is at Eclipsera South Gate. Voss's intake reports are cross-referenced against Jonas's ledger — condoned goods appear in both. The supply chain that doesn't appear in either is the FourthEye thread. Don't develop until party pulls on it.

**FourthEye pipeline**
Drug spreading through Eclipsera's Underground Bazaar (Giblets' stall is the bazaar-end node). Supply chain runs from Vulture's Nest, bypasses Jonas's ledger entirely, never appears in Voss's intake. Masaharu is at the Nest tracing it backward. Identity of the Nest-side operator: unknown. Giblets' "plan connected to someone he used to work with" is the forward-pointing thread. Three Regency hard lines violated: too addictive, too destructive, council gets no cut. See `locations/vultures-nest.md` (Masaharu, Rumors) and `locations/underground-bazaar.md` (Giblets).

**Kess & Moth — Bazaar recurring characters** (`locations/underground-bazaar.md`)
Now fully wired in. Kess: granddaughter of the Cartographer, using Cartographers Guild as cover, working methodically toward paying off debt and exiting. Her mother died in the mine — imprisoned illegally by the Warden as leverage against the Cartographer's network. Kess went in with Giblets to fix it; something went badly wrong; Mortis pulled them out; she sold the memory. Has tattoo echoes including one that reacts near Giblets' stall. Knows where the grandmother's mine map is. Has plans that extend past her own exit — potential future bazaar uprising organizer. Moth: freely spending swines, no apparent interest in escape, coin purse that never empties, wildcard. Kess finds him maddening. Mortis knows the full story of the mine and has never mentioned it to either of them.

**The Descended** (`bestiary/the-descended.md`)
Former humans from the deep. Range through cave system, upper limit is Diamond Shelf. Crouch-run in open passages, seamless transition to belly-slither at shelf entrance. Primary drive: drag things deeper. Collapsed characters are prioritized — dragged toward fissure, DM judges pace. Demon Court uses them as deterrent through whisper/fear — nobody knows what they are, only what happens. Stat block: Mind 2 / Body 3 / Soul 1, HP 15.

**The Diamond Shelf** (`quests/the-wallows-descent.md`)
Labor level, far end of main corridor. Nearly-exhausted diamond vein. Two-foot ceiling, belly crawl. Fissure splits it — prisoners cross to reach ore. Initiates guard from entrance side. Descended in back section. Worst assignment in the Wallows. DC 13 Body/Sense to cross fissure cleanly.

**The Wallows** (`locations/the-wallows.md`, `factions/demon-court.md`, `quests/the-wallows-descent.md`)
Mine beneath Eclipsera. Five layers: bazaar → labor level → threshold → deep (Aurora). The Boar built it knowingly above Aurora's binding site. Labor level runs on proximity compliance — workers feel Aurora's warmth as patience. Threshold: sticky echoes, slimes, cave reaches. Alternate exit threads through the threshold to outside the city walls — the Cartographer's map shows this route. Aurora at the bottom: not an encounter, dissolution through love. Don't develop the deep without Drew. Quest file written: two pressure tracks (Demon Court awareness / Seat influence), modular encounter nodes, hidden behavioral rules for the Seat track.

**Wallows Slime** (`bestiary/wallows-slime.md`)
Threshold creature. Reaches, envelops, doesn't attack. Warm. Forcing extraction raises Seat Influence by 1. Gentle extraction does not. Stat block pending.

**Warden Pazuzu / The Demon Court** (`factions/demon-court.md`)
Pazuzu runs the Wallows labor operation for the Boar. Built his guard hierarchy as a mirror of the Regency council — demon masks instead of animal titles. Tiers: Pazuzu (apex), Overseers (armored, unarmed), chain whip guards, Initiates (yellow, entry checkpoint). Direwolves for pursuit — trained to operate in the upper threshold. Pazuzu considers himself the Boar's eighth councillor. The Regency does not acknowledge the Demon Court. Pazuzu has never gone to the deep and has not examined why.

**Lord Archibald — the Boar** (`world/the-regency.md`)
His official animal title is the Boar. Informally called the Pig — never to his face. Lore/formal files use Boar. Everyday references (bazaar, street-level) stay as Pig. Pig debt, swines, etc. unchanged.

**Bazaar uprising thread** (future)
Kess is positioned as a future organizer: Cartographers Guild network, grandmother's intelligence cache, personal grievance, methodical temperament. Moth as wildcard (nothing to lose). FourthEye pipeline crossing Regency hard lines as potential lever. Don't develop without Drew — flag as long thread.

**Canille** (`experimental/canille.md`)
Island village in a lake northeast of Vulture's Nest. Research colony founded by scientists attempting to create sentient life. Three generations of scientists and cubs. Cubs are quadrupedal, pug-faced, ~120lbs, fully furred. White smiling masks on hooks by every door — ceremony, not disguise. Key characters: Hess (oldest founder, knows the answer, won't say it), Cob (third-gen cub, asks the questions nobody will answer). Not yet canon.

**Road encounters**
Day 1 travel between Vulture's Nest and Briarwatch is now the Briarwoods. Jackrabbits and Briar Scratchers are present. No formal random encounter table yet — DM discretion. Shifting Burrow (`quests/shifting-burrow.md`) is an alternate encounter for parties exploring off the road near Briarwatch.

**Black Maggie** (`experimental/black-maggie.md`)
Last survivor of the Thessians — nomadic healers who transferred and witnessed suffering. Archon: MoroM, Seat of Witnessed Suffering. Maggie performs torture-sacrifice at ritual sites. 100 sacrifices = site permanently haunted, anchors MoroM's plane to held reality. Seven sites total — six completed, possibly working on seventh. Maggie is the 700th sacrifice (herself), completing the permanent binding. The haunting feels like grief, not malevolence. Site count and Maggie's current location open. Don't develop further without Drew.

**Thessian lore delivery:** sprinkle world history through found objects — an old tavern song (words half-corrupted, shape still intact) about seeking a nomad healer in great suffering; a book on a forgotten shelf, possibly dismissive, written by someone who never witnessed the gift firsthand. Neither should announce itself. Let the party find it and file it away until it matters.

**Senshi / The Naturalist Collection** (`locations/gilded-tusk.md`)
All 12 bestiary entries written. Senshi is Thessian — horns hidden under chef's hat at all times, short-tempered, food is sacred.
- Non-combat entries complete: unity-jelly, phantom-tail-slug, high-altitude-bat, emerald-frog, bicolor-spider, sapphire-ant
- Hazard entries complete: future-lock-wasp (deck contamination, 20min removal after drawn, Body/Soul save), death-ball-sponge (Rooted floor trap, DC 13 spot)
- Full stat blocks complete: gene-thief-tardigrade, bone-collector, flapjack-octopus, elder-tower-creature
- Environmental entries complete: elder-tower-creature (harvest tubes, patience puzzle)
- **Pending:** Flapjack Octopus card set — drafted in `experimental/cards-flapjack-octopus.md`, needs Drew's sign-off on placement
- **Pending:** Future-Lock status card needs glossary entry before canon — new keyword, requires approval
- Bone Collector wired to Gilded Tusk (Senshi commission) and Turnroot Weald (Web-Forest POI)
- Future-Lock Wasp wired to Turnroot Weald (Hanging Gallery POI)
- Abyssal Trench created (`locations/abyssal-trench.md`) — oceanic sub-area with sponge hazard, octopus, elder towers

**Mirel / Steve / Pip / Kaine** (`characters/mirel.md`, `experimental/steve-and-pip.md`, `experimental/kaine.md`, `experimental/lightning-loop.md`, `quests/tide-pulls-back.md`)
Two story arcs in development. Tide Pulls Back adventure written — four encounters, Mirel opening hook, Void Runners dock fight, Final Current lodge infiltration, Kaine climax at Full Tide ceremony. Steve's bathing happens at the ceremony — pulleys get stuck, he's down too long, Pip forms on the way up. Lightning Loop ends in party's hands as unresolved problem. Mirel's ending is open. Kaine not necessarily dead. Pip arc is its own separate quest — party chooses to intervene or not, fallout is emergent. Don't pre-write the Pip resolution. Storm Seat confirmed as valid (Seats file is not exhaustive).

---

## Key Design Decisions (This Project)

**The Unheld is a hard edge; sailing lives on rivers**
Nothing sails or fishes the Unheld Ocean — it is the true edge of reality, not a soft boundary. No islands exist in it. The only exceptions: Glasslight light-cartographers map its edge (never the water), and the People of Promise touch it deliberately (ritual bathing = transgression as worship). Ghost stories preserve the memory of ships that once went past the coast; Corvel is living proof. The continent is laced with interconnected rivers and lakes draining toward the Unheld — Vulture's Nest is the heart of the river web. Tides are an Unheld phenomenon that breathes up the rivers (when the grey water pulls back, rivers drop inland — this keeps the Tide Pull and the Glasslight tide framework working). **The coastline is a hard threshold: unheldness does not cross it, by flowing or by being carried — inland water is mundane, only the tidal motion travels upstream.** This is why Promise bathing must happen at the coast, and why Corvel's vials are ordinary water (what they carry is Pneum's diseases, not unheldness — see `experimental/pneum.md`). The Island in a Ship is unchanged: the Oracle's island is now the only location in the setting not on the continent. Former Unheld islands (Canille, Pneum) relocated to lakes. Eclipsera's Temple of the Sea renamed Temple of the Rivers.

**Stat loss reduces the stat's derived value** (`rules/card-glossary.md`, Stat Loss)
General rule, not a keyword: a card that reduces a stat for a combat (Sunder→Mind, Wither→Body, Erode→Soul) lowers whatever that stat governs. Body loss → −3 max HP per point (Body's derived value; clamps current HP, can Collapse). Mind loss → hand size. Soul loss → initiative. Only Body touches HP. Reverts at combat end. Every current/future stat-draining card inherits this. Sim: `combatsimulations/engine.py` Combatant.erode (Body-only HP).

**Soul = movement speed**
Soul governs initiative AND movement speed. High Soul characters move faster and act first. This is why flee/chase uses Soul, not Body. Body is impact, not velocity. Important for future card and mechanic design — don't use Body for movement checks. Flee is now formalized: 2d10 + Soul vs DC 10 + highest enemy Soul (ambush formula from the other side), GM-adjusted for terrain/obstacles/position/enemy intent — see `rules/combat.md`, Fleeing Combat. Enemies don't roll to flee; enemy disengagement is a GM behavior call.

**Abstract movement**
No distances in play. "In reach / close / far" is the language. Combat uses abstract positions (Frontline/Backline). When a character moves away from the combat area, that ends the combat — flee function. Enemies can re-engage. Non-combat chasing uses Soul checks. Avoid specific distances in any bestiary or quest content.

**Quick reference is `rules/core-rules.md`**
Canonical rules quick reference. Covers stats, DC table, combat actions, attack resolution, card anatomy, positioning, collapse, resting, cover, stealth/ambush, chase.

**Initiative is a continuous wheel**
Turn order is a closed loop, not a list that resets each cycle — there are no rounds (see `rules/combat.md`). Seat count equals combatant count; shifts wrap at the ends. Initiative Shift X (`rules/card-glossary.md`) is the only way card effects move someone in the order — it guarantees a positive shift never delays a target's next turn and a negative shift never accelerates it, and large shifts (|X| ≥ seat count) decompose into full revolutions plus a remainder. Slipstream and Synchrony (`cards/blue-mind.md`, `cards/green-soul.md`) are the first cards to treat wheel position itself as a build-around.



**Seats & Echoes** (`mythology/seats.md`, `mythology/echoes.md`)
Seats are fixed metaphysical positions — structural features of reality. Echoes are beings whose identity has aligned with a Seat's domain (Resonance → Alignment → Incarnation/Archon). Failed Seat-takers are the most powerful and least stable Echoes.

**The Pendragon Attempt** (`world/the-regency.md`)
The Regency council was originally an adventuring party. They attempted to claim the Seat of Love/Binding together. Failed. Aurora held. The five survivors (Oswald, Cedric, Elara, Archibald, Eveline) became the original council members — each losing internal contradiction, gaining an animal mask as scar tissue. Isabella and Percival were recruited after, don't have full knowledge of the foundation. Oswald's long-term plan: claim the Seat fully with Aurora suppressed. The letter at Table #9 of the Gilded Tusk is about this.

**Aurora** (`mythology/seats.md`, `locations/eclipsera-city.md`)
Bearer of the Seat of Love/Binding. Bound beneath Eclipsera. The city's unity runs on her. The chains are not permanent containment — they are preparation for Oswald's claim.

**Animal titles = scar tissue**
The council's animal symbols (Lion, Panther, Bear, Fox, Owl, Pig, Elephant) are not heraldic. They're the shape the Seat left on each person when the attempt failed.

**Deck-building conventions** (canonical home: `rules/cards.md`, Deck Building)
Player decks: color counts match stats (Mind 4/Body 2/Soul 3 → 4B/2R/3G) — heuristic, not law. Enemy decks: 3 themed signature cards + 4–7 core cards (7–10 total), leaning toward the creature's stat spread. Enemies draw to hand size like players. Opening hands: everyone draws to hand size when initiative is rolled (added to `rules/combat.md`). Worked combat: `rules/combat-example.md` — includes rulings on 4 edge cases, all resolved by Drew. Tie-counts-as-successful-defense is ruled per-card, not universally: WITNESS says so on the card; new cards referencing "successful defense" must carry their own clarifying line until/unless the convention is promoted to a universal rule.

**Card system: signature sets**
Creature combat decks are filled from core cards. Signature cards are Oracle rewards. Drew determines how many land in a given set after reviewing the full 9. The standard loop: draft 9, red team all 9, fix/cut/replace until all pass, present all 9, Drew decides placement.

**HP formula: (2 × Body) + 9** (changed from 3×Body+6 — Drew, via sim experiment)
Flatter curve to decouple HP from Body and reduce Body's damage+HP double-dip. Crossover at Body 3 (both = 15); trims high Body (B4: 18→17, B5: 19, B8: 25) and lifts low Body (B1: 11, B2: 13). Bites harder at high stats, which is where powerful creatures live. Player impact: Frost stays 15, Steele 18→17. **Existing creature stat blocks keep their authored HP** (gm-guide allows GM-set HP); new content + players use the new formula. Sim uses it (`hp_per_body`). NOTE: the sim showed HP is NOT the main lever for Steele's dominance (even flat HP left Steele at 59% vs Frost) — the real driver is red damage + color spread.

**Damage-distribution rebalance (Drew, applied):** Pain is Fuel & Push d6→d4; Stillness & Excavate d2→d4; Attune d2→d4. Narrowed the color-EV gap (RED 2.62→2.53, BLUE 2.15→2.21, GREEN 2.44→2.47) — good for draft diversity / makes blue-green picks more competitive. BUT the sim showed single-card dice tweaks DON'T move deck-level balance: Steele barely budged (66% vs Frost). Reason: damage = stat + die, and a Body-4 stat (+4 flat on every red card) dominates a one-step die change (−1 avg). **The real Steele lever is the stat-to-damage ratio, not card dice** — e.g. capping how much stat adds, or a smaller stat mod + bigger dice. Card dice are the right tool for per-card attractiveness (Oracle draft balance), the wrong tool for reining in a high-stat deck.

**GAME LENGTH is the master balance variable (big finding).** Tested shifting ALL damage dice up/down one size (sim only, not applied): dice DOWN → Steele 66%→56% vs Frost (games longer, 8.6 turns); dice UP → Steele 66%→70% (games faster, 7.0 turns). Monotonic. Bigger dice = faster games = raw-stat power converts to wins more directly (fewer decisive hits, less room for reads/card-play). Smaller dice = longer games = flat stat advantage grinds through more RPS variance and dilutes. This unifies all balance findings: HP-flatten helped a little (slightly longer games), single-card dice nerfs did nothing (too small to change length), a blanket dice-DOWN would help a lot (shortens nothing, lengthens everything). The RPS mind-game, reads, and card advantage all NEED turns to exist; speed kills them and rewards whoever hits hardest. So to dilute stat-max: lengthen games (smaller dice / more HP / cheaper defense), never shorten them. Drew's "shift dice UP" suggestion does the opposite — DON'T. No canon change made yet; direction TBD.

**Full lever sweep (all sim-tested, only HP-flatten applied):** for reining in Steele's ~66% dominance —
- HP decouple 2×Body+9: mild help (~2pts). APPLIED/canon.
- Single-card dice nerfs (5 cards): ~0 effect (too small to change game length).
- Dice UP one size: WORSE (66→70%, faster games).
- Dice DOWN one size: HELPS most (66→56%, longer games) but blunt/drags/feel cost.
- Remove dice entirely (flat damage): slightly WORSE (66→69%) — removes the underdog's variance, and would gut the "d-scale damage dice" core identity. DON'T.
- Stat cap (die + min(stat,N)): ruled out by Drew.
CONCLUSION: the ONLY reliable dilution of stat-max is LENGTHENING games, and within that VARIANCE HELPS THE UNDERDOG (so flat damage / faster games hurt). Best remaining lever = DEFENSE ECONOMY (make blocking more available/effective → longer games, no single hit decisive), which lengthens without shrinking dice or gutting identity. BUT also worth questioning whether it's a problem at all: stat-maxing (Volk) is self-defeating (loses to everyone); Steele's ~66% is modest and comes from GOOD deckbuilding (high primary + viable secondary), which is arguably healthy.

**Balance philosophy (Drew):** red's combat power is INHERENT — don't fight it. Balance via card EFFECTS: green and blue pay for less damage with stronger effects.

**Minmax trifecta added to sim (Latin square, each stat takes 4/3/2 once):** Steele Body4/Mind3/Soul2 (4R/3B/2G, canonical), Sage Mind4/Soul3/Body2 (4B/3G/2R), Adept Soul4/Body3/Mind2 (4G/3R/2B). Round-robin under tactician OVERTURNED the "blue is weakest" premise. Color-archetype ranking: **Blue(Sage) 72% avg > Red(Steele) 62% > neutral(Frost) 41% > Green(Adept) 23%.** Blue is the STRONGEST 1v1 archetype (Axiom+Paradox control + Mind-4 fat hand; crushes Frost 90%). Green is WEAKEST — but structurally: its best effects are ally buffs (dead in a duel). CRITICAL: the 1v1 sim STRUCTURALLY overrates blue (selfish control) and underrates green (team support). Color identities revealed: Red=consistent bruiser, Blue=1v1 controller, Green=team anchor. So DON'T buff blue (already #1) and DON'T buff green's selfish power off 1v1 numbers (would break team play where its support already works). Green balance, like hand-size, is un-evaluable until the team sim. Blue/green EFFECT-buff pass is on hold pending this reframe — awaiting Drew's direction.

**TEAM SIM built (Stage 1)** — `team_engine.py` (Battle: N-v-N, interleaved initiative wheel, target selection, taunt-forced targeting, team win), `team_policies.py` (TeamTactician: focus-fire lowest HP, recency defense), `team_run.py` (runner). Shares the 1v1 card effects: ally effects route through `engine.allies(me)` — empty in 1v1 (behavior UNCHANGED, verified: Steele>Frost still 66.3, Sage>Frost 90.2), populated in teams. Wired a few green ally effects live (Renewal heal, Twin Strike buff, Mockery taunt, Blood Tithe ally-heal). Stage-1 3v3 findings: **hand-size/blocking CONFIRMED** — Sage (Mind4, hand5) went 56%→87% vs Red in teams, because a big hand blocks the extra between-turn attacks. Validates the block-capacity thesis AND the decision to keep the +1. Green did NOT come alive (Adept 21→16% vs Red) BUT that's not trustworthy: only a thin slice of green's support kit is implemented and the naive focus-fire policy can't PILOT support (no proactive heals, buff timing, protective taunts). STAGE 2 needed for a fair green test: implement the full green support kit (Resonate/Support/Conduct/Witness/Shared Burden/Intercept) + a support-aware policy. Team sim under-rates green for the same reason 1v1 did — the AI can't use the cards.

**TEAM SIM Stage 2 (green vindicated):** implemented green's support kit (Resonate all-ally +2/Resist, Support/Conduct buff+draw, Witness heal, Shared Burden damage-redirect tank) + Warden deck (Soul4 green support) + support-aware team policy. Green went from worst-by-far to TEAM ANCHOR: Warden vs Sage(blue) 56% (was Adept 20%!), vs Steele(red) 28% (was 16%). 1v1 unchanged (support cards inert, Sage>Frost 90.5). **BIG FINDING — emergent archetype RPS in team play: Blue(Sage)>Red(Steele) 87%, Red>Green(Warden) 72%, Green>Blue 56% = the exact card RPS wheel (Blue>Red>Green>Blue) reproduced at the deck-archetype level.** Every color has a home and a predator; no color is "best". CONCLUSION on the balance arc: the system is well-balanced ACROSS formats; red's 1v1 damage, blue's 1v1 control, green's team support are context-specialized, not broken. Don't buff/nerf colors off single-format data.

**GREEN SELF-TARGETING buff (Drew, CANONIZED):** Green (Soul) cards count the user among their allies — green's heals/buffs/Resist/draw can target the caster. Rule added to `rules/cards.md` (You Are Not Your Own Ally → "Green counts itself among its allies"). Redirect-to-someone-else effects (Shared Burden) still need a separate target. Effect: gives green-SUPPORT decks a 1v1 floor (Warden went to viable: beats Sage 59%, even w/ Frost 50%, loses only to aggro) while attacker-green (Adept) stays weak — rewards building green AS support. In teams it pushed green's counter to blue 56%→63.5%. Team RPS triangle now clean & decisive: Blue>Red 71%, Red>Green 68%, Green>Blue 63.5% (green>blue is the softest leg; Drew wanted more of a blowout — open whether to push green's anti-control support harder, risking the triangle). Sim implements via `_team(engine,me)=[me]+allies` in green support effects; 1v1 ripple on Steele/Frost negligible (RENEWAL/TWIN STRIKE self-buff minor).

**Why Blue(Sage)>Red(Steele) is 71% in teams (Drew wanted it ~65):** it's NOT a color imbalance and NOT Axiom (Axiom is a TEAM DUD — removing it from Sage made Sage STRONGER, 71→83% vs Steele; its single-target one-reveal ban barely matters in a 6-person fight; Axiom is a 1v1 star only). The real driver is blue's Mind-4 blocking wall + card advantage, which walls MIDRANGE decks. Steele is balanced midrange → feeds the wall. But aggressive red BEATS blue: Volk(Body5, 7-red) vs Sage = Volk 58%. And green sustain beats blue (Warden 63%). So the meta is the classic AGGRO > CONTROL(blue) > MIDRANGE, with green-sustain also beating control. Blue's blocking is coupled to both its legs (can't lower B>R without raising G>B past 65). RECOMMENDATION (given): don't nerf — 71% is control correctly eating midrange; the counter to blue is aggression or sustain, both available. The "clean color triangle" is really a richer archetype metagame. No change made.

**Composable brains + Scry (Drew Q: can you combine brains?):** YES — via a shared sub-brain mixin. Implemented `ScryMixin` in policies.py: every action-brain (tactician/greedy/reader/team) composes with ONE shared scry strategy; any brain can override it for card-specific cleverness. `engine.scry(actor, owner, x)` added to both Duel and Battle (reorder top X of own or enemy deck). Strategy (Drew's): own deck → surface value, bury Wounds; enemy deck → bury their threats + the color that beats your attacks, leave junk/their Wounds on top. Wired to ALIGN (own) + AXIOM defense (enemy). FINDING: scry has ~0 measurable impact (+0.0-0.1% A/B) — SAME structural reason deck-tracking failed: tiny reshuffling decks defeat deck manipulation. Scry's real value is the conditional riders (ALIGN draw/+2) and human information, not the reorder. Composability architecture is the real deliverable. Rulings-log: gap-retaliate & stalemate-cap accepted as final simplifications; scry resolved by implementation.

**Scry keyword extended (Drew): Scry now = Scry + Surveil.** Look at top X, place each on top, bottom, OR into the discard pile. Canonized in `rules/card-glossary.md` + `rules/cards.md`. Engine.scry (both engines) supports the discard bucket. FINDING: binning to discard is combat-NEUTRAL (~0, even a scry-centric 4x-ALIGN deck; slightly negative) — in a small RESHUFFLING deck, binning a card just recycles it faster on the next reshuffle (MTG surveil works b/c no mid-game reshuffle; ours reshuffles). BUT surveil has real value OUTSIDE combat: binning a Wound to discard moves it where a short rest can REMOVE it (rest clears hand/discard, never deck) and where Press the Wound counts it — a Wound-MANAGEMENT tool, not a tempo tool. Sim brain bottoms Wounds (combat-optimal); engine keeps bin capability for the keyword. Through-line of the whole balance arc: deck-STATE strategies (track/scry/bin) are ~neutral in this system's tiny reshuffling decks; tempo/read strategies (recency, blocking, aggro, sustain) move win rates.

**Expanded card set (Drew): +21 cards implemented (~even split, team focus).** Now 55 real cards (19B/18R/18G). New engine hooks: Armour (flat reduction, clears next turn), can't-defend (Interrupt), team Intercept (ally steps in to defend — Battle only), Fortress damage-shield, AoE splash (Chain/Trample), ongoing support ticks (Synchrony team heal, Rooted Oath anchored buff), Patience "did I wait" flag. Cards: R = Strike, Guard, Intercept, Fortress Stance, Rally, Trample, Charge. B = Interrupt, Chain, Calculate, Analyze, Study, Profile, Refract. G = Synchrony, Rooted Oath, Urgency, Delay, Communion, Mirror Step, Patience. All ally effects route through engine.allies/_team (inert in 1v1, live in Battle). Verified: Guard armour, Intercept redirect, Fortress shield all work via forced test; 1v1 unchanged. Two test archetypes added to roster: `vanguard` (Body4 tank/protection) and `tempo` (Mind4 control). FINDING: pure-protection Vanguard is weak (6% vs Steele) even piloted well — protective cards are ROLE-PLAYERS, not deck cores; a deck needs a damage win-condition. Team policy now values protection/tempo/AoE by team need.

**Initiative Shift fully implemented (Drew), with true repositioning:** turn order is now a rotating QUEUE (queue[0]=current actor, rotates to back each turn) in both engines. `_apply_shift(engine,queue,target,amount)` REPOSITIONS the target by `amount` slots — it SETTLES into that new slot (verified: a +3 on the 3rd-in-line moves them to the back after lapping), it is NOT locked into the slot after the shifter. A positive shift that crosses the current marker ALSO grants a bonus turn now (pending_turns, fired right after the current turn); the target then settles at its shifted slot. Negative shift moves the target that many slots LATER (a real per-slot delay, more faithful than a binary skip; also fixes teams where the old `abs//n` gave 0 for |amount|<team-size, so Mockery/Delay did nothing in a 6-wheel). Interrupt/Delay tempo denial now bites in teams. 1v1 unchanged (Sage 88.9, Steele 63.5). Battles terminate (~18-34 turns, no runaway). Minor fidelity gap: after a crossing bonus the target may also act at its resettled slot the same cycle rather than strictly next cycle — negligible (Drew: intended, no fix).

**Predictable implemented (Study def) — blind simultaneity now breakable for one reveal.** `_study_defense` marks the attacker `_predictable_to = caster`; the engines (both) expose that attacker's actual card to the caster on their very next reveal (`defender._known_attack = card`), then the mark expires. Shared policy helper `perfect_read_defense(me)` consumes the peek with certainty: play the exact counter if held → else tie the same color to negate the hit (a tie deals no damage) → else decline and keep cards. Wired into every choose_defense (random/greedy/reader/tactician + team tactician). Only the caster benefits (if an ally Intercepts, the caster isn't defending, so no read; the mark persists until the marked foe attacks the caster). FINDING: value is small and appropriate — ~0.74 dmg prevented per duel on the defender (color-varying attacker vs diverse-hand Seer, 2000-duel A/B). It's a single-reveal defensive rider on a mid card, not a swing; STUDY only marks when it wins a block, and reads only the next reveal. Note: no ROSTER deck currently runs STUDY, so it never surfaces in the standard tournament — the mechanic is proven via forced-STUDY test decks. Was the last documented sim no-op; the sim now models every implemented card's effect. Audited (Drew's request): the exposed card (`_known_attack`) is set immediately before the marked defense choice and cleared immediately after, so it is present on EXACTLY the marked reveals and nowhere else (500-duel audit: read-flag count == PREDICTABLE-fire count, zero leftover after any run) — the early-reveal never leaks into ordinary blind defenses.

**Self initiative-shift — the marker-crossing model (Drew, corrected across TWO passes).** This one crossed the threshold twice; the log keeps both moves because the middle state was itself wrong.
- STATE 0 (original): `_apply_shift`'s current-actor branch (`i == 0`) did `pending_turns.append(target)` on ANY positive amount — so a current actor shifting ITSELF +1 got a bonus turn. Latent, not live (no card self-shifts as the current actor: Interrupt/Urgency's `initiative_shift(me,+3)` run in DEFENSE hooks where `me` is the defender at index >=1). Wrong: a +1 self-shift shouldn't be a free action.
- STATE 1 (my first fix — ALSO wrong, over-corrected): made the `i==0` branch reposition and NEVER cross — clamped so a self-shift could not grant a bonus/skip at all. WHY wrong: Drew clarified the actual model.
- DREW'S MODEL: on your turn you are ON the turn marker. Your first unit of movement takes you OFF the marker but does NOT cross it — "you can't pass it if you're on it, you have to go all the way around first." So the current actor crosses (→ positive: bonus turn; negative: skip) ONLY on a FULL revolution, `|amount| >= total seats`. This differs from a NON-current combatant, who sits some distance `i` AHEAD of the marker and so crosses at `amount >= i`. Same underlying rule ("cross when forward movement reaches the marker"); the actor's forward-distance-to-marker just happens to be a whole lap because it is sitting on it.
- STATE 2 (current, correct): the `i==0` shift is DEFERRED — `_apply_shift` records `engine._pending_self_shift`; the new shared `_rotate_current(engine, queue, who)` applies it at rotation time (when the actor is a normal back-of-wheel combatant, which also dodges the index-0 / run-loop-rotation collision). For `amount>0`: `>= total` → bonus turn + settle a lap back; `< total` → come around `amount` sooner (may land at "acts next" for `amount == total-1`, still NO bonus). For `amount<0`: `>= total` backward → `skip_turns += 1`; smaller → already latest, stays at back, no skip. Verified across sizes: in a 5-wheel +4 = acts next / no bonus, +5 = bonus; -4 = hold / no skip, -5 = skip; monotonic (+ never slower, - never faster). Both run loops now call `_rotate_current` (identical to the old inline rotate when there is no shift; tournaments unchanged, Steele 63.2 / Team B 64.6). Side effect (intended): Delay's DEFENSE on the current attacker now routes through this path — a full-lap `-3` skips in a duel (total 2), merely goes-last in a big team (total 6). Non-current forward-cross bonus turn preserved (regression-checked).

**ARCHITECTURAL NORTH STAR (Drew, via a GPT brainstorm) — rule modifiers, not special cases. LOGGED AS DIRECTION; no refactor yet.** The engine currently implements every rule-bending card as an inline special case in `attack()` (Predictable, Axiom's color-ban, Paradox's RPS inversion, Interrupt's cannot-defend, stagger). Drew's reframe: these are not exceptions to core rules — they are temporary swaps of *which rule set is active*. The invariant is not "card selection is always simultaneous"; it is "card selection follows the CURRENTLY ACTIVE rule set." Default rule set = select simultaneously → reveal simultaneously → resolve RPS. Predictable temporarily installs: target selects → target's card revealed → opponent selects with perfect info → resolve. On expiry the engine reverts. The vision: engine-as-OS with swappable Rule Modules (selection / reveal / initiative / RPS-resolution); cards are temporary patches to the OS itself (explicit MMBN-chip analogy, but chips that edit the engine, not just the battlefield). The engine should stop asking "is Predictable active?" and ask "what are the current reveal and selection rules?" — so new rule-benders compose through one system instead of adding one-off branches.

WHY NOT NOW (my caution, Drew agreed by choosing "log as direction"): building the policy-stack host before the ~5th rule-bender exists means paying full price to host 3 tenants — every core step must be rewritten to consult a stack, and every existing mechanic re-expressed as a modifier or it rots outside the system. The abstraction extracted from 3 real examples will be righter than one designed from 1. AGREED SEQUENCING (promote only when the card list demands the next step): (1) FLAGS — where we are now; each bender is a per-combatant flag (`_predictable_to`, `axiom_ban`, `special_reveal='paradox'`, `cannot_defend`, `staggered`) read inline. (2) TYPED MODIFIERS-WITH-LIFETIMES — cheap next step: a per-combatant (later per-battle) set of active modifiers, each with an explicit lifetime (`on-next-reveal` / `end-of-turn` / `N-turns`), and the four core steps consult it. Gets ~80% of the conceptual win (modifiers become data with a lifecycle, not scattered booleans) without rewriting the resolution core. (3) POLICY STACK — the full engine-as-OS; each core step asks a stack of active policies. Do this only when adding a modifier as a special case has become genuinely painful. The seam already exists (every bender routes through one temporary flag); step 2 just names and types it. Keep MMBN-chip framing as the design north star — but note Drew's correction: "two designers rewriting the duel" implies 1v1, and Tales Untold is TEAM-based. The right image is a whole TABLE rewriting the rules of the fight mid-combat (N players, not a duel).

**Hand-size change (Mind+1 → Mind) — TABLED until team sim exists.** Tested: makes Mind a real stat (a Mind-4 blue deck went 69%→80% vs Steele) but Drew correctly held off. KEY INSIGHT: hand size = BLOCKING CAPACITY between turns, which only matters in TEAM play (multiple enemies attack you before your next turn; each block costs a card). The current +1 is a load-bearing defensive floor (Mind 2 → hand 3 → attack + still 2 blocks; nobody is ever defenseless). Remove it and Mind 2 → 1 block (focus-fired to death) while Mind 4 → 3 blocks (dominant wall). The 1v1 sim STRUCTURALLY CANNOT measure this (only one attacker between turns), so the Sage 80% is the floor of how dominant Mind-4 would be, not the ceiling. → hand-size balance is un-evaluable until the team sim; keep Mind+1 for now. Strong argument for building the team sim next.

**Range definitions**
Quick reference sheet is canonical. Melee: both must be Frontline. Ranged: works only while not in Melee range with target.

**Alignment Marshal — Correction Protocol**
Passive ability on the Marshal stat block: whenever the Marshal takes damage, shuffle 1 Exhaust into the attacker's deck. See `bestiary/alignment-marshal.md`. Cards: `cards/alignment-marshal-engine.md`.

**Aege — the Carrion Guide**
Named NPC at Vulture's Nest. Turnroot native. Gives party the sealed letter hook to Turnroot Weald. Also gives Carrion Feather item on handoff. Refer to her as "the Carrion Guide" in session — Aege is her name. See `locations/vultures-nest.md`.

---

## Workflow Rules

**No new keywords without Drew's approval.**
Current keyword list in `experimental/README.md`.

**Card loop**
1. Draft 9 (3R/3B/3G) in experimental.
2. Red team all 9 against: balance, keyword compliance, creature fidelity, early-game fit, Oracle reward value.
3. Fix what can be fixed. Cut what can't.
4. Generate replacements for any cuts (matching color).
5. Loop until all 9 pass red team.
6. Present all 9 to Drew with your read on which are strongest — Drew decides where they land (signature set, Oracle, archive, etc.).

---

## Content Reference

**Locations**
- `locations/vultures-nest.md` — Session 0/1 hub. Aege, Bartho, Kino, Corvel, Moving Crate. Tideward Compact: Bartho (dockmaster), Jonas (ledger-keeper + Regency informant), Harlow (pirate faction). Condoned smuggling: unsafe magical items, addictive substances, forged papers, stolen cargo, weapons without provenance — anything with a council cut and no Regency visibility. Hard lines: too destructive, too visible, or no cut = quiet final response. Masaharu investigating FourthEye supply chain.
- `locations/roadhouse.md` — Government inn between Vulture's Nest and Briarwatch. Two Regency guards on rotation. Barracks: weapon rack, chest (d6+2 silver, Barbed Wrap, posting order). Posting order → Voss thread.
- `locations/briarwoods.md` — Travel region north of Vulture's Nest. Surrounds Roadhouse and Briarwatch. Day 1 and Day 2 routing. Jackrabbits and Scratchers.
- `locations/briarwatch.md` — Village location, leads into Hollow Below Briarwatch.
- `locations/the-coil.md` — Labyrinth island in the deep lake east of Vulture's Nest. Surfaces on condition only the Night Ferryman knows. Hidden wall-following rule; breaking it raises pressure track and alerts minotaurs. Center: open/TBD. Minotaur stat block pending.

**Creatures**
- `bestiary/briar-scratcher.md` — Mind 1/Body 1/Soul 2, HP 9. Road encounter teaching Wounds as deck pressure. Cards: `cards/briar-scratcher.md`.
- `bestiary/delve-roller.md` — Mind 1/Body 2/Soul 1, HP 12. Rolled Shell passive (−1 all incoming damage). Immune to Blind. Cards: `cards/delve-roller-hollow.md`.

**Quests / Encounters**
- `quests/shifting-burrow.md` — Alternate surface encounter near Briarwatch. Borrower Sentries. Backline movement requires Easy Body check (fail = Exhaust). Cards: BURROW RESHUFFLE, ALERT CALL, DIRT CLOD.
- `quests/hollow-below-briarwatch.md` — References Shifting Burrow as alternate Surface Layer encounter.

**Items**
- `items/briarwoods-items.md` — Barbed Wrap, Carrion Feather, Split Wedge.
- `items/vultures-nest-items.md` — Dockhook Line, Low Lantern, Salted Strip, Dock Broth, Chewfat Ration.
- `items/consumables.md` — Terrormite Capsule, Echo Shell, Blood Phial, Imprint Sigil, Universal Pin, Phase Draught.

**Agent Tools** (`agent-tools/`)
Drop-in prompts for common design tasks. See `agent-tools/README.md` for full index. Always run `repo-orientation.md` first in a new session.

---

## World Context Notes

**Kino** (also "Sawyer") — 15, green eyes, red scarf, real name kept private. At Vulture's Nest, operates with the Red Scarves. In-progress character — behavioral contract only, more detail surfaces as campaign develops.

**Silas** — character passed between multiple AI instances and Drew over time. Nobody can fully claim authorship. That's intentional.

**The Unheld** — don't explain it. Drop hints when they feel right. Some point toward something, some are noise. The distinction between signal and noise is what players are navigating.

**Eclipsera's fog basin** — threshold space that never closes. Pell operates here. Fogcallers are apex negotiators, not simple predators. See `locations/fog-basin.md`.

**Glasslight Reach** — on cliffs above the fog line. Kino can see the basin from home. He chose to go down into it.

**The Island in a Ship** — constants: small island, Oracle at table, cave. Variables: structure mirrors last threshold the party crossed. Session 0 frame: first visit the night of the sailor's story, characters named, decks built. See `locations/island-in-a-ship.md`.

---

## Multi-Agent Notes

Different agents naturally specialize based on which parts of the repo they engage with. Drew is content adjudicator. Don't pre-define agent roles — the environment does that work.

The repo IS the persistent memory. This file captures what the repo can't — mid-session decisions and active threads.

New agents: read `CLAUDE.md` first, then this file. The experimental folder and archives show design process history.
