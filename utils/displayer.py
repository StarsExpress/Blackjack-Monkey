
# Return input hand's value.
def show_value(double_down, stand, value, soft, ordinary_21=False, blackjack=False, split_aces=False):
    if blackjack:  # If the hand is Blackjack.
        return 'Your hand is a Blackjack!'

    if True in [stand, double_down, ordinary_21, split_aces]:  # If any of the four conditions is met.
        return 'Final value is ' + str(value) + '.'

    if soft:  # If the hand is soft.
        return 'Total value: ' + str(value) + ' or ' + str(value - 10) + '.'

    return 'Total value: ' + str(value) + '.'


if __name__ == '__main__':
    print(show_value(True, True, 20, False, ordinary_21=False))
