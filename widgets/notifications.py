from configs.input_config import DEFAULT_PLAYER_NAME
from configs.output_config import CAPITAL_TEXT, INFO_SCOPE, POPUP_DICT, POPUP_IMPLICIT_CLOSE, POPUP_SIZE
from configs.rules_config import MIN_BET, MAX_SPLITS
from widgets.layouts import write_text
from pywebio.output import popup


emoji_1, emoji_2 = POPUP_DICT["huge_profits"]["emojis"]  # Emojis for huge profits.


def update_cumulated_capital(player_name: str | None, remaining_capital: int):
    """
    Update displayed remaining capital of player.

    Args:
        player_name (str | None): name of player. If None, default player name is used.
        remaining_capital (int): remaining capital of player.
    """
    if player_name is None:  # If player doesn't enter name.
        player_name = DEFAULT_PLAYER_NAME
    write_text(f"Dear {player_name}{CAPITAL_TEXT}{str(remaining_capital)} dollars.", INFO_SCOPE)


def notify_inadequate_capital(
        remaining_capital: int, no_more_hand: bool = False, broke: bool = False
):
    """
    Notify player if remaining capital is less than min bet.

    Args:
        remaining_capital (int): remaining capital of player.
        no_more_hand (bool, optional): if player doesn't have enough capital for another hand. Defaults to False.
        broke (bool, optional): if player doesn't have enough capital for another round. Defaults to False.
    """
    notification = f"Your remaining capital {str(remaining_capital)} < minimum bet {str(MIN_BET)}."

    if no_more_hand:
        notification += "\nNo more hands allowed in this round."
    if broke:
        notification += "\nGame over."

    popup(
        POPUP_DICT["inadequate_capital"]["title"],
        notification + POPUP_IMPLICIT_CLOSE,
        POPUP_SIZE,
        True,
    )


def remind_splits_rules(head_ordinal: str):  # Remind special Aces pair split rule.
    """
    Remind player of special Aces pair split rule.

    Args:
        head_ordinal (str): ordinal of hand.
    """
    notification = f"Hand {head_ordinal} just reached {str(MAX_SPLITS)} splits.\nNo more splits allowed for it."
    popup(
        POPUP_DICT["max_splits"]["title"],
        notification + POPUP_IMPLICIT_CLOSE,
        POPUP_SIZE,
        True,
    )


def notify_early_exit():
    """Notify the player if a round can exit early."""
    popup(
        POPUP_DICT["early_exit"]["title"],
        POPUP_DICT["early_exit"]["content"] + POPUP_IMPLICIT_CLOSE,
        POPUP_SIZE,
        True,
    )


def send_congrats(profit: int | float, chips: int):
    """
    Send congratulatory message to player if a round's rate of return meets defined threshold.

    Args:
        profit (int | float): profit made in given round.
        chips (int): number of chips bet in given round.
    """
    if profit / chips >= POPUP_DICT["huge_profits"]["threshold"]:
        content = f"{emoji_1}{str(round(100 * profit / chips, 2))}% Profit Rate{emoji_2}{POPUP_IMPLICIT_CLOSE}"
        popup(POPUP_DICT["huge_profits"]["title"], content, POPUP_SIZE, True)
