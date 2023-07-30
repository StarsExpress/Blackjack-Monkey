from config import DEALER_VALUE_MINIMUM
from utils.judges import judge_blackjack
from utils.properties_tracker import track_properties
from utils.displayer import show_value


class Dealer:
    """Blackjack dealer."""

    def __init__(self):
        self.cards_list, self.value = None, 0  # Hand value starts from 0.
        # Four default marks are False.
        self.blackjack, self.ordinary_21, self.soft, self.bust = False, False, False, False

    def prepare(self, first_card):  # Load first card for a new round. Reset default marks back to False.
        self.cards_list, self.value = [first_card], 0
        self.blackjack, self.ordinary_21, self.soft, self.bust = False, False, False, False

        additional_message = 'No surrender allowed against Ace.\n' if first_card == 'A' else ''  # If first card is Ace.
        print('\nDealer' + "'" + 's first card: ' + first_card + '.\n' + additional_message)

    def add_to_17_plus(self, shuffle_machine_obj, player_all_blackjack=False):  # Dealer needs 17+ except special cases.
        print('\n')  # Print a space line.
        while self.value < DEALER_VALUE_MINIMUM:
            drawn_card = shuffle_machine_obj.draw()
            self.cards_list.append(drawn_card)
            print('Dealer' + "'" + 's new drawn card: ' + drawn_card + '.')

            if judge_blackjack(self.cards_list):  # If dealer has Blackjack, return entire attribute.
                self.blackjack = True  # Change Blackjack mark to True.
                print('Dealer has Blackjack.\n\n')
                return

            if player_all_blackjack:  # If player's hands are all Blackjack and dealer's isn't, return entire attribute.
                print('Dealer has no Blackjack.\n\n')
                return

            self.ordinary_21, self.value, self.soft, self.bust = track_properties(self.cards_list)
            if self.ordinary_21:  # If dealer has 21, return entire attribute.
                print('Dealer' + "'" + 's final value: 21.\n\n')
                return

            show_value(False, False, self.value, self.soft, self.ordinary_21)
            if self.bust:  # If dealer is busted, return entire attribute.
                print('Dealer is busted.\n\n')
                return

        print('Dealer' + "'" + 's final value: ' + str(self.value) + '.\n\n')


if __name__ == '__main__':
    from machines.shuffle_machine import ShuffleMachine

    machine_main = ShuffleMachine()
    machine_main.load_and_shuffle()
    dealer_main = Dealer()
    dealer_main.prepare(machine_main.draw())
    dealer_main.add_to_17_plus(machine_main, True)
