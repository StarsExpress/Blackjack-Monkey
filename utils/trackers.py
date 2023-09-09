from configs.rules_config import CARD_TO_VALUE_DICT, MAX_TOTAL_VALUE, MIN_DEALER_VALUE


# Return format: value (integer), soft (True/False), bust (True/False).
def update_properties(cards_list):
    soft = False
    value = sum([CARD_TO_VALUE_DICT[cards] for cards in cards_list])  # Initial value of cards.

    if 'A' in cards_list:
        value -= 10 * cards_list.count('A')  # Count all Aces as 1 for each first.
        if value + 10 <= MAX_TOTAL_VALUE:  # If an Ace counts as 11 without bust, the given hand is soft.
            value += 10  # Take the greatest possible total value.
            soft = True

    bust = True if value > MAX_TOTAL_VALUE else False
    return value, soft, bust


# Return the hand value to be displayed on game page.
def track_display_value(value, blackjack=False, dealer=False, player_all_bj=False, stand=False, soft=False, bust=False):
    # Argument dealer is False if this function is called for player's hand. Otherwise, it should be True.

    if blackjack:
        return 'Blackjack'
    if dealer & player_all_bj:  # If dealer has no Blackjack, and all hands from player are.
        return 'No Blackjack'
    if bust:
        return 'Busted'

    # Show both possible values in either case.
    # 1. Player's soft hand hasn't stood, and is under 21.
    if (dealer is False) & soft & (stand is False) & (value < MAX_TOTAL_VALUE):
        return '/'.join([str(value), str(value - 10)])

    # 2. Dealer's soft hand is under required value.
    if dealer & soft & (value < MIN_DEALER_VALUE):
        return '/'.join([str(value), str(value - 10)])

    return str(value)


if __name__ == '__main__':
    print(update_properties(['A'] * 11))
    print(track_display_value(18, soft=True, stand=True))
