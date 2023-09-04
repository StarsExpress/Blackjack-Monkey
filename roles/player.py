from machines.hand_processor import HandProcessor


class Player:
    """Blackjack player."""

    def __init__(self):
        self.hands_dict, self.chips_dict = {}, {}  # Dictionaries of each hand's cards and placed chips.

    def prepare(self, chips_list, cards_list):  # Load chips and cards for a new round.
        self.hands_dict.clear()  # Clear dictionaries before loading values.
        self.chips_dict.clear()

        for i in range(len(chips_list)):  # Load chips and hands into dictionaries.
            self.chips_dict.update({str(i + 1): chips_list[i]})
            self.hands_dict.update({str(i + 1): HandProcessor(str(i + 1), chips_list[i], cards_list[i])})
            self.hands_dict[str(i + 1)].display_properties()
