from configs.rules_config import BLACKJACK_PAYOUT


# Chips = the bet amount put at head hand before double down or split.
# If dealer is busted, fill 0 as dealer value.
# Return chips to be returned, and win/draw/lose reason.
def judge_returned_chips(chips, player_value=0, dealer_value=0, player_bj=False, dealer_bj=False, double_down=False):
    if dealer_bj:  # If dealer has Blackjack.
        if player_bj:  # If player also has Blackjack.
            return chips, ' (dealer and you both have Blackjack)'  # Return initial bet.
        return 0, ' (dealer has Blackjack and you don' + "'" + 't)'  # Otherwise, return 0 as player loses initial bet.

    # If dealer doesn't have Blackjack, check the followings.
    if player_bj:  # If player has Blackjack, return original bet * 2.5.
        return int(chips * (1 + BLACKJACK_PAYOUT)), ' (you have Blackjack and dealer doesn' + "'" + 't)'

    double_down_multiple = 1 if double_down else 0  # The additional double down amount to be dealt with,
    if player_value < dealer_value:  # If dealer has a higher value, return 0 as player loses initial bet.
        return 0, ' (dealer' + "'" + 's value ' + str(dealer_value) + ' > your value ' + str(player_value) + ')'

    if player_value == dealer_value:  # If a draw happens, return initial bet.
        return chips * (1 + double_down_multiple), ' (you and dealer have the same value ' + str(player_value) + ')'

    # Return twice initial bet if player wins.
    if dealer_value == 0:  # If the reason is dealer is busted but player isn't.
        reason = ' (dealer is busted but you aren' + "'" + 't)'

    else:  # If the reason is player has a higher value.
        reason = ' (your value ' + str(player_value) + ' > dealer' + "'" + 's value ' + str(dealer_value) + ')'

    return chips * (1 + double_down_multiple) * 2, reason


if __name__ == '__main__':
    print(judge_returned_chips(400, 17, 20, False, False, True))
