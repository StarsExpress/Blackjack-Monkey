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
# Sub scopes within player scope include card and value.
PLAYER_SUB_SCOPES = {'card': PLAYER_SCOPE + '_Card', 'value': PLAYER_SCOPE + '_Value'}

DEALER_HEADER = "Dealer's Hand"
DEALER_SCOPE = 'Dealer'
# Sub scopes within dealer scope include card and value.
DEALER_SUB_SCOPES = {'card': DEALER_SCOPE + '_Card', 'value': DEALER_SCOPE + '_Value'}

SHARED_HEIGHT = 200
RELATIVE_WIDTH = '72% 10px 47%'  # Relative size between player and dealer scopes. Pixels are for middle blank between.


# Popup widget when inadequate capital happens.
POPUP_TITLE = 'Inadequate Capital'
POPUP_SIZE = 10
