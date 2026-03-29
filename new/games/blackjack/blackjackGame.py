from . import classes


# Instructions
def instructions():
    print("Instructions:")
    print("1. The goal of Blackjack is to have a hand value as close to 21 as possible without going over.")
    print("2. Each player starts with two cards, and the dealer also gets two cards (one face up and one face down).")
    print("3. Players can choose to \n  'Hit' (take another card) \n  'Stand' (keep their current hand) " \
    "\n  'Double Down' (double your bet and take one more card) \n  'Split' (if you have two cards of the same value, you can split them into two separate hands).")
    print("4. If a player's hand exceeds 21, they 'bust' and lose the game.")
    print("5. After all players have finished their turns, the dealer reveals their hidden card and plays according to set rules.")
    print("6. The player with the highest hand value that does not exceed 21 wins!\n\n")


def decisions(player, dealer, deck):
    #Checks to see if this is player or simulation and handles the betting
    if player.playing == True:
        bet = input("Enter amount to bet: ")
        if bet.isdigit() and int(bet) > 0 and int(bet) <= player.balance:
            player.bet = int(bet)
            player.balance -= player.bet
            print(f"You bet ${player.bet}. Your current balance is ${player.balance}.\n")
        else:
            print("Invalid bet amount. Please enter a positive number that does not exceed your current balance.")
            decisions(player, dealer, deck)
    else:
        #Come back for this in simulation
        pass
    
    # Deals the initial cards to the player and dealer
    deck.deal_cards(player.hands[0])
    deck.deal_cards(dealer.hand)
    if not check_blackjack(dealer, player):
        play_all_hands(player, dealer, deck)
    else:
        # Round ends immediately - blackjack detected
        new_round(player, dealer, deck)

def play_all_hands(player, dealer, deck):
    #Plays through all player hands sequentially before dealer's turn
    hand_index = 0
    while hand_index < len(player.hands):
        player.current_hand_index = hand_index
        play_hand(player, dealer, deck, hand_index)
        hand_index += 1
    
    # All hands complete - now dealer's turn
    classes.clear_terminal()
    print("\n=== All hands complete. Dealer's turn ===")
    dealer_play(dealer, player, deck)
    get_results(player, dealer, deck)


def play_hand(player, dealer, deck, hand_index):
    #Plays a single hand to completion
    current_hand = player.hands[hand_index]
    current_bet = player.bets[hand_index]
    hand_value = player.get_hand_value(hand_index)
    
    classes.clear_terminal()
    
    # Display all hands if multiple exist
    if len(player.hands) > 1:
        print(f"\n=== Playing Hand {hand_index + 1} of {len(player.hands)} ===")
        for i, hand in enumerate(player.hands):
            status = " (CURRENT)" if i == hand_index else ""
            print(f"Hand {i + 1}: {hand} (Value: {player.get_hand_value(i)}, Bet: ${player.bets[i]}){status}")
    else:
        print(f"Your hand: {current_hand} (Value: {hand_value})")
    
    print(f"\nDealer's hand: [{dealer.hand[0]}, ('Hidden Card')] (Value: {classes.get_hand_value([dealer.hand[0]])})\n")
    
    if player.playing:
        # Determine available options
        can_split = (len(current_hand) == 2 and 
                    current_hand[0][0] == current_hand[1][0] and 
                    player.balance >= current_bet)
        can_double = player.balance >= current_bet and len(current_hand) == 2
        
        # Display options
        # Player mode
        if player.playing == True:
            if can_split:
                option = input("Options:\n 1) Hit\n 2) Stand\n 3) Double Down\n 4) Split\n")
            elif can_double:
                option = input("Options:\n 1) Hit\n 2) Stand\n 3) Double Down\n")
            else:
                option = input("Options:\n 1) Hit\n 2) Stand\n")
        #simulation mode
        else:
            # Simulation mode
            pass
        match option:
            case "1":  # Hit
                deck.deal_cards(current_hand)
                hand_value = player.get_hand_value(hand_index)
                if hand_value > 21:
                    print("Busted! Your hand value exceeded 21.\n")
                    return
                play_hand(player, dealer, deck, hand_index)
            
            case "2":  # Stand
                print(f"You chose to stand on hand {hand_index + 1}.\n")
                return
            
            case "3":  # Double Down
                if can_double:
                    player.balance -= current_bet
                    player.bets[hand_index] *= 2
                    deck.deal_cards(current_hand)
                    new_value = player.get_hand_value(hand_index)
                    print(f"You doubled down. Hand: {current_hand} (Value: {new_value})\n")
                    if new_value > 21:
                        print(f"Hand {hand_index + 1} busted!\n")
                    return  # Double down = automatic stand
                else:
                    print("Cannot double down. Try again.\n")
                    play_hand(player, dealer, deck, hand_index)
            
            case "4":  # Split
                if can_split:
                    # Create new hand from split card
                    split_card = current_hand.pop()
                    player.hands.insert(hand_index + 1, [split_card])
                    player.bets.insert(hand_index + 1, current_bet)
                    player.balance -= current_bet
                    
                    # Deal one card to each hand
                    deck.deal_cards(player.hands[hand_index])
                    deck.deal_cards(player.hands[hand_index + 1])
                    
                    print(f"You split! Now playing hand {hand_index + 1}.\n")
                    play_hand(player, dealer, deck, hand_index)
                else:
                    print("Cannot split. Try again.\n")
                    play_hand(player, dealer, deck, hand_index)
            
            case _:
                print("Invalid option. Try again.\n")
                play_hand(player, dealer, deck, hand_index)
       

