import random
import os
from .blackjackStragegy import get_strategy_move

class Player:
    #Player Variables
    def __init__(self, balance, playing, simulation_rounds,strategy):
        self.playing = playing
        self.balance = balance
        self.starting_balance = balance  # Track starting balance for simulation
        self.hands = [[]]  # List of hands (supports multiple splits)
        self.bets = [0]    # List of bets corresponding to each hand
        self.current_hand_index = 0  # Which hand is currently being played

        #Simulation tracking variables
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.rounds_played = 0  # Track actual rounds completed
        self.simulation_rounds = simulation_rounds
        self.current_round = 1  # Start at round 1
        self.strategy = strategy

    #Returns the value of a specific hand
    def get_hand_value(self, hand_index):
        if hand_index < len(self.hands):
            return get_hand_value(self.hands[hand_index])
        return 0
    
    def get_strategy_move(self, hand_index, dealer_up_card):
        if hand_index < len(self.hands):
            return get_strategy_move(self.hands[hand_index], dealer_up_card, self.strategy)
        return None
    
    @property
    def hand(self):
        return self.hands[0] if len(self.hands) > 0 else []
    
    @property
    def bet(self):
        return self.bets[0] if len(self.bets) > 0 else 0
    
    @bet.setter
    def bet(self, value):
        if len(self.bets) > 0:
            self.bets[0] = value
        else:
            self.bets.append(value)


class Dealer:
    #Dealer Variables
    def __init__(self):
        self.hand = []
    
    #Returns the value of the hand dynamically as cards are added
    @property
    def hand_value(self):
        return get_hand_value(self.hand)


class Deck:
    #Deck Variables
    def __init__(self, deck_num=6):
        self.deck_num = deck_num
        self.deck = self.create_deck()
        self.shoe = False
        

    #Deck Functions
    # Creates a standard deck of 52 cards and multiplies it by the number of decks specified    
    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        num_cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [(num, suit) for num in num_cards for suit in suits]
        deck *= self.deck_num  # Multiply the deck by the number of decks
        random.shuffle(deck)     #Shuffles the deck
        deck.insert(int(len(deck) * random.uniform(0.75, .90)), 'Shoe')  # Insert the shoe at a random position between 75% and 90% of the deck
        self.shoe = False  # Reset shoe flag when creating a new deck
        return deck

    def deal_cards(self, hand):
        """Deal cards to a hand, reshuffling deck if needed"""
        # Initial hand for the player and dealer (2 cards)
        if len(hand) == 0:
            hand.append(self._pop_card())
            hand.append(self._pop_card())
        # Counting hits and double downs for one more card
        else:
            hand.append(self._pop_card())
        
        # Check to see if shoe marker was dealt
        if 'Shoe' in hand: 
            hand.remove('Shoe')
            self.shoe = True
            hand.append(self._pop_card())
    
    def _pop_card(self):
        """Pop a card from deck, reshuffling if empty"""
        if len(self.deck) == 0:
            self.deck = self.create_deck()
        return self.deck.pop(0)
        

#Supporting Functions
def get_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        if card[0] in ['J', 'Q', 'K']:
            value += 10
        elif card[0] == 'A':
            aces += 1
        else:
            value += int(card[0])
    for _ in range(aces):
        if value + 11 > 21:
            value += 1
        else:
            value += 11
    return value

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux (posix)
    else:
        _ = os.system('clear')