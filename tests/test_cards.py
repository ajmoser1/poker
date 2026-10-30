from poker.cards import Deck
import copy

def test_deck_has_52_unique_cards():
    deck = Deck()
    assert len(set(deck.cards)) == 52

def test_dealing_reduces_deck():
    deck = Deck()
    card = deck.deal()
    assert len(deck.cards) == 51
    assert card not in deck.cards

def test_shuffling_keeps_same_set():
    deck = Deck()
    original_cards = copy.copy(deck.cards)
    deck.shuffle()
    assert len(deck.cards) == 52
    assert set(deck.cards) == set(original_cards)