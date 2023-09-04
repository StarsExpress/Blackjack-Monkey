from configs.app_config import PAGE_TITLE, GAME_END_SLEEP
from configs.input_config import DEFAULT_PLAYER_NAME, NAME_DICT, CAPITAL_DICT
from configs.output_config import CAPITAL_TEXT, INFO_SCOPE, DEALER_SCOPE, PLAYER_SCOPE
from configs.rules_config import MIN_BET
from widgets.layouts import configure_name, set_title, set_core_layouts, write_text, clear_contents
from widgets.interactions import get_info, get_hands, get_choice
from widgets.notifications import notify_inadequate_capital
from game import BlackjackGame
import time


class Application:
    """Blackjack app."""

    def __init__(self):
        self.game, self.name, self.capital, self.profit = BlackjackGame(), DEFAULT_PLAYER_NAME, 0, 0
        configure_name()

    def execute(self):  # The execute attribute is put into start_server of main.py.
        set_title(r"""<h1 align='center'><strong>""" + PAGE_TITLE + """</strong></h1>""")  # Page title.

        info_dict = get_info()
        if len(info_dict[NAME_DICT['name']].strip()) > 0:  # If player enters non-empty name.
            self.name = info_dict[NAME_DICT['name']].lstrip().rstrip()  # Keep middle spaces.
        self.capital = info_dict[CAPITAL_DICT['name']]

        write_text('Dear ' + self.name + CAPITAL_TEXT + str(self.capital) + ' dollars.', INFO_SCOPE, True)

        set_core_layouts()  # Establish core scopes.

        while self.capital >= MIN_BET:  # While remaining capital is enough for another round.
            hands = get_hands()
            self.game.set_up(hands, self.capital)
            self.game.start()

            profit = self.game.capital - self.capital  # Calculate this round's profit
            self.profit += profit  # Update cumulated profit.
            self.capital += profit  # Update remaining capital.

            if self.capital < MIN_BET:  # If remaining capital < minimum bet.
                time.sleep(GAME_END_SLEEP)  # Pause for a moment.
                notify_inadequate_capital(self.capital, broke=True)  # Send notification.
                break

            choice = get_choice()  # Right after choice is made, clear player and dealer scope.
            clear_contents([PLAYER_SCOPE, DEALER_SCOPE])
            if choice == 'exit':  # If player selects exit.
                break
