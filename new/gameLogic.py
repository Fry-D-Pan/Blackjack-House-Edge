import random
from cards import calculateHandValue
from cpuDecision import basicStrat



def actions(player_hand, player_value, dealer_hand, dealer_show_value, deck, discard, score, decision):
    if decision == "hit":
        print("Player chooses to hit.")
        player_hand.append(deck.pop(random.randint(0, len(deck)-1)))
        discard += 1

        if calculateHandValue(player_hand) > 21:
            print("Player busts after hit!")
            score -= 1
            result = "loss"
            return score , result, player_hand
        
        else:
            player_value = calculateHandValue(player_hand)
            print(f"Player hand value after hit: {player_value}")
            return basicStrat(player_hand, player_value, dealer_hand, dealer_show_value, deck, discard, score)
        

    elif decision == "stand":
        print("Player chooses to stand.")
        score, result = checkWinner(player_hand, dealer_hand, score)
        return score, result, player_hand
    

    elif decision == "double":
        print("Player chooses to double down.")
        checkWinner(player_hand, dealer_hand, score)
        score, result = checkWinner(player_hand, dealer_hand, score)
        score = score * 2
        return score, result, player_hand


    elif decision == "split":
        print("Player chooses to split.")
        result = "push"
        return score, result, player_hand


def DealCheck(player_value, dealer_total_value, score):
    if player_value == 21 and dealer_total_value == 21:
        print("Push! Both player and dealer have Blackjack.")
        result = "push"
        return score, result
    elif player_value == 21:
        print("Player has Blackjack! Winner!")
        score += 1
        result = "win"
        return score, result
    elif dealer_total_value == 21:
        print("Dealer has Blackjack! Loser!")
        score -= 1
        result = "loss"
        return score, result
    else:
        return score, "continue"

def checkWinner(player_hand, dealer_hand, score):
    result = "" 
    player_value = calculateHandValue(player_hand)
    dealer_value = calculateHandValue(dealer_hand)
    if player_value > 21:
        score -= 1
        print("Player busts! Dealer wins.")
        result = "loss"
        return score , result
    elif dealer_value > 21:
        score += 1
        print("Dealer busts! Player wins.")
        result = "win"
        return score , result
    elif player_value > dealer_value:
        score += 1
        print("Player wins!")
        result = "win"
        return score , result
    elif dealer_value > player_value:
        score -= 1
        print("Dealer wins!")
        result = "loss"
        return score , result
    else:
        print("Push! It's a tie.")
        result = "push"
        return score , result