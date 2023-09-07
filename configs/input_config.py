"""All input configurations."""

from configs.rules_config import MIN_BET, MAX_CAPITAL

# Player name widget.
MAX_NAME_LEN = 20  # Maximal player name length.
DEFAULT_PLAYER_NAME = '💸Benji Bucket🪣'  # If player doesn't enter name.
NAME_DICT = {'label': '😃How may we call you, Sir/Madame:', 'name': 'name',
             'holder': f"Would like to know your name, or we'll call you {DEFAULT_PLAYER_NAME}",
             }


# Capital widget.
CAPITAL_DICT = {'label': '💰Cash in your capital, please:', 'name': 'capital',
                'holder': f'Please be integer. Available range: {str(MIN_BET)} to {str(MAX_CAPITAL)}.',
                }


# Hands widget.
HANDS_DICT = {'label': 'How many hands do you want', 'min': 1, 'max': 6}


# Chips widget.
CHIPS_DICT = {'label': '💰Put your chips for hand',
              'holder': f'Please be integer. Available range: {str(MIN_BET)} to'
              }


# Early pay widget.
EARLY_PAY_DICT = {'label': 'take early pay❓',
                  'options': [{'label': 'Take', 'value': 'take', 'type': 'submit', 'color': 'danger'},
                              {'label': 'Wait', 'value': 'wait', 'type': 'submit', 'color': 'success'}
                              ]
                  }


# Player actions widget.
ACTIONS_DICT = {'label': 'available actions👇',
                # Available actions are dynamic and collected by keys.
                'surrender': {'label': 'Surrender', 'value': 'surrender', 'type': 'submit', 'color': 'danger'},
                'stand': {'label': 'Stand', 'value': 'stand', 'type': 'submit', 'color': 'primary'},
                'hit': {'label': 'Hit', 'value': 'hit', 'type': 'submit', 'color': 'success'},
                'double_down': {'label': 'Double Down', 'value': 'double_down', 'type': 'submit', 'color': 'warning'},
                'split': {'label': 'Split', 'value': 'split', 'type': 'submit', 'color': 'info'}
                }


# Continue or exit widget.
CHOICES_DICT = {'label': 'Want another round?',
                'choices': [{'label': 'Continue', 'value': 'continue', 'type': 'submit', 'color': 'success'},
                            {'label': 'Exit', 'value': 'exit', 'type': 'submit', 'color': 'danger'}
                            ]
                }
