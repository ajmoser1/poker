# Plan 02: River hand evaluator

**Goal:** given 7 cards (2 hole + 5 board), return a value that says what the best 5-card
hand is and that can be compared against another player's value to decide the winner.

**Depends on:** plan 01 (cards, tests).

**Revised 2026-10-31.** Decision: adopt Paul Senzee's perfect-hash variant of Cactus Kev's
5-card evaluator (`poker/evaluator.c`) instead of writing one. The learning goal shifts
from "design a comparable hand value" to "understand an existing evaluator well enough to
integrate it and verify it." The test list below is unchanged; that suite is how you earn
trust in code you didn't write.

## What the adopted code does and doesn't do

- 5-card only. Returns an int 1..7462. 1 is a royal flush, 7462 is 7-5-4-3-2 offsuit.
  Lower is better. 7462 is the number of distinct hand-strength classes; the same number
  from the original plan's checkpoint.
- Expects cards as 32-bit ints in Cactus Kev's layout:
  ```
  +--------+--------+--------+--------+
  |xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
  +--------+--------+--------+--------+
  b = one bit set per rank (bit 0 = deuce .. bit 12 = ace), used for flush/straight lookup
  cdhs = one bit set for the suit
  r = rank number 0..12
  p = prime for the rank (2,3,5,7,11,13,17,19,23,29,31,37,41)
  ```
  The product of the five primes identifies the five ranks regardless of order. That
  product is what the hash looks up.
- As committed, the file is incomplete: it declares `flushes[]` and `unique5[]` but doesn't
  define them. They come from Cactus Kev's `arrays.h`. The file won't link until they're
  added.
- No 7-card function. That's the 21-subset loop, still to be written.
- No category or name. 1..7462 has to be decoded into "full house" etc. Kev's `hand_rank()`
  gives the thresholds.

## Design decisions you make

1. **How Python calls it.** Options: (a) `ctypes` against a compiled shared library, with
   `eval_7hand` added in C so a 7-card hand is one call; (b) port the algorithm and tables
   to Python, no build step; (c) a real C extension, not yet. Record the choice here with
   one sentence of reasoning.
   **Decided 2026-10-31: ctypes.** Measured on this machine: 2.5M five-card calls/sec,
   120k seven-card hands/sec with the 21-subset loop in Python. Enough for plan 04
   sampling; too slow for full preflop enumeration tables. Upgrade path if needed:
   `eval_7hand` in C so one call covers a hand.
   **Done 2026-10-31:** `eval_7hand` added in C using a fixed table of the 21 five-of-seven
   index combinations. Measured: Python loop 92k hands/sec, single C call 687k hands/sec.
   The old Python loop lives on in the tests as `_score7_reference`, the answer key.

## Status: complete (2026-10-31)

- Encoder, 7-card scoring in C, category decoding, and `best_hand()` all work.
- Key test: every one of the 2,598,960 five-card hands is scored; category counts match
  the known totals and every score 1..7462 appears. Runs in about 1.5 seconds.
- Category bounds were derived by hand: 10, 156, 156, 1277, 10, 858, 858, 2860, 1277.
- Checkpoints answered: 7,462 classes, prime products (unique factorization), flush check
  first for correctness, cost is the Python-to-C crossing.
- Not done, deliberately: readable hand names ("Kings full of Fours"). Add when the
  interface needs them.
2. **Where the card encoding lives.** A method on `Card`, or a function in `evaluator.py`?
   The encoder is evaluator-specific; `Card` shouldn't know about Cactus Kev.
3. **What `best_hand()` returns.** The raw int is enough for the simulator. The interface
   wants a name. Decide on a small result object or a tuple.
4. **Build and distribution** (option a only). Where the compiled library goes, how it gets
   built, and that build artifacts are ignored by git.

## Steps

1. Read Cactus Kev's evaluator writeup, then Senzee's page on the perfect hash. Required.
   Before continuing you should be able to explain: the card bit layout, why primes are
   used, why flushes and straights get separate lookups, and what 7462 counts.
2. Obtain `flushes[]` and `unique5[]` from Kev's `arrays.h`. Confirm the C file compiles
   and links. Keep the attribution header.
3. Write `encode(card) -> int` in Python. Test it with hand-computed values for three or
   four cards: work the bits out on paper first, then assert.
4. Decide and implement the binding (decision 1). Smoke test: encode a known royal flush,
   evaluate it, expect 1.
5. Write 7-card evaluation (21 subsets, take the min). Test it with the same case list as
   the original plan: one per category, wheel, steel wheel (A-5 straight flush), flush
   where other suits form a straight, full house vs full house, two trips in 7 cards,
   three pairs in 7 cards, kicker decides, exact tie.
6. Decode 1..7462 into category and a readable name. Test the boundaries: the worst
   straight flush and the best quads must land in different categories.
7. Property test: random 7-card hands, assert category is consistent with simple facts
   (five of a suit present implies at least a flush, etc.).
8. Measure speed: 7-card evaluations per second. Write the number here. Plan 04 decides
   whether it's enough.

## Done when

- The C file links, or the port passes the same tests.
- All category, edge-case, and boundary tests pass.
- `best_hand(seven_cards)` returns a comparable value plus a readable name.
- You can explain, without notes, how a 5-card hand becomes an int and why the int order
  is a valid strength order.

## Learning checkpoints

- Why are there exactly 7,462 distinct hand strengths when there are 2,598,960 five-card
  hands? What does the evaluator throw away?
- Why can a product of primes stand in for an unordered set of ranks, and why would a sum
  not work?
- Why does the flush check come first in `eval_5hand_fast`, before the straight check?
- What is the cost of calling a C function from Python, and when does it dominate?

## Reading

- Cactus Kev's Poker Hand Evaluator writeup (the original). Required.
- Paul Senzee's page on the perfect-hash variant. Short.
- Python `ctypes` tutorial, first half, if you pick option (a).
- Optional, for perspective: the Two Plus Two evaluator thread, which goes further with a
  7-card lookup table. Read for understanding, not to adopt.

## Where this might change

- If plan 04 enumeration (1.7M boards, 21 subsets each) is too slow through ctypes, the
  upgrade path is to move more of the loop into C, or to switch to a direct 7-card table.
  Each is a separate unit of work; measure first.
- If you later want numpy-vectorized evaluation for range-vs-range work, the Python port
  (option b) becomes the better base. Keep the encoding and decoding in Python regardless,
  so that switch is cheap.
