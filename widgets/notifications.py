from configs.output_config import POPUP_TITLE, POPUP_SIZE
from configs.rules_config import MIN_BET
from pywebio.output import popup


def notify_inadequate_capital(remaining_capital, hands=False, broke=False):  # If remaining capital isn't enough.
    notification = 'Your remaining capital ' + str(remaining_capital) + ' < minimum bet ' + str(MIN_BET) + '.'

    if hands:  # If not enough capital for another hand.
        notification += '\nSo no more hands allowed now.'
    if broke:  # If not enough capital for another round.
        notification += '\nSo game ends here.'

    popup(POPUP_TITLE, notification, size=POPUP_SIZE)
