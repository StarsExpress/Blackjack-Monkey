from configs.app_config import PAGE_TITLE, GAME_END_SLEEP
from configs.input_config import NAME_DICT, CAPITAL_DICT
from configs.output_config import DEALER_SCOPE, PLAYER_SCOPE
from configs.rules_config import MIN_BET
from widgets.rules import show_rules
from widgets.layouts import configure_name, set_title, set_core_layouts, clear_contents, remove_scopes
from widgets.interactions import get_info, get_hands, get_choice
from widgets.notifications import update_cumulated_capital, notify_inadequate_capital, send_congrats
from blackjack import Blackjack
import time


class Application:
    """Blackjack app."""

    def __init__(self):
        self.blackjack, self.capital, self.profit = Blackjack(), 0, 0
        configure_name()

    def execute(self):  # The execute attribute is put into start_server of main.py.
        show_rules()
        set_title(r"""<h1 align='center'><strong>""" + PAGE_TITLE + """</strong></h1>""")

        player_name = None
        info_dict = get_info()
        if len(info_dict[NAME_DICT['name']].strip()) > 0:  # If player enters non-empty name.
            player_name = info_dict[NAME_DICT['name']].lstrip().rstrip()  # Keep middle spaces.
        self.capital = info_dict[CAPITAL_DICT['name']]

        update_cumulated_capital(player_name, self.capital)
        set_core_layouts()

        while self.capital >= MIN_BET:  # While remaining capital is enough for another round.
            hands = get_hands()
            self.blackjack.set_up(hands, self.capital, player_name)
            bets_placed = self.blackjack.start()

            profit = self.blackjack.capital - self.capital  # This round's profit.
            send_congrats(profit, bets_placed)
            self.profit += profit  # Update cumulated profit.
            self.capital += profit  # Update remaining capital.

            if self.capital < MIN_BET:
                time.sleep(GAME_END_SLEEP)
                notify_inadequate_capital(self.capital, broke=True)
                break

            choice = get_choice()  # Right after choice is made, clear player and dealer scope.
            clear_contents([PLAYER_SCOPE, DEALER_SCOPE])
            if choice == 'exit':  # If player selects exit.
                remove_scopes([PLAYER_SCOPE, DEALER_SCOPE])
                break
