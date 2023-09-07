from configs.rules_config import MIN_DEALER_VALUE
from configs.app_config import DEALER_SLEEP
from utils.judges import judge_blackjack
from utils.trackers import update_properties
from widgets.cards import show_dealer_value
import time


class Dealer:
    """Blackjack dealer."""

    def __init__(self):
        self.cards_list, self.value = [], 0  # Hand value starts from 0.
        self.blackjack, self.soft, self.bust = False, False, False  # Three default marks are False.

    def prepare(self, first_card):  # Load first card for a new round.
        self.cards_list.clear()  # Clear list before loading first card.
        self.cards_list.append(first_card)

        self.blackjack = False  # Reset Blackjack mark back to False.
        self.value, self.soft, self.bust = update_properties(self.cards_list, False)

        # ace_text = 'No surrender allowed against Ace.' if first_card == 'A' else ''  # If first card is Ace.
        show_dealer_value(first_card, value=self.value, soft=self.soft, first=True)

    def add_to_17_plus(self, shuffle_machine_obj, player_all_blackjack=False):  # Dealer needs 17+ except special cases.
        while self.value < MIN_DEALER_VALUE:
            time.sleep(DEALER_SLEEP)  # Pause before drawing a new card.
            drawn_card = shuffle_machine_obj.draw()
            self.cards_list.append(drawn_card)

            if judge_blackjack(self.cards_list):  # If dealer has Blackjack, end loop here.
                self.blackjack = True  # Change Blackjack mark to True.
                show_dealer_value(drawn_card, blackjack=self.blackjack)
                return

            if player_all_blackjack:  # If player's hands are all Blackjack and dealer's isn't, end loop here.
                show_dealer_value(drawn_card, player_all_bj=player_all_blackjack)
                return

            self.value, self.soft, self.bust = update_properties(self.cards_list, False)
            if self.bust:  # If dealer is busted, set value as 0 for chips calculation convenience.
                self.value = 0
                show_dealer_value(drawn_card, bust=self.bust)
                return  # End loop here.

            show_dealer_value(drawn_card, value=self.value, soft=self.soft)
