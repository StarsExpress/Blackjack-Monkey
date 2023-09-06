from configs.rules_config import BLACKJACK_PAYOUT


# Chips: final bet amount placed at input hand.
# If dealer is busted, fill 0 as dealer value.
# Return two things: chips to be returned and win/draw/lose reason.
def judge_returned_chips(chips, player_value=0, dealer_value=0, player_bj=False, dealer_bj=False):
    if dealer_bj:  # If dealer has Blackjack.
        if player_bj:  # If player also has Blackjack.
            return chips, ' (dealer and you both have Blackjack)'
        return 0, " (dealer has Blackjack and you don't)"

    if player_bj:  # If player has Blackjack, return chips according to Blackjack payout rate.
        return f"{int(chips * (1 + BLACKJACK_PAYOUT))} (you have Blackjack and dealer doesn't)"

    if player_value < dealer_value:  # If dealer wins.
        return 0, f" (dealer's value {str(dealer_value)} > your value {str(player_value)})"

    if player_value == dealer_value:  # If a draw happens.
        return chips, f' (you and dealer have the same value {str(player_value)})'

    # If player wins.
    if dealer_value == 0:
        reason = " (dealer is busted but you aren't)"

    else:
        reason = f" (your value {str(player_value)} > dealer's value {str(dealer_value)})"

    return chips * 2, reason


if __name__ == '__main__':
    print(judge_returned_chips(400, 17, 0, False, False))
