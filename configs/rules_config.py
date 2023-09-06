"""All rules configurations."""

NUMBER_OF_DECKS = 6
CARDS_LIST = ([str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']) * 4
# Dictionary to map card name and value.
CARD_TO_VALUE_DICT = dict(zip(CARDS_LIST, [i for i in range(2, 11)] + [10, 10, 10, 11]))


MAX_TOTAL_VALUE = 21  # Each hand is busted if over this value.
MIN_DEALER_VALUE = 17


MAX_CAPITAL = 1000000000
MAX_BET = 10000
MIN_BET = 300


SURRENDER_TO_ACE = False


MAX_SPLITS = 3
ACES_MULTI_SPLITS = False


BLACKJACK_PAYOUT = 1.5
