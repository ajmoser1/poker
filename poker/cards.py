import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str
    rank_values = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    @property
    def value(self):
        return Card.rank_values[self.rank] if self.rank in Card.rank_values else int(self.rank)

    def __repr__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        self.suits = ['♠', '♥', '♦', '♣']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        random.shuffle(self.cards)


    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None