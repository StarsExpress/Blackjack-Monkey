"""All app configurations."""

import os

APP_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Where python files are stored.
RULES_PATHS_DICT = {'english': os.path.join(APP_BASE_PATH, 'rules', 'english.txt')}


PORT = 1998  # Server port.


PAGE_NAME = "🎰Job's Here"
PAGE_THEME = 'sketchy'
PAGE_TITLE = "♠️♥️Jack's Online Blackjack♦️♣️"


DEALER_SLEEP = 1  # Sleep: pause before next line of code.
EARLY_EXIT_SLEEP = 2
GAME_END_SLEEP = 2
