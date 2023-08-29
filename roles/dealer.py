from configs.output_config import DEALER_SCOPE
from configs.game_config import MIN_DEALER_VALUE
from utils.judges import judge_blackjack
from utils.tracker import show_properties, show_value
from pywebio.output import use_scope, put_text


class Dealer:
    """Blackjack dealer."""

    def __init__(self):
        self.cards_list, self.value = None, 0  # Hand value starts from 0.
        # Four default marks are False.
        self.blackjack, self.ordinary_21, self.soft, self.bust = False, False, False, False

    def prepare(self, first_card):  # Load first card for a new round. Reset default marks back to False.
        self.cards_list, self.value = [first_card], 0
        self.blackjack, self.ordinary_21, self.soft, self.bust = False, False, False, False

        additional_message = 'No surrender allowed against Ace.' if first_card == 'A' else ''  # If first card is Ace.
        with use_scope(DEALER_SCOPE):  # For first card, declare the scope to use.
            put_text("Dealer's first card: " + first_card + '. ' + additional_message)

    def add_to_17_plus(self, shuffle_machine_obj, player_all_blackjack=False):  # Dealer needs 17+ except special cases.
        while self.value < MIN_DEALER_VALUE:
            drawn_card = shuffle_machine_obj.draw()
            self.cards_list.append(drawn_card)

            drawn_card_message = "Dealer's new drawn card: " + drawn_card + '. '

            if judge_blackjack(self.cards_list):  # If dealer has Blackjack, return entire attribute.
                self.blackjack = True  # Change Blackjack mark to True.
                put_text(drawn_card_message + 'Dealer has Blackjack.', scope=DEALER_SCOPE)
                return

            if player_all_blackjack:  # If player's hands are all Blackjack and dealer's isn't, return entire attribute.
                put_text(drawn_card_message + 'Dealer has no Blackjack.', scope=DEALER_SCOPE)
                return

            self.ordinary_21, self.value, self.soft, self.bust = show_properties(self.cards_list)
            if self.ordinary_21:  # If dealer has 21, return entire attribute.
                put_text(drawn_card_message + 'Dealer' + "'" + 's final value: 21.', scope=DEALER_SCOPE)
                return

            if self.bust:  # If dealer is busted, return entire attribute.
                put_text(drawn_card_message + 'Dealer is busted.', scope=DEALER_SCOPE)
                return

            total_value_message = show_value(False, False, self.value, self.soft, self.ordinary_21)
            put_text(drawn_card_message + total_value_message, scope=DEALER_SCOPE)

        put_text("Dealer's final value: " + str(self.value) + '.', scope=DEALER_SCOPE)
