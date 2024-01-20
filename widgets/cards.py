from configs.output_config import IMAGES_WIDTH, PLAYER_SCOPE, PLAYER_SUB_SCOPES, TABLE_HEADERS
from configs.output_config import DEALER_SCOPE, DEALER_SUB_SCOPES, SHARED_HEIGHT
from utils.swiss_knife import read_cards_images, find_ordinal_text, find_value_color
from utils.trackers import track_display_value
from widgets.layouts import clear_contents
from pywebio.output import put_collapse, put_scrollable, put_row, put_scope, put_table, put_image


cards_images_dict = read_cards_images()


# Display new drawn card and current value of player's hand.
def show_player_value(head_ordinal, branch_ordinal, cards_list=None, suits_list=None, value=0, chips=0, insurance=0,
                      blackjack=False, stand=False, soft=False, bust=False, first_split=False,
                      new_branch=False, value_only=False, update_chips=False, insurance_only=False):
    tab_scope = f'{PLAYER_SCOPE}_{head_ordinal}'  # Tab to which input hand belongs.
    branch_scope = f'{tab_scope}_{branch_ordinal}'  # Branch scope for input hand.
    chips_scope = f"{branch_scope}_{PLAYER_SUB_SCOPES['chips']}"

    if update_chips:  # Update placed chips. Erase old value for new value.
        clear_contents(chips_scope)
        put_table([[chips, insurance]], header=TABLE_HEADERS['chips'], scope=chips_scope)
        if insurance_only:  # If only chips need updates.
            return

    cards_scope = f"{branch_scope}_{PLAYER_SUB_SCOPES['cards']}"
    value_scope = f"{branch_scope}_{PLAYER_SUB_SCOPES['value']}"
    profit_scope = f"{branch_scope}_{PLAYER_SUB_SCOPES['profit']}"

    if first_split:  # When a branch hand commits 1st split.
        clear_contents(cards_scope)

    value_color = find_value_color(value, soft, bust)  # Display value is string, so find color first.
    value = track_display_value(value=value, blackjack=blackjack, stand=stand, soft=soft, bust=bust)

    if new_branch:  # When a new branch hand has to be displayed.
        # Add new branch scope in tab scope.
        put_collapse(f'{find_ordinal_text(branch_ordinal)} Branch', put_scrollable(
            put_scope(branch_scope), height=SHARED_HEIGHT // 2), open=True, scope=tab_scope)

        put_row([None,  # Edge blank.
                 put_scope(chips_scope, put_table([[chips, insurance]],
                                                  header=TABLE_HEADERS['chips'], scope=chips_scope)),
                 None,  # Middle blank.
                 None,  # Middle blank.
                 put_scope(cards_scope, [
                                     put_image(cards_images_dict[f'{cards_list[0]}{suits_list[0]}'],
                                               width=IMAGES_WIDTH, scope=cards_scope),
                                     put_image(cards_images_dict[f'{cards_list[1]}{suits_list[1]}'],
                                               width=IMAGES_WIDTH, scope=cards_scope)], scope=cards_scope),
                 None,  # Middle blank.
                 put_scope(value_scope, put_table([[value]], header=TABLE_HEADERS['value'],
                                                  scope=value_scope).style(f'color:{value_color}')),
                 put_scope(profit_scope, put_table([[0]], header=TABLE_HEADERS['profit'], scope=profit_scope))
                 ], scope=branch_scope)
        return

    clear_contents(value_scope)  # Erase old value for new value.
    put_table([[value]], header=TABLE_HEADERS['value'], scope=value_scope).style(f'color:{value_color}')
    if value_only:  # If chips and cards don't need updates.
        return

    # Display new drawn card(s): if not first two cards, only show the last card and its suit from list.
    if len(cards_list) != 2:
        put_image(cards_images_dict[f'{cards_list[-1]}{suits_list[-1]}'], width=IMAGES_WIDTH, scope=cards_scope)
        return

    for i in range(len(cards_list)):
        put_image(cards_images_dict[f'{cards_list[i]}{suits_list[i]}'], width=IMAGES_WIDTH, scope=cards_scope)


# Display new drawn card and current value of dealer's hand.
def show_dealer_value(card, suit, value=0, first=False, blackjack=False, check_bj_only=False, soft=False, bust=False):
    if first:  # If is first card, create sub scopes in dealer scope.
        put_row([put_scope(DEALER_SUB_SCOPES['cards']), None, put_scope(DEALER_SUB_SCOPES['value'])],
                scope=DEALER_SCOPE)

    value_color = find_value_color(value, soft, bust)  # Display value is string, so find color first.
    value = track_display_value(value, blackjack, dealer=True, check_bj_only=check_bj_only, soft=soft, bust=bust)

    clear_contents(DEALER_SUB_SCOPES['value'])  # Erase old value for new value.
    put_table([[value]], header=TABLE_HEADERS['value'], scope=DEALER_SUB_SCOPES['value']).style(f'color:{value_color}')
    put_image(cards_images_dict[f'{card}{suit}'], width=IMAGES_WIDTH, scope=DEALER_SUB_SCOPES['cards'])
