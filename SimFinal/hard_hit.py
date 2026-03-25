import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from IPython.display import display

# Strategy Dataframes
basic_data = [['H']*10, ['H']*10, ['H']*10, ['H']*10, ['H']*10, 
              ['H'] + ['D']*4 + ['H']*5,
              ['D']*8 + ['H']*2, ['D']*10, ['H']*2 + ['S']*3 + ['H']*5, 
              ['S']*5 + ['H']*5, ['S']*5 + ['H']*5, 
              ['S']*5 + ['H']*5, ['S']*5 + ['H']*5, 
              ['S']*10,['S']*10, ['S']*10, ['S']*10,['S']*10]
strategy_basic = pd.DataFrame(index=[4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21], 
                              columns=[2,3,4,5,6,7,8,9,10,'A'], data=basic_data)

ace_data = [['H']*2 + ['S']*3 + ['H']*5, 
            ['H']*3 + ['D']*2 + ['H']*5, ['H']*3 + ['D']*2 + ['H']*5,
            ['H']*2 + ['D']*3 + ['H']*5, ['H']*2 + ['D']*3 + ['H']*5,
            ['H'] + ['D']*4 + ['H']*5, ['S'] + ['D']*4 + ['S']*2 + ['H']*3, 
            ['S']*10, ['S']*10, ['S']*10]
strategy_ace = pd.DataFrame(index=[12,13,14,15,16,17,18,19,20,21], 
                            columns=[2,3,4,5,6,7,8,9,10,'A'], data=ace_data)

pair_data = [['P']*5 + ['H']*5, ['P']*5 + ['H']*5, ['H']*3 + ['P']*2 + ['H']*5,
             ['D']*8 + ['H']*2, ['P']*5 + ['H']*5, ['P']*6 + ['H']*4, ['P']*10,
             ['P']*5 + ['S'] + ['P']*2 + ['S']*2, ['S']*10, ['P']*10]
strategy_pair = pd.DataFrame(index=[4,6,8,10,12,14,16,18,20,22], 
                             columns=[2,3,4,5,6,7,8,9,10,'A'], data=pair_data)

print('Basic Strategy')
display(strategy_basic)
print('Ace Strategy')
display(strategy_ace)
print('Pair Strategy')
display(strategy_pair)

# Classes
class Player:
    def __init__(self, stack, bet):
        self.hand = []
        self.hand_pts = 0
        self.action = ''
        self.stack = stack
        self.bet = bet
        self.result_tracking = ['P', 'P']  # Initialize result tracking with two pushes

    # Gets hand points total
    def update_hand_points(self):
        self.hand_pts = get_hand_points(self.hand)

    # What the player will do 
    def update_action(self, dealer_up_card, split_handler):
        self.action = player_strategy_decision(dealer_up_card, split_handler)

    # Sets the tracking to wins and losses
    def update_result_tracking(self, result):
        self.result_tracking.append(result)


class Deck:
    def __init__(self, num_decks=8, shuffle_penetration=0.8):
        # A standard deck of 52 cards multiplied by the number of decks
        self.deck = ([i for i in range(2, 11)] + ["J", "Q", "K", "A"]) * 4 * num_decks
        self.deck = [10 if i in ('J', 'Q', 'K') else i for i in self.deck]  # Face cards value 10
        self.cards = self.deck.copy()
        random.shuffle(self.cards)  # Initial shuffle
        self.count = 0
        self.shuffle_penetration = shuffle_penetration
        self.num_decks = num_decks
        self.cards_dealt = 0  # Tracks the number of cards dealt from the shoe

    def update_count(self, card):
        if card in [2, 3, 4, 5, 6]:
            self.count += 1
        elif card in [10, 'A']:
            self.count -= 1

    def reshuffle(self):
        # Resets and reshuffles the shoe
        self.cards = self.deck.copy()
        random.shuffle(self.cards)
        self.count = 0
        self.cards_dealt = 0  # Reset dealt cards counter
        print("Deck reshuffled!")  # Optional debug message

    def deal_card(self):
        # Check if deck penetration threshold is reached
        if self.cards_dealt / len(self.deck) >= self.shuffle_penetration:
            self.reshuffle()
        
        card = self.cards.pop()  # Deal a card from the deck
        self.update_count(card)  # Update the card count
        self.cards_dealt += 1
        return card
    


# Main Functions
def get_hand_points(hand):
    points = sum([11 if i == 'A' else i for i in hand])
    ace_count = hand.count('A')
    for i in range(0, ace_count):
        if points > 21:
            points -= 10
    return points

def dealer_play(dealer_hand):
    dealer_total = get_hand_points(dealer_hand)
    while dealer_total < 17:  # Dealer hits on 16 or less
        dealer_hand.append(shoe.deal_card())
        dealer_total = get_hand_points(dealer_hand)
    return dealer_total

