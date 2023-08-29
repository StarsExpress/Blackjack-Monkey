from configs.game_config import MIN_BET, MAX_BET
from configs.input_config import CHIPS_DICT
from configs.output_config import CHIPS_SCOPE
from utils.input_validity import check_chips
from machines.shuffle_machine import ShuffleMachine
from roles.dealer import Dealer
from pywebio.input import input, NUMBER
from pywebio.output import put_text, use_scope, clear
import time


class BlackjackGame:
    """Blackjack game."""

    def __init__(self):
        self.machine, self.dealer, self.capital = ShuffleMachine(), Dealer(), 0

    def set_up(self, head_hands, capital):  # Set up capital amount and shuffle machine before each round.
        self.capital = capital  # Remaining capital amount.
        self.machine.load_and_shuffle()  # Load and shuffle cards.

        # chips_list = []  # List of chips for each hand.
        # chips_dict = CHIPS_DICT
        #
        # for i in range(head_hands):  # Iterate through all wanted head hands.
        #     if self.capital < MIN_BET:  # If remaining capital isn't enough for another head hand, break for loop.
        #         inadequate_message = 'Your remaining capital ' + self.capital + ' < minimum bet ' + str(MIN_BET) + '.'
        #         put_text(inadequate_message, scope=CHIPS_SCOPE)
        #         break
        #
        #     chips_dict.update({'label': CHIPS_DICT['label'] + str(i + 1) + ':'})
        #     chips_dict.update({'holder': CHIPS_DICT['label'] + str(min(self.capital, MAX_BET)) + ':'})
        #
        #     with use_scope(CHIPS_SCOPE):
        #         chips = input(label=chips_dict['label'], name=chips_dict['name'], type=NUMBER, required=True,
        #                       validate=check_chips(remaining_capital=self.capital), placeholder=chips_dict['holder'])
        #     print(chips)
        #     self.capital -= chips  # Deduct chips amount from capital.
        #     chips_list.append(chips)  # Append chips to list.
        #
        # time.sleep(3)  # Sleep for 3 seconds.
        # clear(CHIPS_SCOPE)  # Right after choice is made, clear chips' scope.
        # print(chips_list)

        self.dealer.prepare(self.machine.draw())  # Dealer and player preparations.
        self.dealer.add_to_17_plus(self.machine)
