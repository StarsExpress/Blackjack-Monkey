from configs.output_config import DEALER_SCOPE
from configs.game_config import MIN_DEALER_VALUE
from utils.judges import judge_blackjack
from utils.trackers import show_properties, show_value
from widgets.outputs import write_text


class Dealer:
    """Blackjack dealer."""

    def __init__(self):
        self.cards_list, self.value = None, 0  # Hand value starts from 0.
        # Four default marks are False.
        self.blackjack, self.ordinary_21, self.soft, self.bust = False, False, False, False

    def prepare(self, first_card):  # Load first card for a new round. Reset default marks back to False.
        self.cards_list, self.value = [first_card], 0
        self.blackjack, self.ordinary_21, self.soft, self.bust = False, False, False, False

        ace_text = 'No surrender allowed against Ace.' if first_card == 'A' else ''  # If first card is Ace.
        # For first card, declare the scope to use.
        write_text("Dealer's first card: " + first_card + '. ' + ace_text, DEALER_SCOPE, True)

    def add_to_17_plus(self, shuffle_machine_obj, player_all_blackjack=False):  # Dealer needs 17+ except special cases.
        while self.value < MIN_DEALER_VALUE:
            drawn_card = shuffle_machine_obj.draw()
            self.cards_list.append(drawn_card)

            drawn_card_text = "Dealer's new drawn card: " + drawn_card + '. '

            if judge_blackjack(self.cards_list):  # If dealer has Blackjack, return entire attribute.
                self.blackjack = True  # Change Blackjack mark to True.
                write_text(drawn_card_text + 'Dealer has Blackjack.', DEALER_SCOPE)
                return

            if player_all_blackjack:  # If player's hands are all Blackjack and dealer's isn't, return entire attribute.
                write_text(drawn_card_text + 'Dealer has no Blackjack.', DEALER_SCOPE)
                return

            self.ordinary_21, self.value, self.soft, self.bust = show_properties(self.cards_list)
            if self.ordinary_21:  # If dealer has 21, return entire attribute.
                write_text(drawn_card_text + 'Dealer' + "'" + 's final value: 21.', DEALER_SCOPE)
                return

            if self.bust:  # If dealer is busted, return entire attribute.
                write_text(drawn_card_text + 'Dealer is busted.', DEALER_SCOPE)
                return

            total_value_text = show_value(False, False, self.value, self.soft, self.ordinary_21)
            write_text(drawn_card_text + total_value_text, DEALER_SCOPE)

        write_text("Dealer's final value: " + str(self.value) + '.', DEALER_SCOPE)