def player_strategy_decision(dealer_up_card, split_handler):
    if main_player.hand_pts <= 15:
        return 'H'
    if main_player.hand == ['A', 'A'] and split_handler:
        return 'P'
    elif main_player.hand[0] == main_player.hand[1] and len(main_player.hand) == 2 and split_handler:
        strategy_df = strategy_pair
    elif 'A' in main_player.hand and len(main_player.hand) == 2:
        strategy_df = strategy_ace
    else:
        strategy_df = strategy_basic

    strat = strategy_df.loc[main_player.hand_pts, dealer_up_card]

    if strat == 'D' and len(main_player.hand) > 2:
        strat = 'H'
    return strat


def evaluate_hands(dealer_hand, dealer_total, split_ind):
    if main_player.hand_pts > 21:
        main_player.stack -= main_player.bet
        message_print_toggle('Player Bust')
        main_player.update_result_tracking('L')
    elif dealer_total > 21:
        if main_player.hand_pts == 21 and len(main_player.hand) == 2 and not split_ind:
            message_print_toggle('Player Blackjack!')
            main_player.stack += main_player.bet * 1.5  # Blackjack payout (1.5x bet)
        else:
            main_player.stack += main_player.bet
        message_print_toggle('Dealer Bust')
        main_player.update_result_tracking('W')
    elif main_player.hand_pts == dealer_total:
        message_print_toggle('Push')
        main_player.update_result_tracking('P')
    elif main_player.hand_pts == 21 and len(main_player.hand) == 2:
        if not split_ind:
            message_print_toggle('Player Blackjack!')
            main_player.stack += main_player.bet * 1.5  # Blackjack payout (1.5x)
        else:
            main_player.stack += main_player.bet
        main_player.update_result_tracking('W')
    elif dealer_total > main_player.hand_pts:
        main_player.stack -= main_player.bet
        message_print_toggle('Player Loss')
        main_player.update_result_tracking('L')
    else:
        main_player.stack += main_player.bet
        message_print_toggle('Player Win')
        main_player.update_result_tracking('W')    
    message_print_toggle('-------Hand Complete-------')

def hand_prep(bet):
    main_player.hand = [shoe.deal_card(), shoe.deal_card()]
    main_player.update_hand_points()
    main_player.bet = bet
    dealer_hand = [shoe.deal_card(), shoe.deal_card()]
    main_player.update_action(dealer_hand[1], True)
    return dealer_hand


def play_hand(dealer_hand):
    dealer_total = get_hand_points(dealer_hand)
    if dealer_total == 21:
        message_print_toggle('Dealer Blackjack!')
        evaluate_hands(dealer_hand, dealer_total, False)
    else:
        if main_player.action == 'P':
            player_hands = split_handling(dealer_hand)
            message_print_toggle('Split')
            message_print_toggle(f'Split player hands: {player_hands}')
        else:
            player_hands = [main_player.hand]

        for hand in player_hands:
            main_player.hand = hand
            main_player.update_hand_points()

            while main_player.hand_pts < 21:
                main_player.update_action(dealer_hand[1], False)
                if main_player.action == 'H':  # Hit
                    main_player.hand.append(shoe.deal_card())
                    main_player.update_hand_points()
                elif main_player.action == 'S':  # Stand
                    break
                elif main_player.action == 'D':  # Double Down
                    main_player.stack -= main_player.bet
                    main_player.hand.append(shoe.deal_card())
                    main_player.update_hand_points()
                    break

            # After player action is complete, play dealer's hand
            dealer_total = dealer_play(dealer_hand)
            evaluate_hands(dealer_hand, dealer_total, False)

def split_handling(dealer_hand):
    card1, card2 = main_player.hand
    new_hand_1 = [card1, shoe.deal_card()]
    new_hand_2 = [card2, shoe.deal_card()]
    return [new_hand_1, new_hand_2]


def message_print_toggle(message):
    print(message)


# Simulation setup
main_player = Player(stack=10000, bet=100)
shoe = Deck()
dealer_hand = hand_prep(50)
play_hand(dealer_hand)

# Function to run the game for multiple iterations
def simulate_hands(num_iterations):
    wins = 0
    losses = 0
    pushes = 0
    final_stack = main_player.stack  # Track the player's final stack

    for _ in range(num_iterations):
        dealer_hand = hand_prep(50)  # Initialize dealer hand for each iteration
        play_hand(dealer_hand)  # Play the hand

        # Track results and update stack
        result = main_player.result_tracking[-1]  # Get result of most recent hand
        if result == 'W':
            wins += 1
            # Add the bet to the stack (or 1.5x the bet if it's a Blackjack)
            if main_player.hand_pts == 21 and len(main_player.hand) == 2:
                final_stack += main_player.bet * 1.5
            else:
                final_stack += main_player.bet
        elif result == 'L':
            losses += 1
            final_stack -= main_player.bet  # Subtract the bet on loss
        elif result == 'P':
            pushes += 1  # No change to the stack on a push

    return wins, losses, pushes, final_stack

# Ask how many iterations the user wants
num_iterations = int(input("Enter the number of iterations to simulate: "))

# Simulate hands and display the results
wins, losses, pushes, final_stack = simulate_hands(num_iterations)

# Calculate statistics
house_edge = ((10000 - final_stack)/(num_iterations * 100)) * 100
# Display statistics
print(f"House Edge:  {house_edge}")
print(f"After {num_iterations} hands:")
print(f"Final stack: {final_stack:.2f}")
