# Plan 03: Minimal interface (view cards, select actions)

**Goal:** a thin screen that shows cards as text and lets a player pick an action. It
must call your Python code rather than reimplement it.

**Depends on:** plan 01. Benefits from plan 02 (show the hand name).

## Visual direction (decided 2026-10-31)

Raw terminal / dev-log minimalism, modeled on pokerbot.sequoiacap.com, the site that
inspired this project. Tokens and base components are in `styles.css`.

- One monospace font (Source Code Pro), small sizes, uppercase labels.
- Ink on paper, light and dark. Color only carries meaning: red suits and losses, green
  wins, amber close calls.
- Text is the interface: `[FOLD]` `[CALL]` bracket buttons, `=====` dividers, stats as
  `LABEL: value` lines.
- Cards are text in a thin box (`A♠`), not images. The SVG deck in `cards/` is no
  longer needed for the UI.
- 1px solid borders, square corners, no shadows, no gradients.

When a screen feels cluttered, the fix is to remove something, not restyle it.

## Page structure (decided 2026-10-31)

One page. A shared **table** at the top, then stacked feature panels that read from it.

```
POKER LAB
========================================
[+ OPPONENT] [- OPPONENT] [DEAL HANDS] [DEAL BOARD] [CLEAR] [SHOW CARDS] [LIVE EVAL: ON]
NEXT CARD → BOARD 1 · OPPONENTS: 2 · CARDS IN USE: 11/52
----------------------------------------
BOARD      2♣ 8♥ 5♥ 5♠ Q♦   RIVER
----------------------------------------
HERO       A♠ Q♥   TWO PAIR #2787 WINS
VILLAIN 1  A♣ K♣   ONE PAIR #5306
----------------------------------------
card picker (hidden until opened): 52 text cards, 4 x 13, used cards greyed out
========================================
A. EQUITY    every player vs the field          /equity     (plan 04)
B. DRILLS                                                   (plan 05)
C. BOT                                                      (plan 06)
```

Update: the table is now an oval modeled on Sequoia's Exhibit A. The board sits in the
center; seats are spaced evenly on an ellipse, hero at bottom center, opponents clockwise.
Hands display high card first; a pocket pair keeps its dealt suit order.

Each seat shows the preflop class (`/classify`) until the flop, then the live
evaluation (`/evaluate`) replaces it on every street. Live eval off means preflop class
until the river. Buttons sit above the table so they don't move as players are added.

- Board on its own line, above the players.
- Opponents can be added and removed. This makes the table multiway, which plan 04's
  equity has to handle (ties split among several players).
- Random deal fills the empty slots without touching cards already placed.
- Cards travel as two-letter strings (`"Ah"`) between page and server; only display code
  turns them into symbols.
- Assumption: card picker is a clickable grid, not dropdowns. Change here if not.

Build order: table display, card picker, random deal and opponents, then rewire the
preflop panel to read from the table, then the river panel.

**Status 2026-11-01: done.** Front end by Claude (HTML/CSS/JS); Python by the user.
Oval table, picker, deal hands, deal board by street, 1 to 8 opponents, clear, keep hero,
live eval on every street, winner line, auto-deal at 1x/2x/4x/16x. `/classify` and
`/evaluate` built and tested. Two steps changed on purpose:

- Step 4 (SVG card images) dropped. Cards are text, per the visual direction.
- Step 5 (action bar) moved to plan 05. Recording actions means nothing without a betting
  engine, so it gets built with one.

## `/evaluate` contract (the page already sends and expects this)

Request:
```json
{"board": ["Qc", "3h", "Qh", "2c", "Kc"],
 "players": [["As", "Kd"], ["Qs", "2h"], ["5s", "7d"]]}
```

Response 200:
```json
{"results": [{"score": 2468, "category": "Two Pair"}, ...],
 "winners": [1]}
```

- `results[k]` lines up with `players[k]`.
- `winners` holds every index tied for the best score. More than one index means a split.
- Lower score wins. That rule lives here on the server, not in the page.
- Bad input returns 400 with `{"error": "..."}`, same as `/classify`: board not exactly 5,
  a player without exactly 2, unparseable cards.
- Known gap, accepted 2026-10-31: `/evaluate` trusts the page to send no duplicate cards
  across the table and at least one player. The page guarantees both. A hand-made request
  (curl) can still get a wrong answer or a 500. Revisit if anything other than this page
  starts calling the server (the simulator, the bot).

## The design decision that matters most

The current `ui.html` contains a JavaScript copy of the preflop classifier. That's the
trap to avoid: two implementations of every rule. Pick one of these and write your choice
here:

- **A. Python serves the UI.** A tiny web server (Flask or FastAPI) exposes JSON endpoints
  like `POST /classify` and `POST /evaluate`. The HTML page calls them with `fetch`. All
  poker logic stays in Python. This is the path the hint text in `ui.html` already suggests.
- **B. Terminal only for now.** A text interface, no browser. Fastest to build, no new
  concepts, but you'll redo it later.
- **C. Python-rendered pages.** Server returns full HTML per request (Flask templates). No
  JavaScript to speak of.

Recommendation: A, kept deliberately small. It teaches HTTP/JSON, which you'll need for
anything that shows simulation results later. But B is a fine choice if you want to get
to the simulator sooner.

## Concepts to understand before building (option A)

- What a request/response cycle is. What JSON is and how Python dicts map to it.
- Why the server must validate input (two identical cards, bad rank strings) even though
  the page also checks. One sentence: never trust the client.
- Separation: the server knows nothing about pixels, the page knows nothing about poker rules.

## Steps (option A)

1. Install Flask (or FastAPI). Write the smallest possible server with one endpoint that
   returns `{"hello": "world"}`. Open it in a browser. That's the whole first step.
2. Add `POST /classify` that takes two cards as strings and returns the label and hand
   code from `poker.preflop`. Test it with `curl` before touching HTML.
3. Rewrite `ui.html`: delete the JS classifier, replace the submit handler with a `fetch`
   to the endpoint. Move the CSS into `styles.css` (currently empty).
4. Render cards as images from `cards/SVG-cards-1.3/`. Write one function
   `cardImagePath(card)` on the JS side, or have the server return the filename. Decide
   which and why.
5. Add an action bar: fold / check / call / bet with an amount. For now it only needs to
   *record* the action and echo it back. The real betting engine comes with plan 05.
6. When plan 02 lands: `POST /evaluate` with 7 cards returns the hand name. Show it.

## Done when

- Zero poker logic in JavaScript.
- You can deal a random hand in the browser and see the SVG cards and the classification.
- An action click produces a JSON message the server receives.

## Learning checkpoints

- What is the difference between GET and POST, and why is `/classify` a POST?
- What happens if you send the same card twice? Where is it rejected, and why there?

## Reading

- Flask quickstart, up through "Routing" and "About responses". Or FastAPI "First steps".
- MDN: "Using the Fetch API", the first example only.

## Where this might change

- If you want live-updating simulation results (plan 04), you may want a small front-end
  framework or server-sent events. Don't decide now.
- If the bot (plan 06) needs a full game loop, the "action bar" becomes a real client of a
  game-state engine. Keep the action messages simple JSON so that's a small change.
