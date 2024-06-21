from machines.hand_processor import HandProcessor


class Player:
    """
    A class to serve as Blackjack player.

    Attributes:
    hands_dict: dictionary of each hand's cards.

    Methods:
    prepare(chips_list: list[int], cards_and_suits_list: list[list[str]]): load cards for new round.

    update_insurance(insurance_hands_list: list[str]): update insurance marks of hands having insurance.
    """

    def __init__(self):
        self.hands_dict = {}

    def prepare(self, chips_list: list[int], cards_and_suits_list: list[list[str]]):
        self.hands_dict.clear()  # Clear dictionaries before loading values.

        for i in range(len(chips_list)):
            self.hands_dict.update(
                {
                    str(i + 1): HandProcessor(
                        str(i + 1),
                        chips_list[i],
                        cards_and_suits_list[i][:2],  # First 2 items are cards.
                        cards_and_suits_list[i][-2:],  # Last 2 items are suits.
                    )
                }
            )
            self.hands_dict[str(i + 1)].display_properties()

    def update_insurance(self, insurance_hands_list: list[str]):
        if len(insurance_hands_list) > 0:
            for insurance_head_ordinal in insurance_hands_list:
                self.hands_dict[insurance_head_ordinal].set_insurance_value()
