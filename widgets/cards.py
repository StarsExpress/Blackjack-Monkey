from configs.rules_config import MIN_DEALER_VALUE
from configs.output_config import PLAYER_SCOPE, PLAYER_SUB_SCOPES, DEALER_SCOPE, DEALER_SUB_SCOPES, SHARED_HEIGHT
from widgets.outputs import write_text, clear_contents
from pywebio.output import put_collapse, put_scrollable, put_row, put_markdown, put_scope, put_table


# Display new drawn card and current value of player's hand.
def show_player_value(head_ordinal, branch_ordinal, cards_list, value=0, soft=False, bust=False, blackjack=False,
                      split=False, need_new=False, clear=False):
    title = 'Hand ' + head_ordinal
    hand_scope = PLAYER_SCOPE + '_' + head_ordinal
    sub_scopes_dict = PLAYER_SUB_SCOPES.copy()
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

        put_collapse(title, put_scrollable(
            put_scope(hand_scope), height=SHARED_HEIGHT, keep_bottom=True), open=True, scope=PLAYER_SCOPE)
        put_row([put_markdown('Card'), None, put_markdown('Value')], scope=hand_scope)
        put_row([put_scope(sub_scopes_dict['card']), None, put_scope(sub_scopes_dict['value'])], scope=hand_scope)

    if len(cards_list) == 2:  # Differentiate first two and non-first-two cards.
        cards_descr = 'First two: '
        write_text(cards_descr + ', '.join(cards_list), scope=sub_scopes_dict['card'])

    else:
        cards_descr = 'New drawn: '
        write_text(cards_descr + cards_list[-1], scope=sub_scopes_dict['card'])  # Only take the last card from list.

    if blackjack:
        value = 'Blackjack'

    elif bust:
        value = 'Busted'

    else:
        if soft:
            value = str(value) + '/' + str(value - 10)

        else:
            value = str(value)

    clear_contents(sub_scopes_dict['value'])  # Clear value table.
    put_table([[value]], scope=sub_scopes_dict['value'])  # Update value.


# Display new drawn card and current value of dealer's hand.
def show_dealer_value(card, value=0, soft=False, bust=False, blackjack=False, player_all_blackjack=False, first=False):
    if blackjack:
        value = 'Blackjack'

    elif player_all_blackjack:  # If dealer has no Blackjack, and all hands from player are.
        value = 'No Blackjack'

    elif bust:
        value = 'Busted'

    else:
        if soft & (value < MIN_DEALER_VALUE):  # If hand is soft and under required value, show both possible values.
            value = str(value) + '/' + str(value - 10)

        else:
            value = str(value)

    if first:  # If is first card, create sub scopes in dealer scope.
        # First: a row of markdowns.
        put_row([put_markdown('Card'), None, put_markdown('Value')], scope=DEALER_SCOPE)
        # Second: a row of sub scopes for card and value, respectively.
        put_row([put_scope(DEALER_SUB_SCOPES['card']), None, put_scope(DEALER_SUB_SCOPES['value'])], scope=DEALER_SCOPE)

    cards_descr = 'First: ' if first else 'New drawn: '  # Differentiate first and non-first cards.
    write_text(cards_descr + card, scope=DEALER_SUB_SCOPES['card'])  # Show card.
    clear_contents(DEALER_SUB_SCOPES['value'])  # Clear value table.
    put_table([[value]], scope=DEALER_SUB_SCOPES['value'])  # Update value.
