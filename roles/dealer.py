from configs.rules_config import MIN_DEALER_VALUE
from configs.app_config import DEALER_SLEEP
from utils.judges import judge_blackjack
from utils.trackers import update_properties
from widgets.cards import show_dealer_value
import time


class Dealer:
    """Blackjack dealer."""

    def __init__(self):
        self.cards_list, self.suits_list, self.value = [], [], 0  # Hand value starts from 0.
        self.early_pay, self.blackjack, self.soft, self.bust = False, False, False, False  # Default marks are False.

    def prepare(self, first_card, first_suit):  # Load first card for a new round.
        self.cards_list.clear()  # Clear list before loading first card.
        self.cards_list.append(first_card)
        self.suits_list.clear()
        self.suits_list.append(first_suit)

        # If dealer may have Blackjack, early pay mode is on.
        self.early_pay = True if first_card in ['A', 'K', 'Q', 'J', '10'] else False
        self.blackjack = False  # Reset Blackjack mark back to False.
        self.value, self.soft, self.bust = update_properties(self.cards_list)

        show_dealer_value(first_card, first_suit, value=self.value, soft=self.soft, first=True)

    def add_to_17_plus(self, shuffle_machine_obj, check_blackjack_only=False):  # Dealer needs 17+ except special cases.
        while self.value < MIN_DEALER_VALUE:
            time.sleep(DEALER_SLEEP)  # Pause before drawing a new card.
            drawn_card, drawn_suit = shuffle_machine_obj.draw()
            self.cards_list.append(drawn_card)
            self.suits_list.append(drawn_suit)

            if judge_blackjack(self.cards_list):  # If dealer has Blackjack, stop drawing.
                self.blackjack = True  # Change Blackjack mark to True.
                show_dealer_value(drawn_card, drawn_suit, blackjack=self.blackjack)
                return

            # If dealer has no Blackjack, stop drawing in either of two cases.
            # 1. Player's hands are all Blackjack. 2. Player's hands are all busted but have insurance.
            if check_blackjack_only:
                show_dealer_value(drawn_card, drawn_suit, check_bj_only=check_blackjack_only)
                return

            self.value, self.soft, self.bust = update_properties(self.cards_list)
            if self.bust:  # If dealer is busted, set value as 0 for chips calculation convenience.
                self.value = 0
                show_dealer_value(drawn_card, drawn_suit, bust=self.bust)
                return  # Stop drawing here.

            show_dealer_value(drawn_card, drawn_suit, value=self.value, soft=self.soft)
