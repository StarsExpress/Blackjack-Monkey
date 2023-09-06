from configs.output_config import PLAYER_SCOPE, PLAYER_SUB_SCOPES, DEALER_SCOPE, DEALER_SUB_SCOPES, SHARED_HEIGHT
from utils.swiss_knife import find_ordinal_text, find_value_color
from utils.trackers import track_display_value
from widgets.layouts import clear_contents
from pywebio.output import put_collapse, put_scrollable, put_row, put_markdown, put_scope, put_table


# Display new drawn card and current value of player's hand.
def show_player_value(head_ordinal, branch_ordinal, cards_list, value=0, chips=0, blackjack=False, stand=False,
                      soft=False, bust=False, first_split=False, new_branch=False, value_only=False, double_down=False):
    tab_scope = f'{PLAYER_SCOPE}_{head_ordinal}'  # Tab to which input hand belongs.
    branch_scope = f'{tab_scope}_{branch_ordinal}'  # Branch scope for input hand.

    chips_scope = f"{branch_scope}_{PLAYER_SUB_SCOPES['chips']}"  # Chips, card and value scopes inside branch scope.
    cards_scope = f"{branch_scope}_{PLAYER_SUB_SCOPES['cards']}"
    value_scope = f"{branch_scope}_{PLAYER_SUB_SCOPES['value']}"

    if first_split:  # When a branch hand commits 1st split.
        clear_contents(cards_scope)

    value_color = find_value_color(value, soft, bust)  # Display value is string, so find color first.
    value = track_display_value(value=value, blackjack=blackjack, stand=stand, soft=soft, bust=bust)

    if new_branch:  # When a new branch hand has to be displayed.
        # Add new branch scope in tab scope.
        put_collapse(f'{find_ordinal_text(branch_ordinal)} Branch', put_scrollable(
            put_scope(branch_scope), height=SHARED_HEIGHT * 2 // 5), open=True, scope=tab_scope)

        # In new branch scope, set markdowns and three sub scopes.
        put_row([put_markdown('Bets Placed'), None, put_markdown('Cards'), None, put_markdown('Value')],
                scope=branch_scope)

        put_row([
            put_scope(chips_scope, put_table([[chips]], scope=chips_scope)),
            None,  # Middle blank.
            put_scope(cards_scope, put_table([cards_list], scope=cards_scope)),
            None,  # Middle blank.
            put_scope(value_scope, put_table([[value]], scope=value_scope).style(f'color:{value_color}'))
        ], scope=branch_scope)
        return

    clear_contents(value_scope)  # Erase old value for new value.
    put_table([[value]], scope=value_scope).style(f'color:{value_color}')
    if value_only:  # If chips and cards don't need updates.
        return

    if double_down:  # For double down, update placed chips. Erase old value for new value.
        clear_contents(chips_scope)
        put_table([[chips]], scope=chips_scope)

    # Display new drawn card(s): if not first two cards, only show the last card from list.
    cards_list = cards_list if len(cards_list) == 2 else cards_list[-1:]
    put_table([cards_list], scope=cards_scope)


# Display new drawn card and current value of dealer's hand.
def show_dealer_value(card, value=0, first=False, blackjack=False, player_all_bj=False, soft=False, bust=False):
    if first:  # If is first card, create sub scopes in dealer scope.
        put_row([put_markdown('Cards'), None, put_markdown('Value')], scope=DEALER_SCOPE)

        put_row([put_scope(DEALER_SUB_SCOPES['cards']), None, put_scope(DEALER_SUB_SCOPES['value'])],
                scope=DEALER_SCOPE)

    value_color = find_value_color(value, soft, bust)  # Display value is string, so find color first.
    value = track_display_value(value, blackjack, dealer=True, player_all_bj=player_all_bj, soft=soft, bust=bust)

    clear_contents(DEALER_SUB_SCOPES['value'])  # Erase old value for new value.
    put_table([[value]], scope=DEALER_SUB_SCOPES['value']).style(f'color:{value_color}')
    put_table([[card]], scope=DEALER_SUB_SCOPES['cards'])
