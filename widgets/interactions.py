from configs.app_config import RULES_PATHS_DICT
from configs.output_config import TITLE_SCOPE
from configs.input_config import RULES_DICT, NAME_DICT, CAPITAL_DICT, HANDS_DICT, EARLY_PAY_DICT
from configs.input_config import INSURANCE_DICT, MOVES_DICT, CHOICES_DICT
from utils.input_validity import check_name, check_capital
from utils.judges import judge_surrender, judge_split
from utils.swiss_knife import assist_insurance_checkbox, find_ordinal_text
from pywebio.input import input_group, input, TEXT, NUMBER, slider, actions, checkbox
from pywebio.output import put_scope, put_button, popup


file = open(RULES_PATHS_DICT['english'], 'r')
rules_txt = file.read()
file.close()


def read_rules():  # Display a button that pops up rules when clicked.
    put_scope(name=TITLE_SCOPE, content=put_button(label=RULES_DICT['label'], color=RULES_DICT['color'],
                                                   onclick=lambda: popup(RULES_DICT['title'], rules_txt,
                                                                         RULES_DICT['size'], True), scope=TITLE_SCOPE))


def get_info():  # Get player's info: name and initial capital.
    return input_group(inputs=[
        input(label=NAME_DICT['label'], name=NAME_DICT['name'], type=TEXT,
              validate=check_name, placeholder=NAME_DICT['holder']),

        # Initial capital is a required input.
        input(label=CAPITAL_DICT['label'], name=CAPITAL_DICT['name'], type=NUMBER, required=True,
              validate=check_capital, placeholder=CAPITAL_DICT['holder'])
    ])


def get_hands():  # Get number of hands to bet before each round.
    return slider(label=HANDS_DICT['label'], min_value=HANDS_DICT['min'], max_value=HANDS_DICT['max'])


def get_chips(chips_dict, validate_function):  # Get chips placed by player for each hand.
    return input(label=chips_dict['label'], type=NUMBER, required=True,
                 validate=validate_function, placeholder=chips_dict['holder'])


def get_early_pay(head_ordinal):  # Get Blackjack early pay option.
    return actions(f"Hand {head_ordinal}: {EARLY_PAY_DICT['label']}", buttons=EARLY_PAY_DICT['options'])


def get_insurance(dealer_first_card, non_bj_hands_list, hands_dict, validate_function):
    # If no insurance to be asked, return empty list to match the return type from checkbox.
    if dealer_first_card != 'A':
        return []

    options_list = assist_insurance_checkbox(non_bj_hands_list, hands_dict)
    return checkbox(label=INSURANCE_DICT['label'], options=options_list, inline=True,
                    value=non_bj_hands_list, validate=validate_function)


def get_move(ordinals_tuple, cards_list, dealer_card, splits, remaining_capital, initial_bet):  # Get player's move.
    # Ordinals tuple format: (head ordinal, branch ordinal).
    actions_list = []
    if judge_surrender(cards_list, dealer_card, splits):  # First check surrender availability.
        actions_list += [MOVES_DICT['surrender']]

    actions_list += [MOVES_DICT['stand'], MOVES_DICT['hit']]

    if remaining_capital >= initial_bet:  # When remaining capital is enough, check double down and split availability.
        if len(cards_list) == 2:
            actions_list += [MOVES_DICT['double_down']]
        if judge_split(cards_list, splits):
            actions_list += [MOVES_DICT['split']]

    return actions(f"Hand {ordinals_tuple[0]}'s {find_ordinal_text(ordinals_tuple[-1])} " +
                   f"Branch: {MOVES_DICT['label']}", buttons=actions_list)


def get_choice():  # Get choice of continue to play or exit.
    return actions(CHOICES_DICT['label'], buttons=CHOICES_DICT['choices'])