def dealer_play(dealer, player, deck):
    # Dealer's turn logic
    print(f"Dealer's hand: {dealer.hand} (Value: {dealer.hand_value})\n")
    while dealer.hand_value < 17:
        print("Dealer hits.")
        deck.deal_cards(dealer.hand)
        print(f"Dealer's hand: {dealer.hand} (Value: {dealer.hand_value})")
    
    if dealer.hand_value > 21:
        print("Dealer busts! All remaining player hands win!\n")
        player.balance += sum(player.bets) * 2  # Pay out all remaining bets
        end_game(player, dealer, deck)
    else:
        print("Dealer stands.\n")

def get_results(player, dealer, deck):
    for i, hand in enumerate(player.hands):
        hand_value = player.get_hand_value(i)
        print(f"Hand {i + 1}: {hand} (Value: {hand_value}, Bet: ${player.bets[i]})")
        print(f"Dealer's hand: {dealer.hand} (Value: {dealer.hand_value})\n")
        if hand_value > 21:
            print(f"Hand {i + 1} busted. You lose ${player.bets[i]}.\n")
        elif hand_value > dealer.hand_value:
            print(f"Hand {i + 1} wins! You win ${player.bets[i] * 2}.\n")
            player.balance += player.bets[i] * 2
        elif hand_value == dealer.hand_value:
            print(f"Hand {i + 1} pushes. Your bet of ${player.bets[i]} is returned.\n")
            player.balance += player.bets[i]
        else:
            print(f"Hand {i + 1} loses. You lose ${player.bets[i]}.\n")
    end_game(player, dealer, deck)

def check_blackjack(dealer, player):
    # Check for dealer blackjack
    # Check for player blackjack
    if player.get_hand_value(0) == 21:
        print(f"Congratulations! You have Blackjack with hand {player.hands[0]}! You win 1.5x your bet.\n")
        player.balance += int(player.bet * 2.5)  # Return original bet + 1.5x winnings
        return True
    elif dealer.hand_value == 21:
        print(f"Dealer has Blackjack with hand {dealer.hand}! All player hands lose.\n")
        return True
    else:
        return False


def new_round(player, dealer, deck):
    # Resets the player's and dealer's hands for a new round
    player.hands = [[]]
    player.bets = [0]
    player.current_hand_index = 0
    dealer.hand = []

    # Check if the deck needs to be reshuffled
    if deck.shoe == True:
        deck.create_deck()

def end_game(player, dealer, deck):
    print(f"Your current balance is ${player.balance}.\n")
    if player.balance <= 0:
        print("You have run out of money! Game over.\n")
        quit()
    else:
        play_again = input("Do you want to play another round? (y/n): ")
        if play_again.lower() == 'y':
            new_round(player, dealer, deck)
            decisions(player, dealer, deck)
        else:
            print("Thanks for playing! Goodbye.\n")
            quit()

# Main start of the blackjack game
def blackjackGamePlay():
    print("Welcome to Blackjack!")


    #Display the instructions for the game
    #instructions()
   

    #Setup the game
    decks = input("Enter the amount of decks you want to play with (1-8): ")
    if decks.isdigit() and 1 <= int(decks) <= 8:
        deck_num = int(decks)
    else:
        print("Invalid input. Defaulting to 6 decks.")
        deck_num = 6
    money = input("Enter the amount of money you want to start with(Whole positive number): ")
    if money.isdigit() and int(money) > 0:
        balance = int(money)
    else:
        print("Invalid input. Defaulting to $1000.")
        balance = 1000

    
    player = classes.Player(balance, playing=True)
    dealer = classes.Dealer()
    deck = classes.Deck(deck_num)
    decisions(player, dealer, deck)

    