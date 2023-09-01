from configs.rules_config import MIN_DEALER_VALUE
from configs.output_config import DEALER_SCOPE, DEALER_SUB_SCOPES
from widgets.outputs import write_text, clear_contents
from pywebio.output import put_row, put_markdown, put_scope, put_table


def show_cards(head_ordinal, branch_ordinal, cards_list, split=False):  # Display input hand's cards.
    if split:  # If the input hand is from split.
        print('Hand ' + head_ordinal + "'" + 's branch hand ' + branch_ordinal + ': ' + ', '.join(cards_list) + '.')
        return
    print('Hand ' + head_ordinal + ': ' + ', '.join(cards_list) + '.')
    return


# Display new drawn card and current value of dealer's hand.
def show_dealer_value(card, value=0, soft=False, bust=False, blackjack=False, player_all_blackjack=False, first=False):
    text = 'First: ' if first else 'New drawn: '  # Differentiate first and non-first cards.

    if blackjack:  # If dealer has Blackjack.
        value = 'Blackjack'

    elif player_all_blackjack:  # If dealer has no Blackjack, and all hands from player are.
        value = 'No Blackjack'

    elif bust:  # If dealer is busted.
        value = 'Busted'

    else:
        if soft & (value < MIN_DEALER_VALUE):  # If dealer's hand is soft and still under required value.
            value = str(value) + '/' + str(value - 10)

        else:
            value = str(value)

    if first:  # If is first card.
        # First: a row of markdowns in dealer scope.
        put_row([put_markdown('Card'), None, put_markdown('Value')], scope=DEALER_SCOPE)
        # Second: a row of sub scopes for card and value, respectively, in dealer scope.
        put_row([put_scope(DEALER_SUB_SCOPES['card']), None, put_scope(DEALER_SUB_SCOPES['value'])], scope=DEALER_SCOPE)

    write_text(text + card, scope=DEALER_SUB_SCOPES['card'])  # Show card.
    clear_contents(DEALER_SUB_SCOPES['value'])  # Clear value table.
    put_table([[value]], scope=DEALER_SUB_SCOPES['value'])  # Update value.
