from configs.app_config import PAGE_TITLE, PAGE_NAME
from configs.input_config import DEFAULT_PLAYER_NAME, NAME_DICT, CAPITAL_DICT, HANDS_DICT, CHOICES_DICT
from configs.output_config import CAPITAL_DISPLAY, INFO_SCOPE, HANDS_SCOPE, DEALER_SCOPE
from configs.game_config import MIN_BET
from utils.input_validity import check_name, check_capital
from game import BlackjackGame
from pywebio.platform import config
from pywebio.input import input_group, input, TEXT, NUMBER, slider, actions
from pywebio.output import put_html, use_scope, put_text, clear


class Application:
    """Blackjack app."""

    def __init__(self):
        self.name, self.capital, self.game = DEFAULT_PLAYER_NAME, 0, BlackjackGame()
        config(title=PAGE_NAME)  # Set page name.

    def execute(self, chips_dict=None):  # The execute attribute is put into start_server of main.py.
        put_html(r"""<h1 align='center'><strong>""" + PAGE_TITLE + """</strong></h1>""")  # Page title.

        info_dict = input_group(inputs=[
            input(label=NAME_DICT['label'], name=NAME_DICT['name'], type=TEXT,
                  validate=check_name, placeholder=NAME_DICT['holder']),

            input(label=CAPITAL_DICT['label'], name=CAPITAL_DICT['name'], type=NUMBER, required=True,
                  validate=check_capital, placeholder=CAPITAL_DICT['holder'])
        ])  # Initial capital is a required input.

        if len(info_dict[NAME_DICT['name']].strip()) > 0:  # If player enters non-empty name.
            self.name = info_dict[NAME_DICT['name']].lstrip().rstrip()  # Keep middle spaces.
        self.capital = info_dict[CAPITAL_DICT['name']]

        put_text('Dear ' + self.name + CAPITAL_DISPLAY + str(self.capital) + ' dollars', scope=INFO_SCOPE)

        while self.capital >= MIN_BET:  # While remaining capital is enough for another round.
            with use_scope(name=HANDS_SCOPE, clear=True):
                hands = slider(HANDS_DICT['label'], min_value=HANDS_DICT['min'], max_value=HANDS_DICT['max'])

            self.game.set_up(hands, self.capital)

            choice = actions(CHOICES_DICT['label'], buttons=CHOICES_DICT['actions'])
            clear(DEALER_SCOPE)  # Right after choice is made, clear dealer's scope.
            if choice == 'exit':  # If player selects exit, break while.
                break
