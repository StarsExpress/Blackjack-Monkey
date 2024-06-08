from machines.hand_processor import HandProcessor


class Player:
    """Blackjack player."""

    def __init__(self):
        self.hands_dict = {}  # Dictionary of each hand's cards.

    def prepare(self, chips_list: list[int], cards_and_suits_list: list[list[str]]):  # Load cards for new round.
        self.hands_dict.clear()  # Clear dictionaries before loading values.

        for i in range(len(chips_list)):
            # Each list of cards_and_suits_list: first 2 items are cards; last 2 are respective suits.
            self.hands_dict.update({str(i + 1): HandProcessor(str(i + 1), chips_list[i], cards_and_suits_list[i][:2],
                                                              cards_and_suits_list[i][-2:])})
            self.hands_dict[str(i + 1)].display_properties()

    def update_insurance(self, insurance_hands_list: list[str]):  # Update insurance marks of hands having insurance.
        if len(insurance_hands_list) > 0:
            for insurance_head_ordinal in insurance_hands_list:
                self.hands_dict[insurance_head_ordinal].set_insurance_value()
