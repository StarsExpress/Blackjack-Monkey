from configs.output_config import RULES_SUB_SCOPES, TITLE_SCOPE
from configs.input_config import RULES_DICT
from utils.swiss_knife import read_rules
from widgets.layouts import clear_contents
from pywebio.output import put_text, put_scope, put_button, put_buttons, popup


rules_dict = read_rules()


def english():  # Display rules in English.
    clear_contents(RULES_SUB_SCOPES['text'])
    put_text(rules_dict['english'], scope=RULES_SUB_SCOPES['text'])


def trad_chn():  # Display rules in Traditional Chinese.
    clear_contents(RULES_SUB_SCOPES['text'])
    put_text(rules_dict['traditional'], scope=RULES_SUB_SCOPES['text'])


def simp_chn():  # Display rules in Simplified Chinese.
    clear_contents(RULES_SUB_SCOPES['text'])
    put_text(rules_dict['simplified'], scope=RULES_SUB_SCOPES['text'])


def show_rules():  # Display a button that pops up rules when clicked.
    popup_content = [put_scope(name=RULES_SUB_SCOPES['buttons'],
                               # Pass functions in list to allow language switch. Don't call functions.
                               content=put_buttons(RULES_DICT['language'], onclick=[english, trad_chn, simp_chn])),

                     # Default is to display rules in English.
                     put_scope(name=RULES_SUB_SCOPES['text'],
                               content=put_text(rules_dict['english'], scope=RULES_SUB_SCOPES['text']))]

    put_scope(name=TITLE_SCOPE,
              content=put_button(label=RULES_DICT['label'], color=RULES_DICT['color'],
                                 onclick=lambda: popup(RULES_DICT['title'], popup_content, RULES_DICT['size'], True),
                                 scope=TITLE_SCOPE))
