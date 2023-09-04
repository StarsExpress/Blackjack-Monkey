"""All output configurations."""

# Output widgets settings.
CAPITAL_TEXT = ': your cumulated capital is '


# Scope of player info.
INFO_SCOPE = 'Info'

# Width of all scopes.
SCOPE_WIDTH = '120%'


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
DEALER_SUB_SCOPES = {'cards': DEALER_SCOPE + '_Card', 'value': DEALER_SCOPE + '_Value'}

SHARED_HEIGHT = 300
RELATIVE_WIDTH = '85% 10px 34%'  # Relative size between player and dealer scopes. Pixels are for middle blank between.


# Notifications widget.
INADQT_POPUP_TITLE = 'Inadequate Capital'
MAX_SPLITS_POPUP_TITLE = 'No More Splits'
POPUP_SIZE = 10
