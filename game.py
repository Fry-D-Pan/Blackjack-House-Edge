import tkinter as tk
from tkinter import messagebox
import random

class BlackjackGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack")

        # Initialize game variables
        self.deck = self.create_deck()
        self.shuffle_point = int(len(self.deck) * 0.8)
        self.player_hand = []
        self.dealer_hand = []
        self.split_hand = None
        self.current_hand = "player"
        self.balance = 0
        self.bet = 0

        # Ask for initial balance
        self.ask_balance()

        # GUI setup
        self.balance_label = tk.Label(master, text=f"Balance: ${self.balance}")
        self.balance_label.pack()
        
        self.bet_label = tk.Label(master, text="Bet: $0")
        self.bet_label.pack()

        self.bet_entry = tk.Entry(master)
        self.bet_entry.pack()

        self.bet_button = tk.Button(master, text="Place Bet", command=self.place_bet)
        self.bet_button.pack()

        self.player_label = tk.Label(master, text="Player's Hand: []")
        self.player_label.pack()

        self.split_label = tk.Label(master, text="Split Hand: []")
        self.split_label.pack()

        self.dealer_label = tk.Label(master, text="Dealer's Hand: []")
        self.dealer_label.pack()

        self.action_frame = tk.Frame(master)
        self.action_frame.pack()

        self.hit_button = tk.Button(self.action_frame, text="Hit", command=self.hit, state=tk.DISABLED)
        self.hit_button.grid(row=0, column=0)

        self.stand_button = tk.Button(self.action_frame, text="Stand", command=self.stand, state=tk.DISABLED)
        self.stand_button.grid(row=0, column=1)

        self.split_button = tk.Button(self.action_frame, text="Split", command=self.split, state=tk.DISABLED)
        self.split_button.grid(row=0, column=2)

        self.double_button = tk.Button(self.action_frame, text="Double", command=self.double, state=tk.DISABLED)
        self.double_button.grid(row=0, column=3)

    def ask_balance(self):
        def set_balance():
            try:
                balance = int(balance_entry.get())
                if balance <= 0:
                    raise ValueError
                self.balance = balance
                balance_window.destroy()
            except ValueError:
                messagebox.showerror("Invalid Balance", "Please enter a valid starting balance.")

        balance_window = tk.Toplevel(self.master)
        balance_window.title("Set Starting Balance")

        tk.Label(balance_window, text="Enter your starting balance:").pack()
        balance_entry = tk.Entry(balance_window)
        balance_entry.pack()

        tk.Button(balance_window, text="Set Balance", command=set_balance).pack()

        self.master.wait_window(balance_window)

    def create_deck(self):
        deck = []
        for _ in range(6):  # 6 decks
            for value in range(1, 14):
                for _ in range(4):  # 4 suits
                    if value == 11:
                        deck.append("J")
                    elif value == 12:
                        deck.append("Q")
                    elif value == 13:
                        deck.append("K")
                    else:
                        deck.append(value)
        random.shuffle(deck)
        return deck

    def shuffle_deck(self):
        self.deck = self.create_deck()

    def start_game(self):
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.split_hand = None
        self.current_hand = "player"

        if len(self.deck) < self.shuffle_point:
            self.shuffle_deck()

        self.deal_cards()
        self.check_blackjack()

    def deal_cards(self):
        self.player_hand.append(self.deck.pop())
        self.dealer_hand.append(self.deck.pop())
        self.player_hand.append(self.deck.pop())
        self.dealer_hand.append(self.deck.pop())

    def update_labels(self):
        self.player_label.config(text=f"Player's Hand: {self.player_hand} ({self.calculate_hand_value(self.player_hand)})")
        if self.split_hand:
            self.split_label.config(text=f"Split Hand: {self.split_hand} ({self.calculate_hand_value(self.split_hand)})")
        else:
            self.split_label.config(text="Split Hand: []")
        self.dealer_label.config(text=f"Dealer's Hand: [{self.dealer_hand[0]}, ?]")
        self.balance_label.config(text=f"Balance: ${self.balance}")
        self.bet_label.config(text=f"Bet: ${self.bet}")

    def calculate_hand_value(self, hand):
        value = 0
        aces = 0
        for card in hand:
            if card in ("J", "Q", "K"):
                value += 10
            elif card == 1:
                aces += 1
                value += 11
            else:
                value += card

        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    def enable_actions(self):
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.double_button.config(state=tk.NORMAL)
        self.split_button.config(state=tk.NORMAL if self.player_hand[0] == self.player_hand[1] else tk.DISABLED)

    def disable_actions(self):
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.double_button.config(state=tk.DISABLED)
        self.split_button.config(state=tk.DISABLED)

    def place_bet(self):
        try:
            bet = int(self.bet_entry.get())
            if bet > self.balance or bet <= 0:
                raise ValueError
            self.bet = bet
            self.balance -= self.bet
            self.start_game()
        except ValueError:
            messagebox.showerror("Invalid Bet", "Please enter a valid bet amount.")

    def hit(self):
        hand = self.split_hand if self.current_hand == "split" else self.player_hand
        hand.append(self.deck.pop())
        self.update_labels()

        if self.calculate_hand_value(hand) > 21:
            self.end_turn()

    def stand(self):
        self.end_turn()

    def split(self):
        self.split_hand = [self.player_hand.pop()]
        self.player_hand.append(self.deck.pop())
        self.split_hand.append(self.deck.pop())
        self.update_labels()
        self.enable_actions()

    def double(self):
        self.balance -= self.bet
        self.bet *= 2
        self.hit()
        self.stand()

    def dealer_turn(self):
        while self.calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())

    def check_blackjack(self):
        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)

        if dealer_value == 21:
            self.dealer_label.config(text=f"Dealer's Hand: {self.dealer_hand} ({dealer_value})")
            messagebox.showinfo("Blackjack!", "Dealer has blackjack! Dealer wins.")
            self.start_game()
        elif player_value == 21:
            self.balance += int(self.bet * 2.5)
            self.dealer_label.config(text=f"Dealer's Hand: {self.dealer_hand} ({dealer_value})")
            messagebox.showinfo("Blackjack!", "Player has blackjack! Player wins with a 3:2 payout.")
            self.start_game()
        else:
            self.update_labels()
            self.enable_actions()

    def end_turn(self):
        if self.current_hand == "player" and self.split_hand:
            self.current_hand = "split"
        else:
            self.dealer_turn()
            self.determine_winner()

    def determine_winner(self):
        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        split_value = self.calculate_hand_value(self.split_hand) if self.split_hand else None

        result = ""

        if player_value > 21:
            result = "Player busts! Dealer wins."
        elif dealer_value > 21 or player_value > dealer_value:
            self.balance += self.bet * 2
            result = "Player wins!"
        elif player_value == dealer_value:
            self.balance += self.bet
            result = "Push!"
        else:
            result = "Dealer wins!"

        if self.split_hand:
            if split_value > 21:
                result += "\nSplit hand busts! Dealer wins."
            elif dealer_value > 21 or split_value > dealer_value:
                self.balance += self.bet * 2
                result += "\nSplit hand wins!"
            elif split_value == dealer_value:
                self.balance += self.bet
                result += "\nSplit hand pushes."
            else:
                result += "\nDealer wins against split hand."

        final_results = (
            f"Player's Hand: {self.player_hand} ({player_value})\n"
            f"Dealer's Hand: {self.dealer_hand} ({dealer_value})"
        )
        if self.split_hand:
            final_results += f"\nSplit Hand: {self.split_hand} ({split_value})"

        messagebox.showinfo("Game Over", f"{result}\n\n{final_results}")
        self.start_game()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGame(root)
    root.mainloop()
