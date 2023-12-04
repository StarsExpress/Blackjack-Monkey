from configs.app_config import GAME_END_SLEEP
from configs.input_config import NAME_DICT, CAPITAL_DICT
from configs.output_config import DEALER_SCOPE, PLAYER_SCOPE, INCOME_SUB_SCOPES
from configs.rules_config import MIN_BET
from widgets.layouts import set_name_and_theme, set_core_layouts_width, set_top_layouts
from widgets.layouts import set_core_layouts, clear_contents, remove_scopes
from widgets.rules import show_rules
from widgets.income import show_income
from widgets.interactions import get_info, get_hands, get_choice
from widgets.notifications import update_cumulated_capital, notify_inadequate_capital, send_congrats
from blackjack import Blackjack
import time


class Application:
    """Blackjack app."""

    def __init__(self):
        self.blackjack, self.capital, self.income_list = Blackjack(), 0, []
        set_name_and_theme()

    def execute(self):  # This attribute is put into start_server of main.py.
        set_top_layouts()
        show_rules()
        self.income_list.clear()  # After page refreshing, income list reverts to emptiness.
        show_income(self.income_list)

        player_name = None
        info_dict = get_info()
        if len(info_dict[NAME_DICT['name']].strip()) > 0:  # If player enters non-empty name.
            player_name = info_dict[NAME_DICT['name']].lstrip().rstrip()  # Keep middle spaces.

        self.capital = info_dict[CAPITAL_DICT['name']]
        update_cumulated_capital(player_name, self.capital)

        set_core_layouts_width()  # Must set layouts' width before content.
        set_core_layouts()

        round_number = 1
        while self.capital >= MIN_BET:  # While remaining capital is enough for another round.
            hands = get_hands()
            self.blackjack.set_up(hands, self.capital, player_name)
            bets_placed = self.blackjack.start()

            profit = self.blackjack.capital - self.capital  # This round's profit.
            send_congrats(profit, bets_placed)
            self.capital += profit  # Update remaining capital.
            self.income_list += [dict(zip(INCOME_SUB_SCOPES['columns'], [round_number, profit, self.capital]))]

            if self.capital < MIN_BET:
                time.sleep(GAME_END_SLEEP)
                notify_inadequate_capital(self.capital, broke=True)
                break

            choice = get_choice()  # Right after choice is made, clear player and dealer scope.
            clear_contents([PLAYER_SCOPE, DEALER_SCOPE])
            if choice == 'exit':  # If player selects exit.
                remove_scopes([PLAYER_SCOPE, DEALER_SCOPE])
                break

            round_number += 1
