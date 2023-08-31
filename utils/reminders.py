from configs.rules_config import MAX_BET


def remind_betting_amount(remaining_capital):  # Remind maximal feasible amount to bet for iterated hand.
    return str(min(remaining_capital, MAX_BET)) + ". Only accept 100's multiples."
