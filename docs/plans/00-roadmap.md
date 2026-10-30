# Roadmap and how we work

This folder holds one plan per feature. Plans are living documents: before starting a
feature, reread its plan, cross out what no longer applies, and rewrite the steps. The
later plans (04, 05) are deliberately sketches. Do not flesh them out until the earlier
features exist, because what you learn building 02 and 03 will change them.

## Feature sequence

| # | Feature | Plan | Status |
|---|---------|------|--------|
| 0 | Deck, dealing, shuffling | [01-foundation](01-foundation.md) | done, tested |
| 1 | Preflop hand classification | [01-foundation](01-foundation.md) | done, tested; step 4 and checkpoints open |
| 2 | River hand-rank evaluator | [02-hand-evaluator](02-hand-evaluator.md) | empty file exists |
| 2a | Minimal UI: see cards, pick actions | [03-interface](03-interface.md) | static mockup exists |
| 3 | Head-to-head equity simulator | [04-equity-simulator](04-equity-simulator.md) | empty file exists |
| 4 | Training drills: odds, sizing, position | [05-training-drills](05-training-drills.md) | sketch only |
| 5 | Pokerbot: blueprint + CFR | [06-pokerbot](06-pokerbot.md) | sketch only |

Dependency shape (arrows mean "needs"):

```
01 foundation  <-  02 evaluator  <-  04 simulator  <-  05 drills  <-  06 bot
                        ^                 ^
                        |                 |
                   03 interface  ---------+   (interface grows alongside, never blocks)
```

## How we work together (the protocol)

1. **You design first.** Before touching code for a step, write three to six sentences:
   what the piece does, what its inputs and outputs are, and the approach you picked. I
   review that, not your code, first.
2. **You implement.** I write code only for scaffolding you already understand (test
   boilerplate, a file layout, a stub), or when you ask for a specific piece and can say
   back what it does.
3. **I review by asking.** When something is wrong I point at it with a question or a
   failing input, not a patch. You find the fix.
4. **Hint ladder when stuck.** Concept first, then pseudocode, then code. You say which
   rung you want.
5. **Learning checkpoints.** Each plan ends with questions you should be able to answer
   without looking anything up. If you can't, that's the signal to go read before moving on.
6. **Reading assignments** are listed per plan. I'll point you to a resource rather than
   summarize it, unless you ask for a summary after reading.

## Conventions to decide once (in plan 01)

- Python package layout and a test runner (pytest).
- One canonical card representation (rank as `T` or `10`, suit as symbol or letter).
- Separation of library code from scripts. Nothing calls `input()` at import time.

## Changelog

- 2026-10-29: initial plans written.
- 2026-10-30: plan 01 steps 1-3 done. `poker/` package created and installed editable;
  pytest and scripts run with no path configuration.
