from configs.input_config import DEFAULT_PLAYER_NAME
from configs.output_config import CAPITAL_TEXT, INFO_SCOPE, POPUP_TITLES, POPUP_SIZE
from configs.rules_config import MIN_BET, MAX_SPLITS
from widgets.layouts import write_text
from pywebio.output import popup


def update_cumulated_capital(player_name, remaining_capital):  # If capital amount changes.
    if player_name is None:  # If player doesn't enter name.
        player_name = DEFAULT_PLAYER_NAME
    write_text(f'Dear {player_name}{CAPITAL_TEXT}{str(remaining_capital)} dollars.', INFO_SCOPE)


def notify_inadequate_capital(remaining_capital, hands=False, broke=False):  # If remaining capital isn't enough.
    notification = f'Your remaining capital {str(remaining_capital)} < minimum bet {str(MIN_BET)}.'

    if hands:  # If not enough capital for another hand.
        notification += '\nNo more hands allowed in this round.'
    if broke:  # If not enough capital for another round.
        notification += '\nGame over.'

    popup(POPUP_TITLES['inadequate_capital'], notification, size=POPUP_SIZE)


def remind_splits_rules(head_ordinal):
    # Remind special Aces pair split rule here.
    # Aces pair can split just once, and no hits or double down allowed after splitting Aces.
    notification = f'Hand {head_ordinal} just reached {str(MAX_SPLITS)} splits.\nNo more splits allowed for it.'
    popup(POPUP_TITLES['max_splits'], notification, size=POPUP_SIZE)


def notify_early_exit():  # If all hands have been judged and no need for dealer to draw to 17+.
    popup(POPUP_TITLES['early_exit'], 'You have no hands left to be judged in this round.', size=POPUP_SIZE)
