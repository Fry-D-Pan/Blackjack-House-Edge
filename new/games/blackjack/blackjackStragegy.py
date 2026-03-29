# Basic Blackjack Strategy
# h = hit, s = stand, d = double down (hit if unable), p = split

# Hard totals strategy (no ace or ace counted as 1)
# Rows: Player total (5-20)
# Columns: Dealer up card (2, 3, 4, 5, 6, 7, 8, 9, 10, A)
Basic_HARD_STRATEGY = {
    5:  ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],
    6:  ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],
    7:  ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],
    8:  ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],
    9:  ['h', 'd', 'd', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],
    10: ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'h', 'h'],
    11: ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'h'],
    12: ['h', 'h', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],
    13: ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],
    14: ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],
    15: ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],
    16: ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],
    17: ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],
    18: ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],
    19: ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],
    20: ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],
}

# Soft totals strategy (ace counted as 11)
# Rows: Player total (13-20, where 13 means A-2, 14 means A-3, etc.)
# Columns: Dealer up card (2, 3, 4, 5, 6, 7, 8, 9, 10, A)
Basic_SOFT_STRATEGY = {
    13: ['h', 'h', 'h', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # A-2
    14: ['h', 'h', 'h', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # A-3
    15: ['h', 'h', 'd', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # A-4
    16: ['h', 'h', 'd', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # A-5
    17: ['h', 'd', 'd', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # A-6
    18: ['s', 'd', 'd', 'd', 'd', 's', 's', 'h', 'h', 'h'],  # A-7
    19: ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # A-8
    20: ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # A-9
}

# Pair splitting strategy
# Rows: Pair value (2-11, where 11 is A-A)
# Columns: Dealer up card (2, 3, 4, 5, 6, 7, 8, 9, 10, A)
Basic_PAIR_STRATEGY = {
    2:  ['p', 'p', 'p', 'p', 'p', 'p', 'h', 'h', 'h', 'h'],  # 2-2
    3:  ['p', 'p', 'p', 'p', 'p', 'p', 'h', 'h', 'h', 'h'],  # 3-3
    4:  ['h', 'h', 'h', 'p', 'p', 'h', 'h', 'h', 'h', 'h'],  # 4-4
    5:  ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'h', 'h'],  # 5-5 (never split, treat as hard 10)
    6:  ['p', 'p', 'p', 'p', 'p', 'h', 'h', 'h', 'h', 'h'],  # 6-6
    7:  ['p', 'p', 'p', 'p', 'p', 'p', 'h', 'h', 'h', 'h'],  # 7-7
    8:  ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],  # 8-8
    9:  ['p', 'p', 'p', 'p', 'p', 's', 'p', 'p', 's', 's'],  # 9-9
    10: ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # 10-10
    11: ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],  # A-A
}

# Dealer card mapping for easier lookup
DEALER_CARDS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # 11 represents Ace


def card_value(card):
    """Convert a card tuple to its numeric value for strategy lookup"""
    rank = card[0]
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    else:
        return int(rank)


def get_strategy_move(player_hand, dealer_up_card, strategy):
   
    # Convert dealer card to value and get index
    dealer_value = card_value(dealer_up_card)
    dealer_index = DEALER_CARDS.index(dealer_value)
    
    # Convert player cards to values without modifying original hand
    card_values = [card_value(card) for card in player_hand]
    
    # Check for pair (same rank on both initial cards)
    is_pair = (len(player_hand) == 2 and player_hand[0][0] == player_hand[1][0])
    
    if is_pair:
        # Get the rank value for pair lookup
        pair_value = card_values[0]
        if strategy == "basic":
            if pair_value in Basic_PAIR_STRATEGY:
                return Basic_PAIR_STRATEGY[pair_value][dealer_index]
    
    # Calculate total and check for soft hand
    total = sum(card_values)
    has_ace = any(card[0] == 'A' for card in player_hand)
    
    # Determine if it's a soft hand (ace counted as 11 and total <= 21)
    is_soft = has_ace and total <= 21 and len(player_hand) == 2
    
    # If total > 21, recalculate treating aces as 1
    if total > 21 and has_ace:
        total = 0
        aces = 0
        for card in player_hand:
            if card[0] in ['J', 'Q', 'K']:
                total += 10
            elif card[0] == 'A':
                aces += 1
            else:
                total += int(card[0])
        
        # Add aces optimally
        for _ in range(aces):
            if total + 11 <= 21:
                total += 11
                is_soft = True
            else:
                total += 1
                is_soft = False
    
    # Look up strategy based on hand type
    if strategy == "basic":
        if is_soft and total in Basic_SOFT_STRATEGY:
            return Basic_SOFT_STRATEGY[total][dealer_index]
        elif total in Basic_HARD_STRATEGY:
            return Basic_HARD_STRATEGY[total][dealer_index]
    
    # Default behavior for edge cases
    if total >= 17:
        return 's'
    else:
        return 'h'