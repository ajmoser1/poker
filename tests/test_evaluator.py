"""Tests for poker.evaluator.

Fill in the cases from plan 02, step 5. The three below are the smoke test already run
by hand against the compiled library; they pin the tables and the encoder.
"""
import pytest
from poker.cards import Card, Deck
from poker.evaluator import best_hand, best_score, category, encode, score5, score7
from itertools import combinations


def _cards(spec: str):
    """Build Cards from a string like 'As Kh Td'. Suits: s h d c."""
    return [Card.from_str(card) for card in spec.split()]


def test_royal_flush_scores_1():
    royal = _cards("As Ks Qs Js Ts")
    encoded_royal = [encode(card) for card in royal]
    assert score5(encoded_royal) == 1

def test_royal_flush_scores_2():
    royal = _cards("Ah Kh Qh Jh Th 8s 5c")
    assert score7(royal) == 1

def test_worst_hand_scores_7462():
    worst = tuple(encode(c) for c in _cards("7s 5h 4d 3c 2s"))
    assert score5(worst) == 7462


def test_wheel_is_the_weakest_straight():
    wheel = tuple(encode(c) for c in _cards("As 2h 3d 4c 5s"))
    assert score5(wheel) == 1609

def test_score7_finds_scattered_hand():
    scattered = _cards("Ah 8s Kh Qh 5c Jh Th")
    assert score7(scattered) == 1

def test_best_hand_full_house():
    result = best_hand(_cards("Kh Kd Ks 4c 4h 9s 2d"))
    assert result.category == "Full House"

def test_two_three_of_a_kinds():
    result = best_hand(_cards("Kh Kd Ks 4c 4h 4s 9d"))
    assert result.score == best_hand(_cards("Kh Kd Ks 4c 4h 2d 3c")).score

def _score7_reference(cards):
    encoded_cards = [encode(card) for card in cards]
    return min(score5(combo) for combo in combinations(encoded_cards, 5))

def test_score7_matches_score7_reference():
    for i in range(10000):
        deck = Deck()
        deck.shuffle()
        cards = [deck.deal() for _ in range(7)]
        assert score7(cards) == _score7_reference(cards)

def test_score7_rejects_two_cards():
    with pytest.raises(ValueError):
        score7(_cards("Ah Kd"))


# --- Encoder ------------------------------------------------------------------------
# three or four cards whose integer you computed on paper. For example, what is
# the king of diamonds? Work the bits out, then assert encode(...) == that number.
def test_king_of_diamonds():
    king_of_diamonds = encode(Card.from_str("Kd"))
    assert king_of_diamonds == 0b00001000000000000100101100100101


# --- Seven-card and categories -------------------------------------------------------
# TODO (plan 02 step 5): one per category, steel wheel, flush beaten by nothing else in
# hand, full house vs full house, two trips, three pairs, kicker decides, exact tie.

def test_all_hands_and_category_boundaries():
    deck = Deck()
    
    categories_and_hands = {"Royal Flush": 0, "Straight Flush": 0, "Four of a Kind": 0, 
                            "Full House": 0, "Flush": 0, "Straight": 0, "Three of a Kind": 0, 
                            "Two Pair": 0, "Pair": 0, "High Card": 0}
    seen_scores = set()
    encoded_deck = [encode(card) for card in deck.cards]
    for combo in combinations(encoded_deck, 5):
        score = score5(combo)
        hand_category = category(score)
        categories_and_hands[hand_category] += 1
        seen_scores.add(score)

    assert categories_and_hands == {"Royal Flush": 4, "Straight Flush": 36, "Four of a Kind": 624, 
                            "Full House": 3744, "Flush": 5108, "Straight": 10200, "Three of a Kind": 54912, 
                            "Two Pair": 123552, "Pair": 1098240, "High Card": 1302540}
    assert seen_scores == set(range(1, 7463))

# --- best_score: 5, 6, or 7 cards ---------------------------------------------------

def test_best_score_five_cards():
    assert best_score(_cards("As Ks Qs Js Ts")) == 1
    assert best_score(_cards("7s 5h 4d 3c 2s")) == 7462


def test_best_score_six_cards_finds_best_subset():
    assert best_score(_cards("9h As Ks Qs Js Ts")) == 1


def test_best_score_seven_cards_matches_score7():
    cards = _cards("Ah 8s Kh Qh 5c Jh Th")
    assert best_score(cards) == score7(cards) == 1


def test_best_score_matches_reference_on_random_hands():
    for n in (5, 6, 7):
        for _ in range(2000):
            deck = Deck()
            deck.shuffle()
            cards = [deck.deal() for _ in range(n)]
            encoded = [encode(c) for c in cards]
            expected = min(score5(combo) for combo in combinations(encoded, 5))
            assert best_score(cards) == expected


@pytest.mark.parametrize("n", [0, 4, 8])
def test_best_score_rejects_wrong_card_count(n):
    cards = _cards("As Ks Qs Js Ts 9s 8s 7s")[:n]
    with pytest.raises(ValueError):
        best_score(cards)
