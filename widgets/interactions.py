from configs.input_config import NAME_DICT, CAPITAL_DICT, HANDS_DICT, EARLY_PAY_DICT, ACTIONS_DICT, CHOICES_DICT
from utils.input_validity import check_name, check_capital
from utils.judges import judge_surrender, judge_split
from utils.ordinal import find_ordinal_text
from pywebio.input import input_group, input, TEXT, NUMBER, slider, actions


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
    return actions('Hand ' + head_ordinal + EARLY_PAY_DICT['label'], buttons=EARLY_PAY_DICT['options'])


def get_action(ordinals_tuple, cards_list, dealer_card, splits, remaining_capital, initial_bet):  # Get player's action.
    # Ordinals tuple format: (head ordinal, branch ordinal).
    actions_list = []
    if judge_surrender(cards_list, dealer_card, splits):  # First check surrender availability.
        actions_list += [ACTIONS_DICT['surrender']]

    actions_list += [ACTIONS_DICT['stand'], ACTIONS_DICT['hit']]

    if remaining_capital >= initial_bet:  # When remaining capital is enough, check double down and split availability.
        if len(cards_list) == 2:
            actions_list += [ACTIONS_DICT['double_down']]
        if judge_split(cards_list, splits):
            actions_list += [ACTIONS_DICT['split']]

    return actions('Hand ' + ordinals_tuple[0] + "'s " + find_ordinal_text(ordinals_tuple[-1]) +
                   ' Branch' + ACTIONS_DICT['label'], buttons=actions_list)


def get_choice():  # Get choice of continue to play or exit.
    return actions(CHOICES_DICT['label'], buttons=CHOICES_DICT['choices'])
