def instructions():
    print("Instructions:")
    print("1. The goal of Blackjack is to have a hand value as close to 21 as possible without going over.")
    print("2. Each player starts with two cards, and the dealer also gets two cards (one face up and one face down).")
    print("3. Players can choose to \n  'Hit' (take another card) \n  'Stand' (keep their current hand) " \
    "\n  'Double Down' (double your bet and take one more card) \n  'Split' (if you have two cards of the same value, you can split them into two separate hands).")
    print("4. If a player's hand exceeds 21, they 'bust' and lose the game.")
    print("5. After all players have finished their turns, the dealer reveals their hidden card and plays according to set rules.")
    print("6. The player with the highest hand value that does not exceed 21 wins!\n\n")

def blackjackGame():
    balance = input("Enter how much money you want to start with: ")
    balance = round(float(balance), 2)
    print(f"You have ${balance} to start with. Good luck!")


def blackjackGameMain():
    print("Welcome to Blackjack!")
    instructions()    
    blackjackGame()

    

    