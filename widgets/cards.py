from configs.output_config import PLAYER_SCOPE, PLAYER_SUB_SCOPES, DEALER_SCOPE, DEALER_SUB_SCOPES, SHARED_HEIGHT
from utils.ordinal import find_text_ordinal
from utils.trackers import track_display_value
from widgets.layouts import clear_contents
from pywebio.output import put_collapse, put_scrollable, put_row, put_markdown, put_scope, put_table


# Display new drawn card and current value of player's hand.
def show_player_value(head_ordinal, branch_ordinal, cards_list, value=0, blackjack=False,
                      stand=False, soft=False, bust=False, clear=False, new_branch=False):
    tab_scope = PLAYER_SCOPE + '_' + head_ordinal  # Tab to which input hand belongs.
    branch_scope = tab_scope + '_' + branch_ordinal  # Branch scope for input hand.

    card_scope = branch_scope + '_' + PLAYER_SUB_SCOPES['card']  # Card and value scopes inside branch scope.
    value_scope = branch_scope + '_' + PLAYER_SUB_SCOPES['value']

    if clear:  # Only called when a head hand commits 1st split.
        clear_contents(card_scope)

    value = track_display_value(value=value, blackjack=blackjack, stand=stand, soft=soft, bust=bust)
    if new_branch:  # Only called when a new branch hand has to be displayed.
        branch_title = find_text_ordinal(branch_ordinal) + ' Branch'
        # Add new branch scope in tab scope.
        put_collapse(branch_title, put_scrollable(
            put_scope(branch_scope), height=SHARED_HEIGHT // 3, keep_bottom=True), open=True, scope=tab_scope)

        # In new branch scope, set markdowns and sub scopes for card as well as value.
        put_row([put_markdown('Cards'), None, put_markdown('Value')], scope=branch_scope)
        put_row([
            put_scope(card_scope, put_table([cards_list], scope=card_scope)),
            None,  # None means middle blank.
            put_scope(value_scope, put_table([[value]], scope=value_scope))
        ], scope=branch_scope)
        return

    # For already existing branch hand, make updates.
    clear_contents(value_scope)  # Erase old value for new value.
    put_table([[value]], scope=value_scope)

    # Display new drawn card(s): if not first two cards, only show the last card from list.
    cards_list = cards_list if len(cards_list) == 2 else cards_list[-1:]
    put_table([cards_list], scope=card_scope)


# Display new drawn card and current value of dealer's hand.
def show_dealer_value(card, value=0, first=False, blackjack=False, player_all_bj=False, soft=False, bust=False):
    if first:  # If is first card, do the followings in dealer scope.
        # First: a row of markdowns.
        put_row([put_markdown('Cards'), None, put_markdown('Value')], scope=DEALER_SCOPE)
        # Second: a row of sub scopes for card and value, respectively.
        put_row([put_scope(DEALER_SUB_SCOPES['card']), None, put_scope(DEALER_SUB_SCOPES['value'])], scope=DEALER_SCOPE)

    put_table([[card]], scope=DEALER_SUB_SCOPES['card'])

    clear_contents(DEALER_SUB_SCOPES['value'])  # Clear value table.
    value = track_display_value(value, blackjack, dealer=True, player_all_bj=player_all_bj, soft=soft, bust=bust)
    put_table([[value]], scope=DEALER_SUB_SCOPES['value'])  # Update value.
