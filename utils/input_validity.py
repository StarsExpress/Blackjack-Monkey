from configs.input_config import MAX_NAME_LEN
from configs.game_config import MIN_BET, MAX_CAPITAL, MAX_BET


def check_name(name):  # Control player name length.
    if len(name.lstrip().rstrip()) > MAX_NAME_LEN:  # Check length after removal of edge spaces.
        return 'Name length must <= ' + str(MAX_NAME_LEN) + '.'


def check_capital(capital):  # Check if initial capital is within defined range.
    if capital < MIN_BET:
        return 'Capital must >= minimum bet ' + str(MIN_BET) + '.'
    if capital > MAX_CAPITAL:
        return 'Capital must <= maximum capital ' + str(MAX_CAPITAL) + '.'


def check_chips(remaining_capital, chips=0):  # Check if input chips are valid.
    if chips < MIN_BET:  # If input < minimum bet, continue while.
        return 'Chips must >= minimum bet ' + str(MIN_BET) + '.'
    if chips > MAX_BET:  # If input > maximum bet, continue while.
        return 'Chips must <= maximum bet ' + str(MAX_BET) + '.'
    if chips > remaining_capital:
        return 'Chips must < remaining capital ' + str(remaining_capital) + '.'
    if chips % 100 != 0:  # If input isn't 100's multiple, continue while.
        return "Chips must be 100's multiple."
