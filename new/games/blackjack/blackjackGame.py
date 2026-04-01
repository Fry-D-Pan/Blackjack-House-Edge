from . import blackjackClasses


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
        while True:
            bet = input("Enter amount to bet: ")
            if bet.isdigit() and int(bet) > 0 and int(bet) <= player.balance:
                player.bet = int(bet)
                player.balance -= player.bet
                print(f"You bet ${player.bet}. Your current balance is ${player.balance}.\n")
                break
            else:
                print("Invalid bet amount. Please enter a positive number that does not exceed your current balance.")
    else:
        # Set bet for simulation strategies
        player.bet = 10  # Fixed bet for all strategies
        player.balance -= player.bet  # Deduct bet from balance
    
    # Deals the initial cards to the player and dealer
    deck.deal_cards(player.hands[0])
    deck.deal_cards(dealer.hand)
    if not check_blackjack(dealer, player):
        play_all_hands(player, dealer, deck)
    # If blackjack detected, round ends (stats already tracked in check_blackjack)

def play_all_hands(player, dealer, deck):
    #Plays through all player hands sequentially before dealer's turn
    hand_index = 0
    while hand_index < len(player.hands):
        player.current_hand_index = hand_index
        play_hand(player, dealer, deck, hand_index)
        hand_index += 1
    
    # All hands complete - now dealer's turn
    if player.playing == True:
        blackjackClasses.clear_terminal()
    print("=== All hands complete. Dealer's turn ===")
    dealer_play(dealer, player, deck)
    get_results(player, dealer, deck)


def play_hand(player, dealer, deck, hand_index):
    #Plays a single hand to completion
    current_hand = player.hands[hand_index]
    current_bet = player.bets[hand_index]
    hand_value = player.get_hand_value(hand_index)
    
    if player.playing == True:
        blackjackClasses.clear_terminal()
    
    # Display all hands if multiple exist
    if len(player.hands) > 1:
        print(f"\n=== Playing Hand {hand_index + 1} of {len(player.hands)} ===")
        for i, hand in enumerate(player.hands):
            status = " (CURRENT)" if i == hand_index else ""
            print(f"Hand {i + 1}: {hand} (Value: {player.get_hand_value(i)}, Bet: ${player.bets[i]}){status}")
    else:
        print(f"Your hand: {current_hand} (Value: {hand_value})")
    
    print(f"\nDealer's hand: [{dealer.hand[0]}, ('Hidden Card')] (Value: {blackjackClasses.get_hand_value([dealer.hand[0]])})\n")
    
    
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
        option = player.get_strategy_move(hand_index, dealer.hand[0])
        # Fallback if strategy suggests unavailable action
        if option == 'd' and not can_double:
            option = 'h'  # Hit instead of double
        elif option == 'p' and not can_split:
            option = 'h'  # Hit instead of split
    match option:
        case "1" | "h":  # Hit
            deck.deal_cards(current_hand)
            hand_value = player.get_hand_value(hand_index)
            if hand_value > 21:
                if player.playing == True:
                    print("Busted! Your hand value exceeded 21.\n")
                else:
                    print("Busted! Your hand value exceeded 21.")
                return
            play_hand(player, dealer, deck, hand_index)
        
        case "2" | "s":  # Stand
            if player.playing == True:
                print(f"You chose to stand on hand {hand_index + 1}.\n")
            else:
                print(f"You chose to stand on hand {hand_index + 1}.")
            return
        
        case "3" | "d":  # Double Down
            if can_double:
                player.balance -= current_bet
                player.bets[hand_index] *= 2
                deck.deal_cards(current_hand)
                new_value = player.get_hand_value(hand_index)
                if player.playing == True:
                    print(f"You doubled down. Hand: {current_hand} (Value: {new_value})\n")
                else:
                    print(f"You doubled down. Hand: {current_hand} (Value: {new_value})")
                if new_value > 21:
                    if player.playing == True:
                        print(f"Hand {hand_index + 1} busted!\n")
                    else:
                        print(f"Hand {hand_index + 1} busted!")
                return  # Double down = automatic stand
            else:
                if player.playing == True:
                    print("Cannot double down. Try again.\n")
                    play_hand(player, dealer, deck, hand_index)
                else:
                    # Simulation fallback already handled above
                    return
        
        case "4" | "p":  # Split
            if can_split:
                # Create new hand from split card
                split_card = current_hand.pop()
                player.hands.insert(hand_index + 1, [split_card])
                player.bets.insert(hand_index + 1, current_bet)
                player.balance -= current_bet
                
                # Deal one card to each hand
                deck.deal_cards(player.hands[hand_index])
                deck.deal_cards(player.hands[hand_index + 1])
                
                print(f"You split! Now playing hand {hand_index + 1}.")
                play_hand(player, dealer, deck, hand_index)
            else:
                if player.playing == True:
                    print("Cannot split. Try again.\n")
                    play_hand(player, dealer, deck, hand_index)
                else:
                    # Simulation fallback already handled above
                    return
        
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
    else:
        print("Dealer stands.\n")

