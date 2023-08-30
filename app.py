from configs.app_config import PAGE_TITLE, PAGE_NAME
from configs.input_config import DEFAULT_PLAYER_NAME, NAME_DICT, CAPITAL_DICT
from configs.output_config import CAPITAL_DISPLAY, INFO_SCOPE, DEALER_SCOPE
from configs.game_config import MIN_BET
from widgets.outputs import set_title, write_text, clear_contents
from widgets.inputs import get_info, get_hands, get_choice
from game import BlackjackGame
from pywebio.platform import config


class Application:
    """Blackjack app."""

    def __init__(self):
        self.name, self.capital, self.game = DEFAULT_PLAYER_NAME, 0, BlackjackGame()
        config(title=PAGE_NAME)  # Set page name.

    def execute(self):  # The execute attribute is put into start_server of main.py.
        set_title(r"""<h1 align='center'><strong>""" + PAGE_TITLE + """</strong></h1>""")  # Page title.

        info_dict = get_info()
        if len(info_dict[NAME_DICT['name']].strip()) > 0:  # If player enters non-empty name.
            self.name = info_dict[NAME_DICT['name']].lstrip().rstrip()  # Keep middle spaces.
        self.capital = info_dict[CAPITAL_DICT['name']]

        write_text('Dear ' + self.name + CAPITAL_DISPLAY + str(self.capital) + ' dollars.', INFO_SCOPE, True)

        while self.capital >= MIN_BET:  # While remaining capital is enough for another round.
            hands = get_hands()
            self.game.set_up(hands, self.capital)

            choice = get_choice()
            clear_contents(DEALER_SCOPE)  # Right after choice is made, clear dealer scope.
            if choice == 'exit':  # If player selects exit, break while.
                break
