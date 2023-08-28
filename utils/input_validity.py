from configs.input_config import MAX_NAME_LEN
from configs.game_config import MIN_BET, MAX_CAPITAL


def check_name(name):  # Control name length.
    if len(name.strip()) > MAX_NAME_LEN:
        return 'Name length must <= ' + str(MAX_NAME_LEN) + '.'


def check_capital(capital):  # Check if initial capital is within defined range.
    if capital < MIN_BET:
        return 'Capital must >= minimum bet ' + str(MIN_BET) + '.'

    if capital > MAX_CAPITAL:
        return 'Capital must <= maximum capital ' + str(MAX_CAPITAL) + '.'
