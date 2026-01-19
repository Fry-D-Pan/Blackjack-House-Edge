import random
import math
def newDeck (shoe):
    deck = []
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    for _ in range(shoe):
        for suit in suits:
            for i in range(1,14):
                if i == 1:
                    deck.append(['Ace', suit])
                elif i == 11:
                    deck.append(['Jack', suit])
                elif i == 12:
                    deck.append(['Queen', suit])
                elif i == 13:
                    deck.append(['King', suit])
                else:
                    deck.append([str(i), suit])
    return deck

def reshuffleDeck():
    print("Reshuffling the deck...")
    shoe_size = 6
    discard = 0
    deck = newDeck(shoe_size)
    shoe_marker = math.floor(random.randint(70, 85) / 100 * len(deck)) 
    return deck, discard, shoe_marker


def calculateHandValue(hand):
    value = 0
    aces = 0
    for card, _ in hand:
        if card in ['Jack', 'Queen', 'King']:
            value += 10
        elif card == 'Ace':
            aces += 1
            if value + 11 <= 21:
                value += 11
            else:
                value += 1
        else:
            value += int(card)
    return value



def showCardVaule(hand):
    
    rank, _ = hand[0] 
    value = 0

    if rank in ['Jack', 'Queen', 'King']:
        value = 10
    elif rank == 'Ace':
        value = 11
    else:
        value = int(rank)

    return value

def dealCards(player_hand, dealer_hand, deck, discard):
    for _ in range(2):
        dealer_hand.append(deck.pop(random.randint(0, len(deck)-1)))
        discard += 1
        player_hand.append(deck.pop(random.randint(0, len(deck)-1)))
        discard += 1
    dealer_show_value = showCardVaule(dealer_hand)
    dealer_value = calculateHandValue(dealer_hand)
    player_value = calculateHandValue(player_hand)
    print(f"Dealt cards. Player hand: {player_hand} with value {player_value}, Dealer upcard: {dealer_hand[0]} with value {dealer_show_value}")
    return deck, discard, dealer_value, player_value, dealer_show_value