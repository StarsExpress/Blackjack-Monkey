from machines.hand_processor import HandProcessor


class Player:
    """Blackjack player."""

    def __init__(self):
        self.hands_dict, self.chips_dict = None, None

    def prepare(self, chips_list, cards_list):  # Load chips and cards for a new round.
        num_set = sorted(set(map(str, set(range(1, len(chips_list) + 1)))))  # Set from 1 to number of initial hands.
        self.chips_dict = dict(zip(num_set, chips_list))  # Dictionary of each hand's initial chips.

        # Dictionary of each hand's cards.
        hands_processors_list = [HandProcessor(num_set[i], cards_list[i]) for i in range(len(chips_list))]
        self.hands_dict = {num_set[i]: hands_processors_list[i] for i in range(len(chips_list))}

        for key in list(self.hands_dict.keys()):  # Display each hand's properties.
            self.hands_dict[key].display_properties()