def get_results(player, dealer, deck):
    for i, hand in enumerate(player.hands):
        hand_value = player.get_hand_value(i)
        print(f"Hand {i + 1}: {hand} (Value: {hand_value}, Bet: ${player.bets[i]})")
        print(f"Dealer's hand: {dealer.hand} (Value: {dealer.hand_value})\n")
        if hand_value > 21:
            print(f"Hand {i + 1} busted. You lose ${player.bets[i]}.\n")
            player.losses += 1
        elif dealer.hand_value > 21:
            print(f"Hand {i + 1} wins! (Dealer busted) You win ${player.bets[i] * 2}.\n")
            player.balance += player.bets[i] * 2
            player.wins += 1
        elif hand_value > dealer.hand_value:
            print(f"Hand {i + 1} wins! You win ${player.bets[i] * 2}.\n")
            player.balance += player.bets[i] * 2
            player.wins += 1
        elif hand_value == dealer.hand_value:
            print(f"Hand {i + 1} pushes. Your bet of ${player.bets[i]} is returned.\n")
            player.balance += player.bets[i]
            player.ties += 1
        else:
            print(f"Hand {i + 1} loses. You lose ${player.bets[i]}.\n")
            player.losses += 1
    
    # Only call end_game for manual player mode
    if player.playing == True:
        end_game(player, dealer, deck)

def check_blackjack(dealer, player):
    """Check for blackjacks and handle payouts. Returns True if blackjack detected."""
    player_blackjack = player.get_hand_value(0) == 21
    dealer_blackjack = dealer.hand_value == 21
    
    if player_blackjack and dealer_blackjack:
        print(f"Both player and dealer have Blackjack! Push.\n")
        player.balance += player.bet  # Return bet
        player.ties += 1
        return True
    elif player_blackjack:
        print(f"Congratulations! You have Blackjack with hand {player.hands[0]}! You win 1.5x your bet.\n")
        player.balance += int(player.bet * 2.5)  # Return original bet + 1.5x winnings
        player.wins += 1
        return True
    elif dealer_blackjack:
        print(f"Dealer has Blackjack with hand {dealer.hand}! You lose.\n")
        player.losses += 1
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
    player.rounds_played += 1  # Track completed rounds
    print(f"Your current balance is ${player.balance}.\n")
    if player.playing == True:
        # Manual player mode
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
    # Simulation mode - just reset for next round, main loop handles continuation


def print_simulation_summary(player):
    # Display final simulation statistics
    total_hands = player.wins + player.losses + player.ties
    
    print(f"Rounds played: {player.rounds_played}")
    print(f"Total hands: {total_hands}" + (f" (includes {total_hands - player.rounds_played} split hands)" if total_hands > player.rounds_played else ""))
    print(f"\nHand Results:")
    print(f"  Wins: {player.wins} ({player.wins/total_hands*100:.1f}%)")
    print(f"  Losses: {player.losses} ({player.losses/total_hands*100:.1f}%)")
    print(f"  Ties: {player.ties} ({player.ties/total_hands*100:.1f}%)")
    print(f"\nFinancial Results:")
    print(f"  Starting balance: ${player.starting_balance}")
    print(f"  Final balance: ${player.balance}")
    print(f"  Net result: ${player.balance - player.starting_balance:+d}")
    print(f"  ROI: {(player.balance - player.starting_balance) / player.starting_balance * 100:+.2f}%")
    
    # Calculate house edge (positive = house wins, negative = player wins)
    # Use rounds_played for base bet calculation (excludes double/split bets for simplicity)
    avg_bet = 10  # Fixed bet amount per round
    base_wagered = player.rounds_played * avg_bet
    house_edge_pct = ((player.starting_balance - player.balance) / base_wagered) * 100 if base_wagered > 0 else 0
    print(f"  Base amount wagered: ${base_wagered} ({player.rounds_played} rounds)")
    print(f"  House edge: {house_edge_pct:+.2f}% ({'House advantage' if house_edge_pct > 0 else 'Player advantage'})\n")
    


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

    
    player = blackjackClasses.Player(balance, playing=True, simulation_rounds=0, strategy="")
    dealer = blackjackClasses.Dealer()
    deck = blackjackClasses.Deck(deck_num)
    decisions(player, dealer, deck)



def blackjackGameSim():
    print("Welcome to Blackjack Simulation!")
    
    
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
    simulation_rounds = input("Enter the number of simulation rounds to run (Whole positive number): ")
    if simulation_rounds.isdigit() and int(simulation_rounds) > 0:
        simulation_rounds = int(simulation_rounds)
    else:
        print("Invalid input. Defaulting to 1000 rounds.")
        simulation_rounds = 1000
    
    strategy = input("Enter the strategy you want to use for the simulation \n 1)basic " \
    "\n 2)agressive(Hit until 15) \n 3)passive(Hit until 11) \n 4)dealer(Hit until 17) \n 5)random: ")
    if strategy == "1":
        strategy = "basic"
    elif strategy == "2":
        strategy = "aggressive"
    elif strategy == "3":
        strategy = "passive"
    elif strategy == "4":
        strategy = "dealer"
    elif strategy == "5":
        strategy = "random"
    else:
        print("Invalid input. Defaulting to basic strategy.")
        strategy = "basic"
    

    player = blackjackClasses.Player(balance, playing=False , simulation_rounds=simulation_rounds, strategy=strategy)
    dealer = blackjackClasses.Dealer()
    deck = blackjackClasses.Deck(deck_num)
    
    # Main simulation loop
    print(f"\nStarting simulation of {simulation_rounds} rounds using {strategy} strategy...\n")
    
    while player.current_round <= simulation_rounds and player.balance > 0:
        print(f"=== Round {player.current_round}/{simulation_rounds} ===")
        decisions(player, dealer, deck)
        player.rounds_played += 1  # Increment completed rounds
        print(f"Balance after round: ${player.balance}\n")
        new_round(player, dealer, deck)
        player.current_round += 1
    
    # Simulation complete - show results
    print("\n=== Simulation Complete! ===\n")
    if player.balance <= 0:
        print("Simulation ended early: Player went bankrupt.\n")
    print_simulation_summary(player)