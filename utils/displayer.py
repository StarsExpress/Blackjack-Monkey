from config import MINIMUM_BET, MAXIMUM_CAPITAL, INITIAL_HANDS_MAXIMUM, MAXIMUM_BET
from colors import Colors
from utils.properties_tracker import track_properties


def show_app_invalid_input(not_digit=False, below_minimum=False, over_maximum=False, remaining_capital=0,
                           get_broke=False, invalid_hands=False, invalid_choice=False):
    # Print corresponding messages if invalid input happens in app.py.
    if not_digit:
        print(Colors.yellow + 'Input is not integer.' + Colors.default + '\n')
    if below_minimum:
        print(Colors.yellow + 'Capital must >= minimum bet (' + str(MINIMUM_BET) + ').' + Colors.default + '\n')
    if over_maximum:
        print(Colors.yellow + 'Capital must <= maximum capital (' + str(MAXIMUM_CAPITAL) + ').' + Colors.default + '\n')
    if invalid_hands:
        print(Colors.yellow + 'Total hands must >= 1 & <= ' + str(INITIAL_HANDS_MAXIMUM) + '.' + Colors.default + '\n')
    if get_broke:
        print(Colors.yellow + 'Your remaining capital ' + str(remaining_capital) + ' dollars < minimum bet '
              + str(MINIMUM_BET) + ', so the game must end here.' + Colors.default + '\nSee you next time~\n')
    if invalid_choice:
        print(Colors.yellow + 'Invalid choice. Please enter again.' + Colors.default + '\n')
    return


def show_game_invalid_input(not_digit=False, below_minimum=False, remaining_capital=0, over_capital=False,
                            over_maximum=False, not_100_multiple=False, invalid_option=False, invalid_action=False):
    # Print corresponding messages if invalid input happens in game.py.
    if not_digit:
        print(Colors.yellow + 'Input is not integer.' + Colors.default + '\n')
    if below_minimum:
        print(Colors.yellow + 'Input must >= minimum bet (' + str(MINIMUM_BET) + ').' + Colors.default + '\n')
    if over_capital:
        print(Colors.yellow + 'Your remaining capital is ' + str(remaining_capital) +
              '. Put an amount not higher than it.' + Colors.default + '\n')
    if over_maximum:
        print(Colors.yellow + 'Input must <= maximum bet (' + str(MAXIMUM_BET) + ').' + Colors.default + '\n')
    if not_100_multiple:
        print(Colors.yellow + 'Input must be 100' + "'" + 's multiple.' + Colors.default + '\n')
    if invalid_option:
        print(Colors.yellow + 'Invalid option. Please enter again.' + Colors.default + '\n')
    if invalid_action:
        print(Colors.yellow + 'Invalid action. Please enter again.' + Colors.default + '\n')
    return


def show_out_of_money(remaining_capital):  # Display out of money message.
    print(Colors.yellow + 'Your remaining capital (' + str(remaining_capital) + ' dollars) < minimum bet ('
          + str(MINIMUM_BET) + ' dollars), so no more hands allowed.' + Colors.default + '\n')
    return


def show_cards(head_ordinal, branch_ordinal, cards_list, split=False):  # Display input hand's cards.
    if split:  # If the input hand is from split.
        print('Hand ' + head_ordinal + "'" + 's branch hand ' + branch_ordinal + ': ' + ', '.join(cards_list) + '.')
        return
    print('Hand ' + head_ordinal + ': ' + ', '.join(cards_list) + '.')
    return


# Display input hand's value.
def show_value(double_down, stand, value, soft, ordinary_21=False, blackjack=False, split_aces=False):
    if blackjack:  # If the hand is Blackjack.
        print('Your hand is a Blackjack!\n')
        return

    if True in [stand, double_down, ordinary_21, split_aces]:  # If any of the four conditions is met.
        print('Final value is ' + str(value) + '.\n')
        return

    if soft:  # If the hand is soft.
        print('Total value: ' + str(value) + ' or ' + str(value - 10) + '.\n')
        return
    print('Total value: ' + str(value) + '.\n')
    return


# Display input hand's actions.
def show_actions(head_ordinal, branch_ordinal, cards_list, remaining_capital, initial_bet, split):
    value, soft = track_properties(cards_list, True)  # Input hand's value and soft properties.
    value_message = str(value) + ' or ' + str(value - 10) if soft else str(value)

    # If the input hand is from split, add branch hand message.
    branch_message = "'" + 's ' + 'branch hand ' + str(branch_ordinal) if split else ''

    disabled_message = ''  # If remaining capital < initial bet, write that double down and split are disabled.
    if remaining_capital < initial_bet:
        disabled_message = ' < initial bet ' + str(initial_bet) + ' dollars, so double down and split are disabled now'

    print('Hand ' + head_ordinal + branch_message + ' now at: ' + ', '.join(cards_list) + '; value = ' + value_message
          + '.\nRemaining capital: ' + str(remaining_capital) + ' dollars' + disabled_message + '. Your action:'
          + ' (enter integer to choose)')
    return


def show_early_pay(head_ordinal):  # Display input hand's Blackjack early pay options.
    print('Dealer might have Blackjack. Does your hand ' + head_ordinal +
          ' want early pay or wait to the end:' + ' (enter integer to choose)')
    return


def show_result(head_ordinal, branch_ordinal, returned_chips, initial_chips,
                split=False, double_down=False, reason=None):  # Display total profit or loss by each hand.
    # If the input hand is from split, add branch hand message.
    branch_hand_message = "'" + 's ' + 'branch hand ' + str(branch_ordinal) if split else ''
    double_down_multiple = 1 if double_down else 0  # The additional double down amount to be dealt with,

    if returned_chips >= initial_chips:  # If player has profit.
        profit_loss_message = ' profit is ' + str(returned_chips - initial_chips * (1 + double_down_multiple))
        color = Colors.red  # Text color is red.

    else:  # If player has loss.
        profit_loss_message = ' loss is ' + str(initial_chips * (1 + double_down_multiple) - returned_chips)
        color = Colors.green  # Text color is green.

    reason = '' if reason is None else reason  # If reason is None, leave it as an empty string.
    print(color + 'Your hand ' + head_ordinal + branch_hand_message + profit_loss_message
          + ' dollars' + str(reason) + '.' + Colors.default + '\n')
    return


if __name__ == '__main__':
    show_value(True, True, 20, False, ordinary_21=False)
    show_actions('1', '1', ['2', 'A', '7'], 500, 500, 0)
    show_result('3', '1', 0, 400, False, True)
