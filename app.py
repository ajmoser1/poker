from flask import Flask, request
from poker.cards import Card
from poker.preflop import evaluate_hand

app = Flask(__name__)

@app.route("/")
def hello_world():
    # Returning a dictionary automatically converts it to JSON
    return {"hello": "world"}

@app.route("/classify", methods=["POST"])
def classify():
    cards = request.get_json()["cards"]
    return {"category": evaluate_hand([Card.from_str(card) for card in cards])}


if __name__ == "__main__":
    app.run(debug=True, port=5001)
