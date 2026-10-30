# Plan 03: Minimal interface (view cards, select actions)

**Goal:** a thin screen that shows cards using the SVG assets in `cards/` and lets a
player pick an action. It must call your Python code rather than reimplement it.

**Depends on:** plan 01. Benefits from plan 02 (show the hand name).

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
