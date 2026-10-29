from numpy import void

from deck import Card, Deck

deck = Deck()
deck.shuffle()

RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
RANK_TO_INDEX = {rank: index for index, rank in enumerate(RANKS)}
RANK_TO_INDEX['10'] = RANK_TO_INDEX['T']
SUIT_TO_SYMBOL = {'s': '♠', 'h': '♥', 'd': '♦', 'c': '♣'}


matrix = [
    [
        f'{r1}{r2}s' if i < j else (f'{r1}{r2}o' if i > j else f'{r1}{r2}')
        for j, r2 in enumerate(RANKS)
    ]
    for i, r1 in enumerate(RANKS)
]

def choose_card(card_number):
    print(f"\nChoose rank for card {card_number}:")
    print("A: 1, K: 2, Q: 3... 2: 13")
        

    while True:
        try:
            rank_choice = int(input("Rank number: "))
            rank = RANKS[rank_choice - 1]
            break
        except (ValueError, IndexError):
            print("Choose a number from 1 to 13.")

    suits = list(SUIT_TO_SYMBOL.values())
    print("\nChoose suit:")
    for index, suit in enumerate(suits, start=1):
        print(f"{index}. {suit}")

    while True:
        try:
            suit_choice = int(input("Suit number: "))
            suit = suits[suit_choice - 1]
            break
        except (ValueError, IndexError):
            print("Choose a number from 1 to 4.")

    return Card('10' if rank == 'T' else rank, suit)


def evaluate_hand(hand):
    card1, card2 = hand
    
    index1 = RANK_TO_INDEX[card1.rank]
    index2 = RANK_TO_INDEX[card2.rank]

    high_index = min(index1, index2)
    low_index = max(index1, index2)

    high_rank = RANKS[high_index]
    low_rank = RANKS[low_index]

    suited = card1.suit == card2.suit
    pair = high_index == low_index
    gap = low_index - high_index - 1

    hand_code = (
        f"{high_rank}{low_rank}"
        if pair
        else f"{high_rank}{low_rank}{'s' if suited else 'o'}"
    )

    if pair and high_index <= RANK_TO_INDEX['J']:
        return "Premium Pair"
    if hand_code in {"AKs", "AKo"}:
        return "Premium Broadway"
    if hand_code in {"TT", "99", "AQs", "AQo", "AJs", "KQs"}:
        return "Strong Hand"
    if pair:
        return "Medium Pair"
    if suited and high_rank == 'A' and low_rank in "23456789":
        return "Suited Ace"
    if suited and gap == 0:
        return "Suited Connector"
    if suited and gap == 1:
        return "Suited One-Gapper"

    return "Trash"


def evaluate_hands(hands):
    return [evaluate_hand(hand) for hand in hands]
    



print("\nHand evaluation\n")
players = int(input("Enter the number of players (2-6): "))
choice = input("\nType [c] to choose hand or [enter] for random: ")

if choice == 'c':
    card1 = choose_card(1)
    deck.cards = [
        card for card in deck.cards
        if (card.rank, card.suit) != (card1.rank, card1.suit)
    ]
    card2 = choose_card(2)
    while (card2.rank, card2.suit) == (card1.rank, card1.suit):
        print("You already selected that card. Choose a different card.")
        card2 = choose_card(2)
    deck.cards = [
        card for card in deck.cards
        if (card.rank, card.suit) != (card2.rank, card2.suit)
    ]
    hands = [[card1, card2]] + [[deck.deal() for _ in range(2)] for _ in range(players - 1)]

else:
    hands = [[deck.deal() for _ in range(2)] for _ in range(players)]


hand_types = evaluate_hands(hands)
for i, hand in enumerate(hands):
    label = "Your hand" if i == 0 else f"Player {i + 1}"
    print("\n",hand, f"{label}:", hand_types[i])
