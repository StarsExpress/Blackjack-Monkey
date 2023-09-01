from configs.output_config import PLAYER_SCOPE, PLAYER_SUB_SCOPES, DEALER_SCOPE, DEALER_SUB_SCOPES, SHARED_HEIGHT
from utils.trackers import track_display_value
from widgets.outputs import write_text, clear_contents
from pywebio.output import put_collapse, put_scrollable, put_row, put_markdown, put_scope, put_table


# Display new drawn card and current value of player's hand.
def show_player_value(head_ordinal, branch_ordinal, cards_list, value=0, soft=False, bust=False, blackjack=False,
                      split=False, need_new=False, clear=False):
    title = 'Hand ' + head_ordinal
    hand_scope = PLAYER_SCOPE + '_' + head_ordinal

    sub_scopes_dict = PLAYER_SUB_SCOPES.copy()  # Make a copy to prevent changing config's values.
    sub_scopes_dict.update({'card': '_'.join([sub_scopes_dict['card'], head_ordinal])})
    sub_scopes_dict.update({'value': '_'.join([sub_scopes_dict['value'], head_ordinal])})

    if split:  # If the input hand is from split.
        title += ''.join(["'s Branch_", branch_ordinal])
        hand_scope += ''.join(['_', branch_ordinal])

    if need_new:  # If needed, create sub scopes in player scope.
        if clear:
            clear_contents(hand_scope)

            sub_scopes_dict.update({'card': '_'.join([sub_scopes_dict['card'], branch_ordinal])})
            sub_scopes_dict.update({'value': '_'.join([sub_scopes_dict['value'], branch_ordinal])})

        # Create current hand scope in player scope.
        put_collapse(title, put_scrollable(
            put_scope(hand_scope), height=SHARED_HEIGHT, keep_bottom=True), open=True, scope=PLAYER_SCOPE)

        # In current hand scope, set markdowns and sub scopes. None means middle blank.
        put_row([put_markdown('Card'), None, put_markdown('Value')], scope=hand_scope)
        put_row([put_scope(sub_scopes_dict['card']), None, put_scope(sub_scopes_dict['value'])], scope=hand_scope)

    if len(cards_list) == 2:
        cards_description = 'First two: ' + ', '.join(cards_list)

    else:  # If not first two cards, only take the last card from list.
        cards_description = 'New drawn: ' + cards_list[-1]

    write_text(cards_description, scope=sub_scopes_dict['card'])

    clear_contents(sub_scopes_dict['value'])  # Clear value table.
    value = track_display_value(value, blackjack, False, False, soft, bust)
    put_table([[value]], scope=sub_scopes_dict['value'])  # Update value.


# Display new drawn card and current value of dealer's hand.
def show_dealer_value(card, value=0, first=False, blackjack=False, player_all_blackjack=False, soft=False, bust=False):
    if first:  # If is first card, do the followings in dealer scope.
        # First: a row of markdowns.
        put_row([put_markdown('Card'), None, put_markdown('Value')], scope=DEALER_SCOPE)
        # Second: a row of sub scopes for card and value, respectively.
        put_row([put_scope(DEALER_SUB_SCOPES['card']), None, put_scope(DEALER_SUB_SCOPES['value'])], scope=DEALER_SCOPE)

    cards_description = 'First: ' if first else 'New drawn: '  # Differentiate first and non-first cards.
    write_text(cards_description + card, scope=DEALER_SUB_SCOPES['card'])

    clear_contents(DEALER_SUB_SCOPES['value'])  # Clear value table.
    value = track_display_value(value, blackjack, True, player_all_blackjack, soft, bust)
    put_table([[value]], scope=DEALER_SUB_SCOPES['value'])  # Update value.
