"""Tests for poker.evaluator.

Fill in the cases from plan 02, step 5. The three below are the smoke test already run
by hand against the compiled library; they pin the tables and the encoder.
"""

from poker.cards import Card
from poker.evaluator import best_hand, encode, score5, score7


def _cards(spec: str):
    """Build Cards from a string like 'As Kh Td'. Suits: s h d c."""
    return [Card.from_str(card) for card in spec.split()]


def test_royal_flush_scores_1():
    royal = tuple(encode(c) for c in _cards("As Ks Qs Js Ts"))
    assert score5(royal) == 1


def test_worst_hand_scores_7462():
    worst = tuple(encode(c) for c in _cards("7s 5h 4d 3c 2s"))
    assert score5(worst) == 7462


def test_wheel_is_the_weakest_straight():
    wheel = tuple(encode(c) for c in _cards("As 2h 3d 4c 5s"))
    assert score5(wheel) == 1609


# --- Encoder ------------------------------------------------------------------------
# three or four cards whose integer you computed on paper. For example, what is
# the king of diamonds? Work the bits out, then assert encode(...) == that number.
def test_king_of_diamonds():
    king_of_diamonds = encode(Card.from_str("Kd"))
    assert king_of_diamonds == 0b00001000000000000100101100100101


# --- Seven-card and categories -------------------------------------------------------
# TODO (plan 02 step 5): one per category, steel wheel, flush beaten by nothing else in
# hand, full house vs full house, two trips, three pairs, kicker decides, exact tie.



# TODO (step 6): category boundaries, e.g. worst straight flush vs best quads.
