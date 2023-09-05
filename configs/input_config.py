"""All input configurations."""

from configs.rules_config import MIN_BET, MAX_CAPITAL

# Input widgets settings.
MAX_NAME_LEN = 20  # Maximal player name length.
DEFAULT_PLAYER_NAME = '💸Benji Bucket🪣'  # If player doesn't enter name.


# Player name widget dictionary.
NAME_DICT = {'label': '😃How may we call you, Sir/Madame:', 'name': 'name',
             'holder': "Would like to know your name, or we'll call you " + DEFAULT_PLAYER_NAME,
             }

# Initial capital widget dictionary.
CAPITAL_DICT = {'label': '💰Cash in your capital, please:', 'name': 'capital',
                'holder': 'Please be integer. Available range: ' + str(MIN_BET) + ' to ' + str(MAX_CAPITAL) + '.',
                }

# Each round's hand widget dictionary.
HANDS_DICT = {'label': 'How many hands do you want', 'min': 1, 'max': 6}


# Chips widget dictionary.
CHIPS_DICT = {'label': '💰Put your chips for hand ',
              'holder': 'Please be integer. Available range: ' + str(MIN_BET) + ' to '
              }

# Early pay widget dictionary.
EARLY_PAY_DICT = {'label': ': take early pay❓',
                  'options': [{'label': 'Wait', 'value': 'wait', 'type': 'submit', 'color': 'primary'},
                              {'label': 'Take', 'value': 'take', 'type': 'submit', 'color': 'danger'}
                              ]
                  }

# Hand actions widget dictionary.
ACTIONS_DICT = {'label': ': available actions👇',
                # Available actions are dynamic and collected by keys.
                'surrender': {'label': 'Surrender', 'value': 'surrender', 'type': 'submit', 'color': 'danger'},
                'stand': {'label': 'Stand', 'value': 'stand', 'type': 'submit', 'color': 'primary'},
                'hit': {'label': 'Hit', 'value': 'hit', 'type': 'submit', 'color': 'primary'},
                'double_down': {'label': 'Double Down', 'value': 'double_down', 'type': 'submit', 'color': 'secondary'},
                'split': {'label': 'Split', 'value': 'split', 'type': 'submit', 'color': 'secondary'}
                }

# Continue and exit widget dictionary.
CHOICES_DICT = {'label': 'Want another round?',
                'choices': [{'label': 'Continue', 'value': 'continue', 'type': 'submit', 'color': 'primary'},
                            {'label': 'Exit', 'value': 'exit', 'type': 'submit', 'color': 'danger'}
                            ]
                }
