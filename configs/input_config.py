"""All input configurations."""

from configs.game_config import MIN_BET, MAX_CAPITAL

# Input widgets settings.
MAX_NAME_LEN = 20  # Maximal player name length.
DEFAULT_PLAYER_NAME = '💸 Benji Bucket 🪣'  # If player doesn't enter name.

# Player name widget dictionary.
NAME_DICT = {'label': '😃 How may we call you, Sir/Madame:', 'name': 'name',
             'holder': "Would like to know your name, or we'll call you " + DEFAULT_PLAYER_NAME,
             }

# Initial capital widget dictionary.
CAPITAL_DICT = {'label': '💰 Cash in your capital, please:', 'name': 'capital',
                'holder': str(MIN_BET) + ' <= capital <= ' + str(MAX_CAPITAL),
                }

# Each round's hand widget dictionary.
HANDS_DICT = {'label': 'How many hands do you want', 'min': 1, 'max': 6}

# Chips widget dictionary.
CHIPS_DICT = {'label': '💰 Put your chips for hand ', 'name': 'chips',
              'holder': str(MIN_BET) + ' <= chips <= ',
              'actions': [{'label': 'Enter', 'value': 'enter', 'type': 'submit', 'color': 'primary'},
                          {'label': 'Reset', 'value': 'reset', 'type': 'reset', 'color': 'secondary'}
                          ]
              }

# Continue and exit widget dictionary.
CHOICES_DICT = {'label': 'Want another round?',
                'actions': [{'label': 'Continue', 'value': 'continue', 'type': 'submit', 'color': 'primary'},
                            {'label': 'Exit', 'value': 'exit', 'type': 'submit', 'color': 'danger'}
                            ]
                }
