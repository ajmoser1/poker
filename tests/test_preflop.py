from poker.cards import Card
from poker.preflop import evaluate_hands

premium_pair =      [Card('Q', '♠'), Card('Q', '♦')]
pair =              [Card('8', '♠'), Card('8', '♦')]
premium_broadway =  [Card('A', '♠'), Card('K', '♦')]
suited_ace =        [Card('A', '♠'), Card('7', '♠')]
suited_connector =  [Card('8', '♠'), Card('9', '♠')]
suited_one_gapper = [Card('T', '♠'), Card('8', '♠')]
trash =             [Card('2', '♠'), Card('7', '♦')]
trash_other_order = [Card('7', '♦'), Card('2', '♠')]

def test_premium_pair():
    assert evaluate_hands([premium_pair]) == ['Premium Pair']

def test_pair():
    assert evaluate_hands([pair]) == ['Pair']

def test_premium_broadway():
    assert evaluate_hands([premium_broadway]) == ['Premium Broadway']

def test_suited_ace():
    assert evaluate_hands([suited_ace]) == ['Suited Ace']

def test_suited_connector():
    assert evaluate_hands([suited_connector]) == ['Suited Connector']

def test_suited_one_gapper():
    assert evaluate_hands([suited_one_gapper]) == ['Suited One-Gapper']

def test_trash():
    assert evaluate_hands([trash]) == ['Trash']
    assert evaluate_hands([trash_other_order]) == ['Trash']