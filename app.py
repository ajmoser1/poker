from flask import Flask, request, render_template
from poker.cards import Card
from poker.preflop import evaluate_hand
from poker.evaluator import best_score, category

app = Flask(__name__)

@app.route("/")
def hello_world():
    # Returning a dictionary automatically converts it to JSON
    return render_template("index.html")

@app.route("/classify", methods=["POST"])
#A body without a "cards" key raises KeyError, which your except ValueError doesn't catch, so the server returns a 500.
def classify():
    try:
        
        body = request.get_json(silent=True)
        if body is None:
            return {"error": "Request body must be JSON"}, 400
        if "cards" not in body:
            return {"error": "Request body must contain a 'cards' key"}, 400
        cards = body["cards"]
        parsed_cards = [Card.from_str(card) for card in cards]
        if len(parsed_cards) != 2:
            return {"error": "Two cards are required to classify a hand"}, 400
        if parsed_cards[0] == parsed_cards[1]:
            return {"error": "You cannot choose the same card twice"}, 400
        return {"category": evaluate_hand(parsed_cards)}
    except ValueError as e:
        return {"error": str(e)}, 400





@app.route("/evaluate", methods=["POST"])          # Flask: run this function for POST /evaluate
def evaluate():
    body = request.get_json(silent=True)          # Flask: request body as a dict, or None
    if body is None:
        return {"error": "Request body must be JSON"}, 400   # Flask: (dict, status) -> JSON reply
    if "board" not in body or "players" not in body:
        return {"error": "Request body must contain 'board' and 'players' keys"}, 400

    try:
        board = [Card.from_str(c) for c in body["board"]]
        hands = [[Card.from_str(c) for c in hand] for hand in body["players"]]
    except ValueError as e:
        return {"error": str(e)}, 400
    if len(board) not in range(3, 6):
        return {"error": "Board must be between 3 to 5 cards"}, 400
    for card in board:
        if board.count(card) > 1:
            return {"error": "No card may appear twice on the board"}, 400
    for hand in hands:
        if len(hand) != 2:
            return {"error": "Every hand must have exactly 2 cards"}, 400

    for card in hands:
        if hands.count(card) > 1:
            return {"error": "No card may appear twice in a hand"}, 400

    scores = [best_score(hand + board) for hand in hands]
    results = [{"score": score, "category": category(score)} for score in scores]
    top_score = min(scores)
    winners = [i for i, score in enumerate(scores) if score == top_score]
    return {"results": results, "winners": winners}


if __name__ == "__main__":
    app.run(debug=True, port=5001)
