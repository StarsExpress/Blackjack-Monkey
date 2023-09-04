from configs.app_config import PAGE_NAME
from configs.output_config import PREVIOUS_HEADER, PREVIOUS_SCOPE, PREVIOUS_HEIGHT, SCOPE_WIDTH
from configs.output_config import PLAYER_HEADER, PLAYER_SCOPE, DEALER_HEADER, DEALER_SCOPE
from configs.output_config import SHARED_HEIGHT, RELATIVE_WIDTH
from pywebio.platform import config
from pywebio.output import put_html, put_collapse, put_scrollable, put_scope
from pywebio.output import use_scope, put_tabs, put_text, put_row, clear


def configure_name():  # Configure web name.
    config(title=PAGE_NAME)


def set_title(title):  # Set page title.
    put_html(title)


def set_core_layouts():  # Set game page layouts.
    # 1st row: scope for previous profits and losses.
    previous_content = put_collapse(PREVIOUS_HEADER, put_scrollable(
        put_scope(PREVIOUS_SCOPE), height=PREVIOUS_HEIGHT, keep_bottom=True))

    put_row([previous_content], size=SCOPE_WIDTH)

    # 2nd row: two parallel contents.
    # Left side content: scope for cards of each player's hand.
    player_content = put_collapse(PLAYER_HEADER, put_scrollable(
        put_scope(PLAYER_SCOPE), height=SHARED_HEIGHT, keep_bottom=True), open=True)

    # Right side content: scope for dealer's cards.
    dealer_content = put_collapse(DEALER_HEADER, put_scrollable(
        put_scope(DEALER_SCOPE), height=SHARED_HEIGHT, keep_bottom=True), open=True)

    put_row([player_content, None, dealer_content], size=RELATIVE_WIDTH)  # None means middle blank between scopes.


def set_cards_tabs(head_hands):  # Set tabs to store scopes for each head hand and its branches.
    tabs_list = []

    for i in range(1, head_hands + 1):
        head_scope = PLAYER_SCOPE + '_' + str(i)
        content = put_scope(name=head_scope, content=put_text("Hand " + str(i) + "'s Branches", scope=head_scope))
        tabs_list.append({'title': 'Hand ' + str(i), 'content': content})

    put_tabs(tabs_list, PLAYER_SCOPE)  # Put all tabs in player scope.


def write_text(message, scope, clear_scope=True):  # Performs put_text in given scope.
    with use_scope(scope, clear=clear_scope) as s:
        put_text(message, scope=s)


def clear_contents(scopes):  # Clear contents inside given scope(s). Argument type: list or string.
    if type(scopes) == list:  # If input is a list of scopes.
        for scope in scopes:
            clear(scope)

    else:
        clear(scopes)
