from configs.input_config import DEFAULT_NAME, MARKDOWN, NAME_DICT, CAPITAL_DICT, HANDS_DICT
from configs.output_config import CAPITAL_DISPLAY
from utils.input_validity import check_name, check_capital
from pywebio.input import input_group, input, TEXT, NUMBER, slider
from pywebio.output import put_markdown, put_text


class Application:
    """Blackjack app."""

    def __init__(self):
        self.name, self.initial_capital = DEFAULT_NAME, 0

    def execute(self):
        put_markdown(MARKDOWN)

        input_dict = input_group(inputs=[
            input(label=NAME_DICT['label'], name=NAME_DICT['name'], type=TEXT,
                  validate=check_name, placeholder=NAME_DICT['holder']),

            input(label=CAPITAL_DICT['label'], name=CAPITAL_DICT['name'], type=NUMBER, required=True,
                  validate=check_capital, placeholder=CAPITAL_DICT['holder'])
        ])  # Initial capital is a required input.

        if len(input_dict[NAME_DICT['name']].strip()) > 0:  # If player enters non-empty name.
            self.name = NAME_DICT['name'].lstrip().rstrip()  # Keep middle spaces.
        self.initial_capital = input_dict[CAPITAL_DICT['name']]

        put_text('Dear ' + self.name + CAPITAL_DISPLAY + str(self.initial_capital) + ' dollars')
        hands = slider(HANDS_DICT['label'], min_value=HANDS_DICT['min'], max_value=HANDS_DICT['max'])
