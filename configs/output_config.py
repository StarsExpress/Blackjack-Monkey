"""All output configurations."""

TITLE_SCOPE = 'Title'

# Sub scopes within rules scope: buttons and text.
RULES_SUB_SCOPES = {'buttons': 'rules_buttons', 'text': 'rules_txt'}

INFO_SCOPE = 'Info'  # Scope of player info.
CAPITAL_TEXT = ': your cumulated capital is '  # Capital tracking.
SCOPE_WIDTH = '120%'  # Width of all scopes.

# Scope of previous rounds and player interactions.
PREVIOUS_HEADER = 'Income Statement: Previous P&L'
PREVIOUS_SCOPE = 'Previous'
PREVIOUS_HEIGHT = 150

# Scopes of each hand for player and dealer. They are put in a shared row with identical height.
PLAYER_HEADER = 'Your Hands'
PLAYER_SCOPE = 'Player'
# Sub scopes within player scope: chips, cards, value and profit.
PLAYER_SUB_SCOPES = {'chips': 'Chips', 'cards': 'Cards', 'value': 'Value', 'profit': 'Profit'}

DEALER_HEADER = "Dealer's Hand"
DEALER_SCOPE = 'Dealer'
# Sub scopes within dealer scope: cards and value.
DEALER_SUB_SCOPES = {'cards': f'{DEALER_SCOPE}_Card', 'value': f'{DEALER_SCOPE}_Value'}

SHARED_HEIGHT = 350
RELATIVE_WIDTH = '85% 10px 34%'  # Relative size between player and dealer scopes. Pixels are for middle blank between.

# Hands values style.
VALUES_COLORS = {'safe': 'black', 'danger': 'orange', 'busted': 'red'}
DANGER_ZONE = {'lower': 12, 'upper': 16}

# Profits style.
PROFITS_COLORS = {'tie': 'black', 'loss': 'red', 'profit': 'green'}

# Notifications widget.
POPUP_DICT = {'inadequate_capital': {'title': '‼️Inadequate Capital‼️'},
              'max_splits': {'title': '⛔No More Splits⛔'},
              'early_exit': {'title': '🛬Early Exit🛬',
                             'content': 'Your hands are all judged.'
                             },
              'huge_profits': {'title': '🎉Winner Winner Chicken Dinner🦃',
                               'emojis': ('💵', '🍾'),
                               'threshold': 0.7
                               }
              }
POPUP_IMPLICIT_CLOSE = '\n(Click anywhere to close~)'  # Reminder of how to close popup.
POPUP_SIZE = 5
