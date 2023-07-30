from utils.judges import judge_surrender, judge_split


# Find eligible actions when player doesn't have Blackjack.
def find_eligible_actions(cards_list, dealer_first_card, splits, remaining_capital, initial_bet):
    actions_list = ['Stand', 'Hit']
    if judge_surrender(cards_list, dealer_first_card, splits):  # Check if surrender is allowed.
        actions_list = ['Surrender'] + actions_list

    if remaining_capital >= initial_bet:  # Check if double down and split are allowed, respectively.
        if len(cards_list) == 2:
            actions_list.append('Double Down')
        if judge_split(cards_list, splits):
            actions_list.append('Split')

    # Return eligible actions in string and a dictionary of strings as keys with actions as values.
    actions_str = ' '.join([str(i + 1) + '.' + actions_list[i] for i in range(len(actions_list))]) + ' '
    return actions_str, dict(zip([str(i + 1) for i in range(len(actions_list))], actions_list))


def offer_early_pay_option():  # Offer Blackjack early pay options.
    actions_list = ['Take', 'Wait']
    # Return eligible options in string and a dictionary of strings as keys with options as values.
    actions_str = ' '.join([str(i + 1) + '.' + actions_list[i] for i in range(len(actions_list))]) + ' '
    return actions_str, dict(zip([str(i + 1) for i in range(len(actions_list))], actions_list))


if __name__ == '__main__':
    print(find_eligible_actions(['A', 'A'], 'A', 0, 500, 600))
