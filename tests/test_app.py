from app import app

client = app.test_client()

MISSING_CARDS = {"error": "Request body must contain a 'cards' key"}


def classify(body=None):
    """POST to /classify. With no body, send nothing at all."""
    if body is None:
        return client.post("/classify")
    return client.post("/classify", json=body)


# --- valid input --------------------------------------------------------------------

def test_classify_valid_hand():
    response = client.post("/classify", json={"cards": ["Ah", "Kd"]})
    assert response.status_code == 200
    assert response.get_json() == {"category": "Premium Broadway"}


def test_classify_card_order_does_not_matter():
    first = classify({"cards": ["Ah", "Kd"]}).get_json()
    second = classify({"cards": ["Kd", "Ah"]}).get_json()
    assert first == second


# --- bad cards ----------------------------------------------------------------------

def test_classify_invalid_hand():
    response = client.post("/classify", json={"cards": ["Ah", "Ah"]})
    assert response.status_code == 400
    assert response.get_json() == {"error": "You cannot choose the same card twice"}


def test_classify_duplicate_hidden_by_whitespace():
    response = classify({"cards": ["Ah", "Ah "]})
    assert response.status_code == 400


def test_classify_invalid_rank():
    response = classify({"cards": ["Zz", "Kd"]})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid rank: Z"}


def test_classify_invalid_suit():
    response = classify({"cards": ["Ax", "Kd"]})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid suit: x"}


def test_classify_card_string_too_long():
    response = classify({"cards": ["Ahxyz", "Kd"]})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid card: Ahxyz"}


# --- wrong number of cards ----------------------------------------------------------

def test_classify_one_card():
    response = classify({"cards": ["Ah"]})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Two cards are required to classify a hand"}


def test_classify_three_cards():
    response = classify({"cards": ["Ah", "Kd", "Qs"]})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Two cards are required to classify a hand"}


# --- malformed request --------------------------------------------------------------

def test_classify_invalid_request():
    response = client.post("/classify")
    assert response.status_code == 400
    assert response.get_json() == {"error": "Request body must be JSON"}


def test_classify_missing_cards_key():
    response = classify({"hand": ["Ah", "Kd"]})
    assert response.status_code == 400
    assert response.get_json() == MISSING_CARDS


def test_classify_rejects_get():
    response = client.get("/classify")
    assert response.status_code == 405


# ===================================================================================
# /evaluate
# ===================================================================================

def evaluate(board, players):
    return client.post("/evaluate", json={"board": board, "players": players})


# --- winners ------------------------------------------------------------------------

def test_evaluate_single_winner():
    response = evaluate(["Qc", "3h", "Qh", "2c", "Kc"], [["As", "Kd"], ["Qs", "2h"], ["5s", "7d"]])
    assert response.status_code == 200
    data = response.get_json()
    assert [r["category"] for r in data["results"]] == ["Two Pair", "Full House", "Pair"]
    assert data["winners"] == [1]


def test_evaluate_results_line_up_with_players():
    response = evaluate(["2c", "7d", "9h", "Js", "Kc"], [["As", "Ad"], ["3s", "4d"]])
    data = response.get_json()
    assert len(data["results"]) == 2
    assert data["results"][0]["category"] == "Pair"
    assert data["results"][1]["category"] == "High Card"
    assert data["winners"] == [0]


def test_evaluate_lower_score_wins():
    data = evaluate(["Ac", "Kd", "7h", "4s", "2c"], [["Ah", "3d"], ["As", "Qd"]]).get_json()
    scores = [r["score"] for r in data["results"]]
    assert data["winners"] == [scores.index(min(scores))]


def test_evaluate_board_plays_is_a_split():
    # Broadway straight on the board; neither hand improves it.
    response = evaluate(["Ac", "Kh", "Qd", "Jc", "Tc"], [["2s", "3d"], ["4s", "5h"]])
    data = response.get_json()
    assert data["winners"] == [0, 1]
    assert data["results"][0]["score"] == data["results"][1]["score"]


def test_evaluate_three_way_split():
    response = evaluate(["Ac", "Kh", "Qd", "Jc", "Tc"], [["2s", "3d"], ["4s", "5h"], ["6s", "7h"]])
    assert response.get_json()["winners"] == [0, 1, 2]


def test_evaluate_kicker_breaks_tie():
    # Both have a pair of aces; the king kicker beats the queen kicker.
    response = evaluate(["Ac", "8d", "6h", "4s", "2c"], [["Ah", "Kd"], ["As", "Qd"]])
    assert response.get_json()["winners"] == [0]


def test_evaluate_single_player():
    response = evaluate(["Ac", "8d", "6h", "4s", "2c"], [["Ah", "Kd"]])
    assert response.status_code == 200
    assert response.get_json()["winners"] == [0]


# --- bad input ----------------------------------------------------------------------

def test_evaluate_requires_json():
    response = client.post("/evaluate")
    assert response.status_code == 400
    assert response.get_json() == {"error": "Request body must be JSON"}


def test_evaluate_requires_board_and_players():
    response = client.post("/evaluate", json={"board": ["Ac", "8d", "6h", "4s", "2c"]})
    assert response.status_code == 400


BOARD_SIZE_ERROR = {"error": "Board must be between 3 to 5 cards"}


def test_evaluate_board_too_short():
    response = evaluate(["Ac", "8d"], [["Ah", "Kd"], ["As", "Qd"]])
    assert response.status_code == 400
    assert response.get_json() == BOARD_SIZE_ERROR


def test_evaluate_board_too_long():
    response = evaluate(["Ac", "8d", "6h", "4s", "2c", "9h"], [["Ah", "Kd"]])
    assert response.status_code == 400
    assert response.get_json() == BOARD_SIZE_ERROR


def test_evaluate_flop():
    data = evaluate(["Qc", "3h", "Qh"], [["As", "Kd"], ["Qs", "2h"]]).get_json()
    assert [r["category"] for r in data["results"]] == ["Pair", "Three of a Kind"]
    assert data["winners"] == [1]


def test_evaluate_turn():
    data = evaluate(["Qc", "3h", "Qh", "2c"], [["As", "Kd"], ["Qs", "2h"]]).get_json()
    assert [r["category"] for r in data["results"]] == ["Pair", "Full House"]
    assert data["winners"] == [1]


def test_evaluate_leader_can_change_by_street():
    # Flop: aces ahead of a flush draw. River: the fourth heart arrives.
    hands = [["As", "Ad"], ["Kh", "Qh"]]
    flop = evaluate(["2h", "7h", "9c"], hands).get_json()
    river = evaluate(["2h", "7h", "9c", "4s", "Th"], hands).get_json()
    assert flop["winners"] == [0]
    assert river["winners"] == [1]
    assert river["results"][1]["category"] == "Flush"


def test_evaluate_hand_with_one_card():
    response = evaluate(["Ac", "8d", "6h", "4s", "2c"], [["Ah"], ["As", "Qd"]])
    assert response.status_code == 400
    assert response.get_json() == {"error": "Every hand must have exactly 2 cards"}


def test_evaluate_invalid_card():
    response = evaluate(["Ac", "8d", "6h", "4s", "Zz"], [["Ah", "Kd"]])
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid rank: Z"}


def test_evaluate_duplicate_on_board():
    response = evaluate(["Ac", "Ac", "6h", "4s", "2c"], [["Ah", "Kd"]])
    assert response.status_code == 400


def test_evaluate_rejects_get():
    assert client.get("/evaluate").status_code == 405
