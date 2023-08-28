"""All input configurations."""

from configs.game_config import MIN_BET, MAX_CAPITAL

# Input widgets settings.
MARKDOWN = 'No Hole Card Blackjack'
MAX_NAME_LEN = 20  # Maximal player name length.
DEFAULT_NAME = 'BENJI Bucket'  # If player doesn't enter name.

# Player name widget dictionary.
NAME_DICT = {'label': 'How should we call you', 'name': 'name',

             'holder': 'Would like to know your name',

             'actions': [{'label': 'Enter', 'type': 'submit', 'value': 'enter'},
                         {'label': 'Reset', 'type': 'reset', 'color': 'warning'}]}

# Initial capital widget dictionary.
CAPITAL_DICT = {'label': 'Cash in your money, please', 'name': 'capital',

                'holder': str(MIN_BET) + ' <= capital <= ' + str(MAX_CAPITAL) + '',

                'actions': [{'label': 'Enter', 'type': 'submit', 'value': 'enter'},
                            {'label': 'Reset', 'type': 'reset', 'color': 'warning'}]}

# Each round's hand widget dictionary.
HANDS_DICT = {'label': 'How many hands do you want in this round', 'min': 1, 'max': 6}
