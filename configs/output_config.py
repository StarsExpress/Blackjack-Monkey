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


# Scopes of each hand and dealer. They are put in a shared row with identical height.
HANDS_HEADER = 'Your Hands'
HANDS_SCOPE = 'Hands'

DEALER_HEADER = "Dealer's hand"
DEALER_SCOPE = 'Dealer'
# Sub scopes within dealer scope include card and value.
DEALER_SUB_SCOPES = {'card': DEALER_SCOPE + '_Card', 'value': DEALER_SCOPE + '_Value'}

SHARED_HEIGHT = 200
RELATIVE_WIDTH = '72% 10px 47%'  # Relative size between hands and dealer scopes. Pixels are for middle blank between.


# Popup widget when inadequate capital happens.
POPUP_TITLE = 'Inadequate Capital'
POPUP_SIZE = 10
