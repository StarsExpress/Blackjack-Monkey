from configs.rules_config import MIN_BET, MAX_BET
from configs.input_config import CHIPS_DICT
from utils.reminders import remind_betting_amount
from widgets.inputs import get_chips
from widgets.outputs import notify_inadequate_capital
from machines.shuffle_machine import ShuffleMachine
from roles.dealer import Dealer
from roles.player import Player


class BlackjackGame:
    """Blackjack game."""

    def __init__(self):
        self.machine, self.dealer, self.player, self.capital = ShuffleMachine(), Dealer(), Player(), 0

    def check_chips(self, chips):  # Check if placed bets are valid.
        # PyWebIO's input validation function only accepts one argument.
        # This function is defined here to receive self.capital as a self-updating global variable.
        if chips < MIN_BET:
            return 'Placed chips must >= minimum bet ' + str(MIN_BET) + '.'
        if chips > MAX_BET:
            return 'Placed chips must <= maximum bet ' + str(MAX_BET) + '.'
        if chips > self.capital:
            return 'Placed chips must <= remaining capital ' + str(self.capital) + '.'
        if chips % 100 != 0:
            return 'Placed chips must be in units of 100.'

    def set_up(self, head_hands, capital):  # Set up capital amount and shuffle machine before each round.
        self.capital = capital  # Remaining capital amount.
        self.machine.load_and_shuffle()  # Load and shuffle cards.

        chips_list = []  # List of chips for each hand.
        chips_dict = CHIPS_DICT.copy()  # Make a copy from config every time.

        for i in range(head_hands):  # Iterate through all wanted head hands.
            if self.capital < MIN_BET:  # If remaining capital isn't enough for another head hand.
                notify_inadequate_capital(self.capital, hands=True)
                break

            # Update label with respect to iterated hand ordinal for displays.
            chips_dict.update({'label': CHIPS_DICT['label'] + str(i + 1) + ':'})
            # Update holder text with respect to remaining capital for maximal feasible bet.
            chips_dict.update({'holder': CHIPS_DICT['holder'] + remind_betting_amount(self.capital)})

            chips = get_chips(chips_dict, self.check_chips)  # Pass validation function check_chips.
            self.capital -= chips  # Deduct chips amount from capital.
            chips_list.append(chips)

        self.dealer.prepare(self.machine.draw())  # Dealer and player preparations.
        self.player.prepare(chips_list, [list(self.machine.draw(True)) for _ in range(len(chips_list))])
        self.dealer.add_to_17_plus(self.machine)
