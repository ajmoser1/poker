import random
import itertools


class Card:
    rank_values = {
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14,
    }

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = self.rank_values[rank] if rank in self.rank_values else int(rank)

    def __repr__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        self.suits = ['♠', '♥', '♦', '♣']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None