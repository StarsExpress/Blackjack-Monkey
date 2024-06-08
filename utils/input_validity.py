from configs.input_config import MAX_NAME_LEN
from configs.rules_config import MIN_BET, MAX_CAPITAL


def check_name(name: str):  # Control player name length after removal of edge spaces.
    if len(name.lstrip().rstrip()) > MAX_NAME_LEN:
        return f'Name length must <= {str(MAX_NAME_LEN)}.'


def check_capital(capital: int):  # Check if initial capital is within defined range.
    if capital < MIN_BET:
        return f'Capital must >= minimum bet {str(MIN_BET)}.'
    if capital > MAX_CAPITAL:
        return f'Capital must <= maximum capital {str(MAX_CAPITAL)}.'
