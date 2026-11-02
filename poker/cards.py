import random
from dataclasses import dataclass

SUITS = "♠♥♦♣"
SUIT_LETTERS = {"s": "♠", "h": "♥", "d": "♦", "c": "♣"}
RANK_VALUES = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

# Card represents a single playing card. Cards are formatted as "rank" + "suit", e.g. "Q♠".
@dataclass(frozen=True)
class Card:
    rank: str
    suit: str
    
    @property
    def value(self):
        return RANK_VALUES[self.rank]

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    @classmethod
    def from_str(cls, card_str):
        #turns "Kd" into Card('K', '♦')
        
        
        if len(card_str) != 2:
            raise ValueError(f"Invalid card: {card_str}")
        if card_str[0] not in RANK_VALUES:
            raise ValueError(f"Invalid rank: {card_str[0]}")
        if card_str[1] not in SUIT_LETTERS:
            raise ValueError(f"Invalid suit: {card_str[1]}")
        return cls(card_str[0], SUIT_LETTERS[card_str[1]])

    def __post_init__(self):
        if self.rank not in RANK_VALUES:
            raise ValueError(f"Invalid rank: {self.rank}")
        if self.suit not in SUITS:
            raise ValueError(f"Invalid suit: {self.suit}")

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANK_VALUES]

    def shuffle(self):
        random.shuffle(self.cards)


    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None