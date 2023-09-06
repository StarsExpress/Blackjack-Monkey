from machines.hand_processor import HandProcessor


class Player:
    """Blackjack player."""

    def __init__(self):
        self.hands_dict = {}  # Dictionary of each hand's cards.

    def prepare(self, chips_list, cards_list):  # Load cards for a new round.
        self.hands_dict.clear()  # Clear dictionaries before loading values.

        for i in range(len(chips_list)):
            self.hands_dict.update({str(i + 1): HandProcessor(str(i + 1), chips_list[i], cards_list[i])})
            self.hands_dict[str(i + 1)].display_properties()
