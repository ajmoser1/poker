# Plan 06: Elementary pokerbot (blueprint strategy + CFR)

**Status: sketch.** Deliberately thin. Everything here is a direction, not a step list.
Rewrite it when you reach it; by then you'll know what you actually want.

**Goal:** a bot with (a) a hand-written strategy blueprint you can play against, and (b)
a learning mechanism, probably Counterfactual Regret Minimization (CFR), that finds a
strategy on its own in a simplified game.

**Depends on:** the betting engine from plan 05, the evaluator, the simulator (for
abstraction and evaluation).

## Two separate things, and the order matters

1. **Blueprint bot.** A rule-based policy: preflop ranges by position, postflop rules
   using equity thresholds from your simulator. You write the rules; this is applied poker
   theory, not ML. Useful as a baseline opponent and a sanity check for everything else.
2. **Learning bot.** CFR is the standard. But CFR on full Hold'em is a research project
   (that's what Libratus and Pluribus did, with abstraction and massive compute). The
   standard learning path, which you should follow, is:
   - **Kuhn poker** (3 cards, one betting round). CFR converges in seconds. You will
     *understand* regret matching here or nowhere.
   - **Leduc Hold'em** (6 cards, two rounds, a community card). Small enough to solve,
     big enough to need information sets done properly.
   - **A tiny Hold'em** of your own design: preflop only, or fixed bet sizes, with hands
     bucketed by equity. This is where your simulator and abstraction ideas meet CFR.

## Concepts you'll need (large; each is its own study unit)

- Extensive-form games, information sets, Nash equilibrium, and why "exploitability" is
  how you score a strategy.
- Regret matching, then CFR, then variants (CFR+, Monte Carlo CFR). Don't start with
  variants.
- Abstraction: card bucketing (by equity or by equity distribution) and action
  abstraction (limited bet sizes). This is what makes Hold'em tractable.
- Evaluating a bot: exploitability (exact, for small games), or head-to-head winrate
  against the blueprint and against your own play (noisy, needs many hands; your
  simulator's variance math applies again).

## Open questions (answer these before writing any plan steps)

- Do you want to *solve* a small game (CFR, exact) or *train* a policy (RL, approximate)?
  These are different fields. CFR is the poker-native choice; RL is the more general ML
  skill. You could do Kuhn with both and compare.
- What game is the bot for: heads-up only? Fixed stack sizes? Those choices shrink the
  problem enormously.
- Does the bot need to run inside the interface in real time, or is it offline analysis?

## Reading (when you get here, in this order)

1. Neller & Lanctot, "An Introduction to Counterfactual Regret Minimization" (2013).
   Implement Kuhn poker from it before reading anything else.
2. Zinkevich et al., "Regret Minimization in Games with Incomplete Information" (2007),
   the original CFR paper. Read after you have working Kuhn code.
3. Brown & Sandholm, the Libratus (2018) and Pluribus (2019) papers, for the abstraction
   and real-time search ideas. Read for understanding, not to implement.
4. Optional: Sutton & Barto "Reinforcement Learning: An Introduction" if you go the RL route.

## What this plan will probably become

Once you've done Kuhn and Leduc, this plan splits into two or three smaller plans:
"abstraction", "CFR on tiny hold'em", and "bot evaluation harness". Don't write those now.
