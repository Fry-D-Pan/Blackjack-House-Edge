
#Basic Strategy Decisions for the CPU Player
split_table ={
    "2,2": {
        2: "split", 3: "split", 4: "split", 5: "split", 6: "split", 7: "split", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    "3,3": {
        2: "split", 3: "split", 4: "split", 5: "split", 6: "split", 7: "split", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    "4,4": {
        2: "hit", 3: "hit", 4: "hit", 5: "split", 6: "split", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    "5,5": {
        2: "double", 3: "double", 4: "double", 5: "double", 6: "double", 7: "double", 8: "double", 9: "double", 10: "hit", "Ace": "hit"
    },
    "6,6": {
        2: "split", 3: "split", 4: "split", 5: "split", 6: "split", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    "7,7": {
        2: "split", 3: "split", 4: "split", 5: "split", 6: "split", 7: "split", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    "8,8": {
        2: "split", 3: "split", 4: "split", 5: "split", 6: "split", 7: "split", 8: "split", 9: "split", 10: "split", "Ace": "split"
    },
    "9,9": {
        2: "split", 3: "split", 4: "split", 5: "split", 6: "split", 7: "stand", 8: "split", 9: "split", 10: "stand", "Ace": "stand"
    },
    "10,10": {
        2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "stand", 8: "stand", 9: "stand", 10: "stand", "Ace": "stand"
    },
    "Ace,Ace": {
        2: "split", 3: "split", 4: "split", 5: "split", 6: "split", 7: "split", 8: "split", 9: "split", 10: "split", "Ace": "split"
    }
}

soft_total_table = {
    13: {
        2: "hit", 3: "hit", 4: "hit", 5: "double", 6: "double", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    14: {
        2: "hit", 3: "hit", 4: "hit", 5: "double", 6: "double", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    15: {
        2: "hit", 3: "hit", 4: "double", 5: "double", 6: "double", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    16:{
        2: "hit", 3: "hit", 4: "double", 5: "double", 6: "double", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    17:{
        2: "hit", 3: "hit", 4: "hit", 5: "double", 6: "double", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    18:{
        2: "double", 3: "double", 4: "double", 5: "double", 6: "double", 7: "stand", 8: "stand", 9: "hit", 10: "hit", "Ace": "hit"
    },
    19:{
        2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "double", 7: "stand", 8: "stand", 9: "stand", 10: "stand", "Ace": "stand"
    },
    20:{
        2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "stand", 8: "stand", 9: "stand", 10: "stand", "Ace": "stand"
    }
}

hard_total_table = {
    4: {
        2: "hit", 3: "hit", 4: "hit", 5: "hit", 6: "hit", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    5: {
        2: "hit", 3: "hit", 4: "hit", 5: "hit", 6: "hit", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    6: {
        2: "hit", 3: "hit", 4: "hit", 5: "hit", 6: "hit", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    7: {
        2: "hit", 3: "hit", 4: "hit", 5: "hit", 6: "hit", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    8: {
        2: "hit", 3: "hit", 4: "hit", 5: "hit", 6: "hit", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    9: {
         2: "hit", 3: "double", 4: "double", 5: "double", 6: "double", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    10: {
        2: "double", 3: "double", 4: "double", 5: "double", 6: "double", 7: "double", 8: "double", 9: "double", 10: "hit", "Ace": "hit"
    },
    11: {
        2: "double", 3: "double", 4: "double", 5: "double", 6: "double", 7: "double", 8: "double", 9: "double", 10: "double", "Ace": "double"
    },
    12: {
        2: "hit", 3: "hit", 4: "stand", 5: "stand", 6: "stand", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    13: {
        2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    14: {
        2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    15: {
        2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    16: {
        2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "hit", 8: "hit", 9: "hit", 10: "hit", "Ace": "hit"
    },
    17: {
        2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "stand", 8: "stand", 9: "stand", 10: "stand", "Ace": "stand"
    },
    18: {
        2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "stand", 8: "stand", 9: "stand", 10: "stand", "Ace": "stand"
    },
    19: {
        2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "stand", 8: "stand", 9: "stand", 10: "stand", "Ace": "stand"
    },
    20: {
        2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "stand", 8: "stand", 9: "stand", 10: "stand", "Ace": "stand"
    }
}

def assignSplitIndex(player_hand):
    if (player_hand[0][0] in ['10', 'Jack', 'Queen', 'King']) and (player_hand[1][0] in ['Jack', 'Queen', 'King']):
        index = "10,10"
        return index
    elif player_hand[0][0] in ['10', 'Jack', 'Queen', 'King']:
        index = "10," + player_hand[1][0]
        return index
    elif player_hand[1][0] in ['10', 'Jack', 'Queen', 'King']:
        index = player_hand[0][0] + ",10"
        return index
    else:
        index = player_hand[0][0] + "," + player_hand[1][0]
        return index
    
def assignColumn(dealer_show_value):
    return "Ace" if dealer_show_value == 11 else dealer_show_value

def basicStrat(player_hand, player_value, dealer_hand, dealer_show_value, deck, discard, score):
    from gameLogic import actions
    ace_checker = 0

    # 1) Check for pair / split and return immediately if splitting
    if len(player_hand) == 2:
        if player_hand[0][0] == player_hand[1][0]:
            index = assignSplitIndex(player_hand)
            column = assignColumn(dealer_show_value)
            decision = split_table[index][column]
            score, result, player_hand = actions(player_hand, player_value, dealer_hand, dealer_show_value, deck, discard, score, decision)
            return score, result , player_hand


    # 2) Count aces to see if this is a soft hand
    for card, _ in player_hand:
        if card == 'Ace':
            ace_checker += 1

    index = player_value
    column = assignColumn(dealer_show_value)

    # 3) Soft vs hard table
    if ace_checker >= 1:
        decision = soft_total_table[index][column]
    else:
        decision = hard_total_table[index][column]

    score, result, player_hand = actions(player_hand, player_value, dealer_hand, dealer_show_value, deck, discard, score, decision)
    return score, result , player_hand