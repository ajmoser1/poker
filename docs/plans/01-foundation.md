# Plan 01: Foundation (deck, cards, preflop classifier, project hygiene)

**Goal:** turn the current scripts into a small library that every later feature imports,
with tests, so you can change things without fear.

**Depends on:** nothing.

## What exists now

- `deck.py`: `Card` and `Deck`. Works. `Card` has no equality or hashing, so the rest of
  the code compares `(rank, suit)` tuples by hand.
- `handEval.py`: preflop classifier. Also the interactive script. The two are tangled: the
  whole file runs `input()` prompts at import time, so nothing else can import
  `evaluate_hand` without triggering the prompts.
- `ui.html`: a static page that reimplements the classifier in JavaScript. Two copies of
  the same logic will drift.

## Things to find and fix yourself (don't just take my word)

Each of these is a real problem in the code. Go find it and decide what to do.

1. ~~There are two different spellings of the ten. One module uses `'10'`, one uses `'T'`
   with an alias. Pick one canonical representation for the whole project and write it
   down in this file.~~
2. ~~There is an unused import at the top of `handEval.py` that pulls in a heavy library.~~
3. ~~Try `python -c "import handEval"` and watch what happens. Learn what
   `if __name__ == "__main__":` is for, then split the file.~~
4. ~~`Card` instances can't be compared with `==` or put in a `set`. Read about
   `@dataclass(frozen=True)` and decide whether that's the right tool. Ask yourself: should
   a card be mutable at all?~~
5. ~~`Card.value` maps ace to 14. Think ahead to the evaluator: in the straight A-2-3-4-5 the
   ace counts as 1. Where should that knowledge live? (Answer in plan 02, but notice it now.)~~
6. ~~`__pycache__` is checked into git. Add a `.gitignore`.~~

## Steps

1. Create a package. A reasonable layout, but you choose:
   ```
   poker/            # package
     cards.py        # Card, Deck, rank/suit constants
     preflop.py      # classify(hand) -> str, hand code like "AKs"
     evaluator.py    # plan 02
     simulator.py    # plan 04
   scripts/
     classify_cli.py # the interactive part of today's handEval.py
   tests/
     test_cards.py
     test_preflop.py
   ```
   **Done 2026-10-30.** Layout above is what exists. The package is installed into `.venv`
   in editable mode via `pip install -e ".[dev]"`, so `import poker.cards` works from any
   directory without path tricks. Rerun that command only if `pyproject.toml` changes.
2. ~~Install pytest and write the first test before moving code: deck has 52 unique cards,
   dealing reduces the deck, shuffling keeps the same set. Then move code and keep tests green.~~
   Done. Tests check uniqueness via `set`, snapshot-then-compare for shuffle, and that a
   dealt card leaves the deck.
3. ~~Write tests for the preflop classifier that pin down current behavior: `AA` is a
   premium pair, `A5s` is a suited ace, `72o` is trash. Then look at the matrix in
   `handEval.py` (the 13x13 grid). It's built but never used. Decide: is the classifier a
   function of the hand code string, so you could classify all 169 codes once and look them up?~~
   Done. The unused matrix was deleted. Classifier labels were simplified while writing
   tests: "Strong Hand" and "Medium Pair" are gone, TT and 99 are plain "Pair", and AQ,
   AJs, KQs moved into "Premium Broadway". Reason for the change still to be written here
   (step 4).
4. Decide what the classifier is *for*. Right now it returns a label. Plan 04 will produce
   real equity numbers for all 169 starting hands. When that exists, your hand-written
   labels become something you can check against data. Leave a note here about what you'd
   want to compare.

## Done when

- [x] `pytest` passes and covers deck and classifier. (10 tests)
- [x] `import poker` runs no interactive code.
- [ ] One card representation everywhere, documented at the top of `cards.py`. Ranks are
      `'2'`..`'9'`, `'T'`, `'J'`, `'Q'`, `'K'`, `'A'`; suits are the symbols `♠ ♥ ♦ ♣`.
      That is the convention in use, but it isn't written in `cards.py` yet.
- [x] The classifier is importable by the evaluator, simulator, and interface.
- [ ] Learning checkpoints answered (see below). Two of three need a second pass.

## Open before closing this plan

- Write the card representation note at the top of `poker/cards.py`.
- Step 4: one sentence on why the labels were simplified and what you'd compare against
  equity data.
- Checkpoints: Fisher-Yates answer described the biased variant; module-vs-script answer
  should name `__name__`.

## Learning checkpoints

- Why should a `Card` be immutable and hashable? What breaks if it isn't?
- What does `random.shuffle` do under the hood, and is it unbiased? (Look up Fisher-Yates.)
- What's the difference between a module and a script in Python?

## Reading

- Python docs: `dataclasses`, `__eq__`/`__hash__` contract.
- pytest "Getting started" page. Just the first page.
- Fisher-Yates shuffle (Wikipedia is fine). Note the common buggy variant.

## Where this might change

- If you switch to a web backend in plan 03, the package layout may gain an `api/` folder.
- If plan 04 needs speed, cards may become integers instead of objects. Don't do that now;
  do note which code would need to change.
