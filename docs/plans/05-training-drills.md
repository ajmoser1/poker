# Plan 05: Training drills (pot odds, equity, bet sizing, position)

**Status: sketch.** Rewrite this plan after plans 02 through 04 exist. The main thing
that will change is what "a scenario" looks like once you have a real game state.

**Goal:** the app presents a spot, asks you a question, and checks your answer using the
simulator. You learn by being wrong and seeing why.

**Depends on:** plan 04 (equity numbers), plan 03 (something to show the spot in). Needs a
**betting engine** that doesn't exist yet: streets, blinds, positions, pot, stacks, legal
actions. That engine is also what plan 06's bot needs, so it's shared infrastructure.

## Concepts you'll need (go learn these, then explain them back to me)

- **Pot odds**: the price you're being offered. Call amount divided by (pot after your
  call). Compare to equity to decide a call.
- **Equity vs. pot odds**: the break-even rule, and why it's only a first approximation
  (implied odds, reverse implied odds, future streets).
- **Bet sizing**: sizing as a fraction of the pot; what a given size "says" about the
  equity the opponent needs to call (the alpha / minimum defense frequency idea).
- **Position**: why acting last is worth money. This one is hard to turn into a numeric
  drill; think about how you'd even measure it.

## Likely shape (revise later)

1. Build the betting engine as a plain state machine first, no UI: `GameState` with
   `legal_actions()` and `apply(action)`. Test it hard. This is the piece most likely to
   hide bugs (side pots, all-ins, min-raise rules). Decide early how much of real NLHE
   rules you want: heads-up only with no side pots is a sane first scope.
2. Drill type 1: "You hold X on board Y, villain bets Z into pot P. Call or fold?" The
   app computes pot odds and your equity vs. a stated villain hand or range and grades you.
3. Drill type 2: "Pick a bet size." Harder to grade; starts as "what equity does villain
   need to call?" arithmetic.
4. Track your answers over time. Simple CSV is enough.

## Open questions to answer before expanding this plan

- Are drills against a *known* villain hand (easy, unrealistic) or a *range* (realistic,
  needs the range extension from plan 04)?
- How much of real NLHE betting rules do you want to implement? Each rule you add is a
  week of edge cases. Write down the subset.
- Do you want the drills to be the main product, or a stepping stone to the bot?

## Reading (when you get here)

- Any introductory explanation of pot odds and implied odds. "The Theory of Poker"
  (Sklansky) chapters on odds, if you want a book.
- "Minimum defense frequency" and "alpha" explainers. These lead directly into the
  game-theory ideas plan 06 needs.
