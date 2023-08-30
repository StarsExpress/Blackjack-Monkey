from configs.game_config import MIN_BET, MAX_BET


def remind_inadequate_chips(remaining_capital):  # Remind inadequate capital for another hand.
    return 'Remaining capital ' + str(remaining_capital) + ' < minimum bet ' + str(MIN_BET) + '.'


def remind_betting_amount(remaining_capital):  # Remind maximal feasible amount to bet for iterated hand.
    return str(min(remaining_capital, MAX_BET)) + "; only 100's multiples are allowed."
