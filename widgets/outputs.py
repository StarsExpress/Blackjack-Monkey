from configs.app_config import PAGE_NAME
from configs.output_config import PREVIOUS_HEADER, PREVIOUS_SCOPE, PREVIOUS_HEIGHT, SHARED_WIDTH, INTER_SCOPE
from configs.output_config import HANDS_HEADER, HANDS_SCOPE, DEALER_HEADER, DEALER_SCOPE
from configs.output_config import SHARED_HEIGHT, RELATIVE_WIDTH, POPUP_TITLE, POPUP_SIZE
from configs.rules_config import MIN_BET
from pywebio.platform import config
from pywebio.output import put_html, put_collapse, put_scrollable, put_scope, use_scope, put_text, popup, clear, put_row


def configure_name():  # Configure web name.
    config(title=PAGE_NAME)


def set_title(title):  # Set page title.
    put_html(title)


def put_layout():
    # Collapsible and scrollable scope for previous profits and losses.
    previous = put_collapse(PREVIOUS_HEADER, put_scrollable(
        put_scope(PREVIOUS_SCOPE), height=PREVIOUS_HEIGHT, keep_bottom=True))

    put_row([previous], size=SHARED_WIDTH)

    # Collapsible and scrollable scope for each hand of player.
    hands = put_collapse(HANDS_HEADER, put_scrollable(
        put_scope(HANDS_SCOPE), height=SHARED_HEIGHT, keep_bottom=True), open=True)

    # Collapsible and scrollable scope for dealer's cards.
    dealer = put_collapse(DEALER_HEADER, put_scrollable(
        put_scope(DEALER_SCOPE), height=SHARED_HEIGHT, keep_bottom=True), open=True)

    put_row([hands, None, dealer], size=RELATIVE_WIDTH)  # None means middle blank between scopes.


def write_text(message, scope, use=False):  # Performs put_text in given scope.
    if use:  # Apply use_scope syntax if use is True.
        with use_scope(scope):
            put_text(message)
        return

    put_text(message, scope=scope)


def notify_inadequate_capital(remaining_capital, game=False, hands=False):  # If remaining capital isn't enough.
    notification = 'Your remaining capital ' + str(remaining_capital) + ' < minimum bet ' + str(MIN_BET) + '.'
    if hands:
        notification += '\nSo no more hands allowed now.'
    if game:
        notification += '\nSo game ends here.'
    popup(POPUP_TITLE, notification, size=POPUP_SIZE)  # Pop up notification.


def clear_contents(scopes):  # Clear contents inside given scope(s).
    if type(scopes) == list:  # If input is a list of scopes.
        for scope in scopes:
            clear(scope)

    else:
        clear(scopes)


def show_cards(head_ordinal, branch_ordinal, cards_list, split=False):  # Display input hand's cards.
    if split:  # If the input hand is from split.
        print('Hand ' + head_ordinal + "'" + 's branch hand ' + branch_ordinal + ': ' + ', '.join(cards_list) + '.')
        return
    print('Hand ' + head_ordinal + ': ' + ', '.join(cards_list) + '.')
    return
