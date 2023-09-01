from configs.rules_config import CARD_TO_VALUE_DICT, MAX_TOTAL_VALUE


# Return format: ordinary 21 (True/False), total value, soft (True/False), bust (True/False).
def show_properties(cards_list, value_and_soft_only=False):  # Default is to return all four properties back.
    value = sum([CARD_TO_VALUE_DICT[cards] for cards in cards_list])  # Initial value of cards.
    soft = False  # Default soft value.

    if 'A' in cards_list:
        value -= 10 * cards_list.count('A')  # Count all Aces as 1 for each first.
        if value + 10 <= MAX_TOTAL_VALUE:  # If an Ace counts as 11 without bust, the given hand is soft.
            soft, value = True, value + 10  # Record greatest possible total value.

    ordinary_21 = True if value == MAX_TOTAL_VALUE else False
    bust = True if value > MAX_TOTAL_VALUE else False

    if value_and_soft_only:  # If only value and soft are needed, just return these two.
        return value, soft
    return ordinary_21, value, soft, bust


if __name__ == '__main__':
    print(show_properties(['A'] * 11))
