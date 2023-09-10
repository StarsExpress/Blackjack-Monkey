from configs.input_config import DEFAULT_PLAYER_NAME
from configs.output_config import CAPITAL_TEXT, INFO_SCOPE, POPUP_DICT, POPUP_IMPLICIT_CLOSE, POPUP_SIZE
from configs.rules_config import MIN_BET, MAX_SPLITS
from widgets.layouts import write_text
from pywebio.output import popup


emoji_1, emoji_2 = POPUP_DICT['huge_profits']['emojis']  # Emojis for huge profits.


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

    popup(POPUP_DICT['inadequate_capital']['title'], notification + POPUP_IMPLICIT_CLOSE, POPUP_SIZE, True)


def remind_splits_rules(head_ordinal):
    # Remind special Aces pair split rule here.
    # Aces pair can split just once, and no hits or double down allowed after splitting Aces.
    notification = f'Hand {head_ordinal} just reached {str(MAX_SPLITS)} splits.\nNo more splits allowed for it.'
    popup(POPUP_DICT['max_splits']['title'], notification + POPUP_IMPLICIT_CLOSE, POPUP_SIZE, True)


def notify_early_exit(paid_insurance=False):  # If a round can exit early.
    notification = '\nInsurance have been paid to you.\n' if paid_insurance else ''  # Notify paid insurance.
    popup(POPUP_DICT['early_exit']['title'], POPUP_DICT['early_exit']['content'] + notification + POPUP_IMPLICIT_CLOSE,
          POPUP_SIZE, True)


def send_congrats(profit, chips):  # If a round's rate of return meets the threshold.
    if profit / chips >= POPUP_DICT['huge_profits']['threshold']:
        popup(POPUP_DICT['huge_profits']['title'],
              f'{emoji_1}{str(round(100*profit / chips, 2))}% Profit Rate{emoji_2}{POPUP_IMPLICIT_CLOSE}',
              POPUP_SIZE, True)
