"""Seven-card hand evaluation.

Wraps the compiled Cactus Kev / Senzee 5-card evaluator in ``_eval.dylib`` (built from
``evaluator.c``). All poker meaning lives here in Python: encoding a ``Card`` into Kev's
32-bit integer layout, iterating the 21 five-card subsets of seven cards, and decoding the
resulting 1..7462 score into a category and readable name.

Score semantics: 1 is a royal flush, 7462 is 7-5-4-3-2 offsuit. LOWER IS BETTER.
Two hands with equal scores are an exact tie.

Build the library from the repo root with:
    cc -shared -O2 -Wall -o poker/_eval.dylib poker/evaluator.c
"""

import ctypes
import itertools
from dataclasses import dataclass
from pathlib import Path
from poker.cards import Card
from math import inf

# --- Loading the compiled evaluator -------------------------------------------------

_LIB_PATH = Path(__file__).with_name("_eval.dylib")
_lib = ctypes.CDLL(str(_LIB_PATH))
_lib.eval_5hand_fast.restype = ctypes.c_int
_lib.eval_5hand_fast.argtypes = [ctypes.c_int] * 5


# --- Card encoding (Cactus Kev layout) ----------------------------------------------
#
#   +--------+--------+--------+--------+
#   |xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
#   +--------+--------+--------+--------+
#   b: one bit per rank, bit 0 = deuce .. bit 12 = ace   (bits 16..28)
#   cdhs: one bit for the suit                            (bits 12..15)
#   r: rank number 0..12                                  (bits 8..11)
#   p: prime for the rank                                 (bits 0..7)

RANK_ORDER = "23456789TJQKA"
PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
SUIT_BITS = {"♣": 8, "♦": 4, "♥": 2, "♠": 1} #Club, Diamond, Heart, Spade


def encode(card: Card) -> int:
    rank = RANK_ORDER.find(card.rank)
    prime = PRIMES[rank]
    suit_bits = SUIT_BITS[card.suit]
    rank_bitmask = 1 << (rank + 16)
    return rank_bitmask | (suit_bits << 12) | (rank << 8) | prime


# --- Scoring ------------------------------------------------------------------------


def score5(cards: tuple[int, int, int, int, int]) -> int:
    """Score five already-encoded cards. 1 best, 7462 worst."""
    return _lib.eval_5hand_fast(*cards)


def score7(cards) -> int:
    """Best 5-card score among seven Card objects.
    Encode each card, iterate every 5-card subset, keep the minimum score.
    """
    min_score = inf
    for subset in itertools.combinations(cards, 5):
        score = score5(subset)
        if score < min_score:
            min_score = score
    return min_score


# --- Decoding a score into a category and a name -----------------------------------
#
# Kev assigns classes in contiguous blocks. Fill in the inclusive upper bound of each
# block, best category first. Source: hand_rank() in Kev's code, or derive the counts
# yourself (how many distinct straight flushes are there? quads? ...). Both are
# worthwhile; the second is a good checkpoint exercise.

CATEGORY_BOUNDS = (
    (1, "Royal Flush"), 
    (10, "Straight Flush"), 
    (167, "Four of a Kind"), 
    (467, "Full House"), 
    (1599, "Flush"), 
    (1609, "Straight"), 
    (2467, "Three of a Kind"), 
    (3222, "Two Pair"), 
    (6185, "One Pair"), 
    (7462, "High Card")
)


def category(score: int) -> str:
    """Map a 1..7462 score to its category name."""
    for upper_bound, category_name in CATEGORY_BOUNDS:
        if score <= upper_bound:
            return category_name
    return "High Card"


@dataclass(frozen=True)
class HandResult:
    """What the interface and simulator get back from best_hand().

    score: comparable value, lower is better.
    category: e.g. "Full House".
    name: readable description, e.g. "Full House, Kings over Fours". Optional at first;
          category alone is enough for plan 03's first version.
    """

    score: int
    category: str
    name: str = ""

    def beats(self, other: "HandResult") -> bool:
        return self.score < other.score


def best_hand(cards) -> HandResult:
    """Evaluate seven Card objects."""
    score = score7(cards)
    category = category(score)
    return HandResult(score, category)
