from configs.app_config import GAME_END_SLEEP
from configs.input_config import NAME_DICT, CAPITAL_DICT
from configs.output_config import DEALER_SCOPE, PLAYER_SCOPE, INCOME_SUB_SCOPES
from configs.rules_config import MIN_BET
from widgets.layouts import set_name_and_theme, set_core_layouts_width, set_top_layouts
from widgets.layouts import set_core_layouts, clear_contents
from widgets.intro import show_intro
from widgets.rules import show_rules
from widgets.income import show_income
from widgets.interactions import get_info, get_hands, get_choice
from widgets.notifications import update_cumulated_capital, notify_inadequate_capital, send_congrats
from blackjack import Blackjack
import time
from pywebio import session


class Application:
    """
    A class to serve as Blackjack application.

    Attributes:
        blackjack (Blackjack): instance of Blackjack class.
        capital (int): player's current capital.
        incomes (list): list of dictionaries, each representing a round's income.

    Methods:
        __init__(): initialize Application instance.
        execute(): execute Blackjack application.
    """

    def __init__(self):
        """Initialize Application instance. Set name, theme and attributes of instance."""
        self.blackjack, self.capital, self.incomes = Blackjack(), 0, []
        set_name_and_theme()

    def execute(self):
        """
        Execute Blackjack application. This method is put into start_server of main.py.

        After each round, it calculates profit, updates capital, and traces income.

        If capital is not enough for another round, it notifies player and breaks loop.

        If player chooses to start over, it clears contents and starts a new session.
        """
        set_top_layouts()
        show_intro()
        show_rules()
        self.incomes.clear()  # After page refreshing, incomes revert to emptiness.
        show_income(self.incomes)

        player_name = None
        info_dict = get_info()
        if len(info_dict[NAME_DICT["name"]].strip()) > 0:
            player_name = info_dict[NAME_DICT['name']].lstrip().rstrip()  # Keep middle spaces.

        self.capital = info_dict[CAPITAL_DICT["name"]]
        update_cumulated_capital(player_name, self.capital)

        set_core_layouts_width()  # Must set layouts' width before content.
        set_core_layouts()

        round_num = 1
        while self.capital >= MIN_BET:  # Remaining capital is enough for another round.
            hands = get_hands()
            self.blackjack.set_up(hands, self.capital, player_name)
            bets_placed = self.blackjack.start()

            profit = self.blackjack.capital - self.capital  # This round's profit.
            send_congrats(profit, bets_placed)
            self.capital += profit  # Update remaining capital.
            self.incomes += [
                dict(
                    zip(INCOME_SUB_SCOPES["columns"], [round_num, profit, self.capital])
                )
            ]

            if self.capital < MIN_BET:
                time.sleep(GAME_END_SLEEP)
                notify_inadequate_capital(self.capital, broke=True)
                break

            choice = get_choice()
            clear_contents([PLAYER_SCOPE, DEALER_SCOPE])
            if choice == "start_over":
                session.go_app("main", new_window=False)

            round_num += 1
