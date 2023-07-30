"""All configurations."""

import os

# File path settings.
APP_BASE_PATH = os.path.dirname(os.path.abspath(__file__))  # App base path is where python files are stored.


# Cards and shuffle machine settings.
NUMBER_OF_DECKS = 6
CARDS_LIST = ([str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']) * 4

# Dictionary to map card name and value.
CARD_NAME_TO_VALUE_DICT = dict(zip(CARDS_LIST, [i for i in range(2, 11)] + [10, 10, 10, 11]))


# Core value threshold settings.
TOTAL_VALUE_MAXIMUM = 21
DEALER_VALUE_MINIMUM = 17


# Betting threshold settings.
MAXIMUM_CAPITAL = 1000000000
MAXIMUM_BET = 10000
MINIMUM_BET = 300
INITIAL_HANDS_MAXIMUM = 6


# Allowed actions settings.
# Surrender settings.
SURRENDER_TO_ACE = False

# Split settings.
SPLITS_MAXIMUM = 3
ACES_MULTI_SPLITS = False


# Profit settings.
BLACKJACK_PAYOUT = 1.5
