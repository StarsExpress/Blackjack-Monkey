from configs.output_config import INADQT_POPUP_TITLE, MAX_SPLITS_POPUP_TITLE, POPUP_SIZE
from configs.rules_config import MIN_BET, MAX_SPLITS
from pywebio.output import popup


def notify_inadequate_capital(remaining_capital, hands=False, broke=False):  # If remaining capital isn't enough.
    notification = 'Your remaining capital ' + str(remaining_capital) + ' < minimum bet ' + str(MIN_BET) + '.'

    if hands:  # If not enough capital for another hand.
        notification += '\nSo no more hands allowed now.'
    if broke:  # If not enough capital for another round.
        notification += '\nSo game ends here.'

    popup(INADQT_POPUP_TITLE, notification, size=POPUP_SIZE)


def notify_max_splits(head_ordinal):  # If number of splits reaches maximum.
    notification = 'Hand ' + head_ordinal + ' just reached ' + str(MAX_SPLITS)
    notification += ' splits.\nSo no more splits allowed.'
    popup(MAX_SPLITS_POPUP_TITLE, notification, size=POPUP_SIZE)
