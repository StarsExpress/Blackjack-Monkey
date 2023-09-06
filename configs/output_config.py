"""All output configurations."""

INFO_SCOPE = 'Info'  # Scope of player info.
CAPITAL_TEXT = ': your cumulated capital is '  # Capital tracking.
SCOPE_WIDTH = '120%'  # Width of all scopes.


# Scope of previous rounds and player interactions.
PREVIOUS_HEADER = 'Income Statement: Previous P&L'
PREVIOUS_SCOPE = 'Previous'
PREVIOUS_HEIGHT = 200


# Scopes of each hand for player and dealer. They are put in a shared row with identical height.
PLAYER_HEADER = 'Your Hands'
PLAYER_SCOPE = 'Player'
# Sub scopes within player scope: chips, cards and value.
PLAYER_SUB_SCOPES = {'chips': 'Chips', 'cards': 'Cards', 'value': 'Value'}

DEALER_HEADER = "Dealer's Hand"
DEALER_SCOPE = 'Dealer'
# Sub scopes within dealer scope: cards and value.
DEALER_SUB_SCOPES = {'cards': f'{DEALER_SCOPE}_Card', 'value': f'{DEALER_SCOPE}_Value'}

SHARED_HEIGHT = 300
RELATIVE_WIDTH = '85% 10px 34%'  # Relative size between player and dealer scopes. Pixels are for middle blank between.


# Hands values style.
VALUE_COLORS = {'safe': 'black', 'danger': 'orange', 'busted': 'red'}
DANGER_ZONE = {'lower': 12, 'upper': 16}


# Notifications widget.
INADQT_POPUP_TITLE = 'Inadequate Capital'
MAX_SPLITS_POPUP_TITLE = 'No More Splits'
POPUP_SIZE = 10
