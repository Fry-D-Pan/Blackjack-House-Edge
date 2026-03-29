from games.blackjack.blackjackGame import blackjackGamePlay
from new.games.blackjack.blackjackClasses import clear_terminal


#Options menu function
def options():
    #set variables for the options menu
    menuType = input("What would you like to do?\n 1. Play a game\n 2. See simulations\n 3. Exit\n")
    # handle's the game options
    if menuType == "1":
        print("You chose to play a game!")
        clear_terminal()
        gameMode = input("Enter what number game you want to play\n1) Blackjack\n2) Crapes\n3) Roulette\n4) Go back.\n")
        if gameMode == "1":
            clear_terminal()
            blackjackGamePlay()
        elif gameMode == "2":
            clear_terminal()
            #crapesGame()
            quit()
        elif gameMode == "3":
            clear_terminal()
            #rouletteGame()
            quit()
        elif gameMode == "4":
            print("Going back to the main menu...\n")
            input("Press Enter to continue...")
            clear_terminal()
            main()
        else:
            print("Invalid choice. Please try again.\n")
            input("Press Enter to continue...")
            clear_terminal()
            main()
    # handle's the simulation options
    elif menuType == "2":
        print("You chose to see simulations!")
        clear_terminal()
        simMode = input("Enter what number simulation you want to see\n1) Blackjack\n2) Crapes\n3) Roulette\n4) Go back.\n")
        if simMode == "1":
            clear_terminal()
            #blackjackSim()
            quit()
        elif simMode == "2":
            clear_terminal()
            #crapesSim()
            quit()
        elif simMode == "3":
            clear_terminal()
            #rouletteSim()
            quit()
        elif simMode == "4":
            input("Press Enter to continue...")
            clear_terminal()
            main()
        else:
            print("Invalid choice. Please try again.\n")
            input("Press Enter to continue...")
            clear_terminal()
            main()
    # handle's the exit option
    elif menuType == "3":
        print("See you next time! Goodbye!")
        quit()
    # handles invalid input
    else:
        print("Invalid choice. Please try again.\n")
        input("Press Enter to continue...")
        main()


#Welcome message
def main():
    clear_terminal()
    print("----------------------Welcome to Python Casino!----------------------")
    print("Here we let you try your luck and beat the casino!")
    print("You can also see what different simulations show you about the casino and how it works.")
    options()
if __name__ == "__main__":
    main()

