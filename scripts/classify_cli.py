from poker.cards import Card, Deck
from poker.preflop import evaluate_hands, RANKS, SUIT_TO_SYMBOL

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

def main():
    deck = Deck()
    deck.shuffle()
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



if __name__ == "__main__":
    main()