RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
RANK_TO_INDEX = {rank: index for index, rank in enumerate(RANKS)}
SUIT_TO_SYMBOL = {'s': '♠', 'h': '♥', 'd': '♦', 'c': '♣'}


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
    if pair:
        return "Pair"
    if hand_code in {"AKs", "AKo", "AQs", "AQo", "AJs", "KQs"}:
        return "Premium Broadway"
    if hand_code in {"KQo", "KJs", "KJo", "QJs", "QJo", "JTs"}:
        return "Broadway"
    if suited and high_rank == 'A' and low_rank in "23456789T":
        return "Suited Ace"
    if suited and gap == 0:
        return "Suited Connector"
    if suited and gap == 1:
        return "Suited One-Gapper"

    return "Trash"

def evaluate_hands(hands):
    return [evaluate_hand(hand) for hand in hands]