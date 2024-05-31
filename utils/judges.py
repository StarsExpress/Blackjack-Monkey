from configs.rules_config import CARD_TO_VALUE_DICT, SURRENDER_TO_ACE, MAX_SPLITS


def judge_blackjack(cards_list, split=False):  # Blackjack judgement format: (True/False).
    if split:  # If split is conducted, then no Blackjack.
        return False

    # If only two cards, and is an Ace with a 10-valued card, it is Blackjack.
    if (len(cards_list) == 2) & ('A' in cards_list) & (len({'10', 'J', 'Q', 'K'} & set(cards_list)) == 1):
        return True
    return False


def judge_surrender(cards_list, dealer_first_card, splits):  # Surrender eligibility judgement format: (True/False).
    # If only first two cards and abide by surrender to dealer's Ace setting, return True.
    if (len(cards_list) == 2) & (SURRENDER_TO_ACE | (dealer_first_card != 'A')) & (splits == 0):
        return True
    return False


def judge_split(cards_list, splits):  # Split eligibility judgement format: (True/False).
    # If both cards have the same face value and haven't reached splits maximum, return True.
    if splits < MAX_SPLITS:
        if (len(cards_list) == 2) & (CARD_TO_VALUE_DICT[cards_list[0]] == CARD_TO_VALUE_DICT[cards_list[-1]]):
            return True
    return False
