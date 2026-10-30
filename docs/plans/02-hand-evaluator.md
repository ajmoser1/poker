# Plan 02: River hand evaluator

**Goal:** given 7 cards (2 hole + 5 board), return a value that says what the best 5-card
hand is and that can be compared against another player's value to decide the winner.

**Depends on:** plan 01 (cards, tests).

## The core idea you need to own

A hand's strength must be a *totally ordered* value. Two hands compare by category first
(straight flush > quads > full house > flush > straight > trips > two pair > pair > high
card), then by tiebreak ranks in a category-specific order. A Python tuple like
`(category, tiebreak1, tiebreak2, ...)` compares exactly this way with `<` and `==`. Work
out on paper what the tiebreak tuple is for each category before writing any code.
Examples to get right:

- Two pair: higher pair, lower pair, kicker.
- Full house: trips rank, pair rank. (What if there are two trips in 7 cards?)
- Flush: the five highest cards *of that suit*, not of the hand.
- Straight: only the top card matters. A-2-3-4-5 tops out at 5, not ace.
- Ties are real. Two players can have identical tuples. The pot splits.

## Design decisions you make

1. **Brute force or direct?**
   - Brute force: write a 5-card evaluator, then evaluate all 21 five-card subsets of 7
     cards and take the max. Simple, obviously correct, slow.
   - Direct: count ranks and suits of all 7 cards and derive the best hand without
     enumerating subsets. Faster, more edge cases.
   - Recommendation: brute force first, test it thoroughly, keep it as the oracle. Write
     the direct version later only if plan 04 is too slow. Then test direct against brute
     force on a million random hands.
2. **Where does the ace-low rule live?** Decide whether the straight detector handles it
   specially, or whether you represent ranks so that the ace appears twice.
3. **What does the function return?** A bare tuple, or a small class with a readable name
   ("Full house, kings over fours") plus the tuple for comparison? The interface in plan 03
   needs the name; the simulator in plan 04 needs only the comparison.

## Steps

1. Write the category list and tiebreak scheme in this file as a table. Have me check it.
2. Write tests first, from hand-picked cases. At minimum one per category, plus: wheel
   straight, steel wheel (A-5 straight flush), flush where the hand also has a straight in
   other suits, full house vs full house, two pair with three pairs present in 7 cards,
   kicker decides, exact tie.
3. Implement the 5-card evaluator. Make tests pass.
4. Implement 7-card by iterating `itertools.combinations(cards, 5)`.
5. Add a property-style test: generate random 7-card hands, assert the result's category
   is consistent with simple facts (if 5 cards share a suit, category >= flush, etc.).
6. Optional oracle: install `treys` only inside tests and compare against it on random
   hands. Do not use it in your own code; the point is to build this yourself.
7. Measure speed: how many 7-card evaluations per second? Write the number here. Plan 04
   will tell you whether it's enough.

## Done when

- All category and edge-case tests pass.
- `best_hand(seven_cards)` returns a comparable value plus a human-readable name.
- You can explain to me, without notes, why `(category, *tiebreaks)` tuple comparison is
  sufficient for every category.

## Learning checkpoints

- How many distinct 5-card hands are there? How many distinct *equivalence classes* of
  hand strength? (There are 7,462. Why so few?)
- Why does kicker ordering matter for a flush but not for quads with the same rank?
- What is the complexity of brute force per 7-card hand, in evaluations?

## Reading

- Wikipedia: "List of poker hands" for the exact tiebreak rules.
- Cactus Kev's poker hand evaluator writeup (just read it; don't implement it). It
  explains the 7,462 classes and why lookup tables exist.
- `itertools.combinations` docs.

## Where this might change

- If plan 04 needs millions of evaluations per run, this evaluator becomes the bottleneck.
  The upgrade path is: direct 7-card method, then integer card encoding with bitmasks,
  then precomputed lookup tables. Each is a separate learning unit. Don't start there.
