from config import MINIMUM_BET, MAXIMUM_CAPITAL, INITIAL_HANDS_MAXIMUM
from utils.displayer import show_app_invalid_input
from colors import Colors
from game import BlackjackGame


class Application:
    """Blackjack app."""

    def __init__(self):
        while True:  # Make sure input capital is valid.
            initial_capital = str(input('Please enter your capital: '))  # Enter initial capital.
            if initial_capital.strip().isdigit() is False:  # If stripped input isn't integer, continue while.
                show_app_invalid_input(not_digit=True)
                continue
            if int(initial_capital) < MINIMUM_BET:  # If amount < minimum bet, continue while.
                show_app_invalid_input(below_minimum=True)
                continue
            if int(initial_capital) > MAXIMUM_CAPITAL:  # If amount > maximum capital, continue while.
                show_app_invalid_input(over_maximum=True)
                continue
            break  # After passing both tests, break while loop.

        initial_capital = int(initial_capital.strip())  # Turn stripped string to integer.
        self.capital, self.profit = initial_capital, 0  # Save initial capital to property. Profit starts from 0.
        print('Your total capital is ' + str(initial_capital) + ' dollars.\n')
        self.game = BlackjackGame()  # Store game object to property.

    def execute(self):  # Execute app.
        while self.capital >= MINIMUM_BET:  # While remaining capital is enough for another round.
            while True:  # Make sure input head hands are valid.
                head_hands = str(input('How many hands do you want: '))  # Enter head hands.
                if head_hands.strip().isdigit() is False:  # If stripped input isn't integer, continue while.
                    show_app_invalid_input(not_digit=True)
                    continue
                # If input not in 1 to 6, continue while.
                if (int(head_hands) < 1) | (int(head_hands) > INITIAL_HANDS_MAXIMUM):
                    show_app_invalid_input(invalid_hands=True)
                    continue
                break  # After passing both tests, break while loop.

            print('\n')  # Print a space line.
            head_hands = int(head_hands.strip())  # Turn stripped string to integer.
            self.game.set_up(head_hands, self.capital)  # Prepare for a new round.
            self.game.start()  # Start a new round.

            profit = self.game.capital - self.capital  # Calculate this round's profit and make notes.
            profit_note = 'profit is ' + str(profit) if profit >= 0 else 'loss is ' + str(profit)
            profit_color = Colors.red if profit >= 0 else Colors.green  # Set text color.
            self.profit += profit  # Update this round's profit into cumulated profit.
            print(profit_color + 'This round' + "'" + 's ' + profit_note + ' dollars.' + Colors.default)

            self.capital = self.game.capital  # Update remaining capital amount and cumulated profit. Make notes.
            total_profit_note = 'profit is ' + str(self.profit) if self.profit >= 0 else 'loss is ' + str(self.profit)
            total_profit_color = Colors.red if self.profit >= 0 else Colors.green  # Set text color.
            print(total_profit_color + 'Your cumulated ' + total_profit_note + ' dollars.' + Colors.default + '\n' +
                  total_profit_color + 'Remaining capital is ' + str(self.capital) + ' dollars.' + Colors.default, '\n')

            if self.capital < MINIMUM_BET:  # If remaining capital < minimum bet, break while loop.
                show_app_invalid_input(remaining_capital=self.capital, get_broke=True)
                break

            while True:  # Make sure valid choice is selected.
                choice = str(input('\nDo you want to keep playing? 1. Yes 2. No ')).strip()  # Choose to play or leave.
                if choice not in ['1', '2']:  # If invalid choice is selected, continue while.
                    show_app_invalid_input(invalid_choice=True)
                    continue
                break  # If valid choice is selected, break while loop.

            win_emoji = '☆ *:.｡.o(≧▽≦)o.｡.: * ☆' if self.profit > 0 else ''  # Add emoji if cumulated profit > 0.
            if choice == '2':  # If chooses to leave the game.
                print('\nThank you for playing. See you next time~\n' + Colors.red + win_emoji + Colors.default + '\n')
                break


if __name__ == '__main__':
    app = Application()
    app.execute()
