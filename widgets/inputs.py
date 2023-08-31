from configs.input_config import NAME_DICT, CAPITAL_DICT, HANDS_DICT, CHOICES_DICT
from configs.output_config import HANDS_SCOPE, CHOICE_SCOPE
from utils.input_validity import check_name, check_capital
from pywebio.input import input_group, input, TEXT, NUMBER, slider, actions
from pywebio.output import use_scope


def get_info():  # Get player's info: name and initial capital.
    return input_group(inputs=[
        input(label=NAME_DICT['label'], name=NAME_DICT['name'], type=TEXT,
              validate=check_name, placeholder=NAME_DICT['holder']),

        # Initial capital is a required input.
        input(label=CAPITAL_DICT['label'], name=CAPITAL_DICT['name'], type=NUMBER, required=True,
              validate=check_capital, placeholder=CAPITAL_DICT['holder'])
    ])


def get_hands():  # Get number of hands to bet before each round.
    with use_scope(name=HANDS_SCOPE):  # Need to clear contents first.
        return slider(label=HANDS_DICT['label'], min_value=HANDS_DICT['min'], max_value=HANDS_DICT['max'])


def get_chips(chips_dict, validate_function):  # Get chips placed by player for each hand.
    # with use_scope(name=HANDS_SCOPE):
    return input(label=chips_dict['label'], type=NUMBER, required=True,
                 validate=validate_function, placeholder=chips_dict['holder'])


def get_choice():  # Get player's choice of continue to play or exit.
    with use_scope(name=CHOICE_SCOPE):
        return actions(CHOICES_DICT['label'], buttons=CHOICES_DICT['actions'])
