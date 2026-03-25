
from cards import reshuffleDeck, dealCards
from gameLogic import DealCheck
from cpuDecision import basicStrat
from cards import calculateHandValue


def endRound(score, result, round,player_hand, dealer_hand):
    print(f"Final Player hand: {player_hand} with value {calculateHandValue(player_hand)}")
    print(f"Final Dealer hand: {dealer_hand} with value {calculateHandValue(dealer_hand)}")
    print(f"Round {round} ended with result: {result}. Current score: {score}.")
    print("--------------------------------------------------")
    print("Thanks for playing!")


def cpuPlay(player_hand, player_value, dealer_hand, dealer_show_value, deck, discard, score, round ):
    print(f"Player hand is {player_hand} with value {player_value}. Dealer show value: {dealer_show_value}.")
    score, result, player_hand = basicStrat(player_hand, player_value, dealer_hand, dealer_show_value, deck, discard, score)
    endRound(score, result, round, player_hand, dealer_hand)
    

def autoStartHand(deck, discard, shoe_marker, round, score):
    #Check if reshuffle is needed
    if shoe_marker <= discard:
        deck, discard, shoe_marker = reshuffleDeck()
        print(f"Reshuffled deck for round {round}. New deck has {len(deck)} cards.")
    #resest hands and deal
    player_hand = []
    dealer_hand = []
    deck, discard, dealer_value, player_value, dealer_show_value = dealCards(player_hand, dealer_hand, deck, discard)

    print(f"Round {round}: Player hand value: {player_value}, Dealer hand value: {dealer_show_value}")

    # Check for Blackjack and end round if necessary
    score, result = DealCheck(player_value, dealer_value, score)
    if result != "continue":
        print(f"Round {round} ended due to Blackjack.")
    else:
        print("No Blackjack this round. Continuing...")
        cpuPlay(player_hand, player_value, dealer_hand, dealer_show_value, deck, discard, score, round)



def autoPlaySetup():
    round = 0
    score = 0
    deck, discard, shoe_marker = reshuffleDeck()
    print(f"Created a new deck with {len(deck)} cards with marker {shoe_marker}.")
    autoStartHand(deck, discard, shoe_marker, round, score)

    



    