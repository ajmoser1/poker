# Plan 04: Equity simulator (multiway)

**Goal:** given two or more hole hands (and optionally a partial board), estimate each
hand's equity by dealing out the rest of the board many times and counting wins, ties,
losses.

**Revised 2026-11-01:** multiway from the start, not as a later extension. The table
already seats up to 9 players and `/evaluate` already returns split winners, so a
two-hand simulator would be rewritten almost immediately.

**Depends on:** plan 02 (evaluator). This is also the first real test of the
evaluator's speed.

## The core idea you need to own

**Equity** is the share of the pot a hand expects to win on average. Heads-up that is
`wins + ties/2` divided by trials. With three or more players a tie can be two-way or
three-way, and working out how each counts is step 1. Monte Carlo estimates it by sampling random runouts. The estimate has
error. The standard error of a proportion is roughly `sqrt(p(1-p)/n)`. You should be able
to say how many trials you need for a result good to about one percentage point, and
verify it empirically by running the same matchup several times and looking at the spread.

The alternative to sampling is **exhaustive enumeration**: deal every possible board. For
two preflop hands there are C(48,5) = 1,712,304 boards. That's exact, and feasible, if the
evaluator is fast enough. Postflop the number drops fast: C(45,2) = 990 on the flop.

**UI hook (added 2026-10-31):** the page has a "Keep hero" toggle. With it on, Clear and
auto-deal keep hero's hand and re-deal everything else. That is the hand-vs-random-field
setup this simulator computes, so the equity panel can read hero's kept hand directly.

## Design decisions you make

1. **Sample or enumerate?** Build sampling first (it's the general tool). Add enumeration
   for the turn and river where it's cheap, and compare the two on the same spot to
   validate your sampler.
2. **Dead cards.** The deck you deal from must exclude both players' hole cards and any
   board cards. Where does that logic live: in `Deck`, or in the simulator?
3. **Result type.** Return raw counts or a small result object with win/tie/loss, equity,
   trial count, and standard error? The interface will want all of them.
4. **Randomness and reproducibility.** Accept a seed so a test can be deterministic.
5. **Unknown opponents.** "Hero vs 3 random hands" means the opponents' cards are dealt
   fresh every trial, along with the board. Is that a separate argument (a count of
   random opponents), or does an unknown hand get passed in as something like `None`?

## Steps

1. Write the equity formula and standard error formula at the top of `simulator.py` as a
   comment, in your own words. Include how a three-way split counts.
2. Implement `simulate(hands, board=(), trials=10_000, seed=None)`, where `hands` is a
   list of two or more hands. Then add unknown opponents (decision 5).
3. Sanity tests with known answers (look these up, then confirm your numbers land within
   a few standard errors): AA vs KK is about 82/18. AKs vs 22 is close to a coin flip.
   Same hand vs same hand must be exactly 50/50 under enumeration.
4. Time it. Record trials per second here. If 10,000 trials take more than a couple of
   seconds, revisit plan 02's "where this might change" section. That is the moment to
   learn profiling (`cProfile`) rather than guessing.
5. Enumeration mode for turn and river. Test that enumeration and a large sample agree.
6. Generate the 169x169 preflop equity table (or at least the 169 hands vs. a random
   hand). This is the payoff: it is real data about starting hands. Compare it to your
   plan 01 classifier labels. Where does your hand-written classification disagree with
   the numbers? Rewrite the classifier, or keep it and write down why.
7. Expose it through the interface (plan 03): pick two hands, see equity.

## Done when

- Known matchups reproduce to within sampling error.
- Enumeration and sampling agree on turn/river spots.
- You have a 169-hand equity-vs-random table saved to disk, and a sentence in plan 01
  about what it taught you.

## Learning checkpoints

- Why is a tie worth half a win and not zero?
- If you double the number of trials, by what factor does the error shrink?
- What's the difference between equity and "chance to win"? (Think about multiway pots
  later; for heads-up they coincide only when ties are rare.)
- Why can enumerating all preflop boards be done once and cached, but sampling can't?

## Reading

- Any short explanation of Monte Carlo methods and the law of large numbers.
- Standard error of a proportion (a statistics intro page is enough).
- Python `cProfile` docs, the "instant user's manual" section.

## Where this might change

- **Ranges.** Real poker is hand *range* vs range, not hand vs hand. The natural extension
  is `simulate(range1, range2)` where a range is a set of hand codes with weights. Plan 05
  will want this. Design the hand-vs-hand function so a range version can wrap it.
- **Speed.** If you go to ranges or millions of trials, this is where numpy vectorization
  becomes worth learning. That's an ML-adjacent skill, so it's a good detour when it comes.
