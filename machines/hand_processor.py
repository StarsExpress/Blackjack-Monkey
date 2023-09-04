from configs.rules_config import MAX_SPLITS
from utils.judges import judge_blackjack
from utils.trackers import track_properties
from widgets.cards import show_player_value


class HandProcessor:
    """Store card values and process surrender, stand, hit, double down and split for a given hand."""

    def __init__(self, head_hand_ordinal, cards_list):
        self.blackjack, self.early_pay = judge_blackjack(cards_list), False  # Blackjack and early pay mark.
        self.surrendered = False  # Surrendered mark.
        self.head_hand_ordinal, self.splits = head_hand_ordinal, 0  # Splits count and head hand ordinal.
        self.aces_pair = True if cards_list == ['A', 'A'] else False  # Aces pair mark.

        ordinary_21, value, soft, bust = track_properties(cards_list)  # Judge hand properties.
        self.cards_dict, self.double_down_dict = {'1': cards_list}, {'1': False}  # Property dictionaries of all hands.
        self.ordinary_21_dict, self.value_dict = {'1': ordinary_21}, {'1': value}
        self.soft_dict, self.bust_dict = {'1': soft}, {'1': bust}

    def display_properties(self, hand_ordinal='1'):
        show_player_value(self.head_hand_ordinal, hand_ordinal, self.cards_dict[hand_ordinal],
                          blackjack=self.blackjack, value=self.value_dict[hand_ordinal],
                          soft=self.soft_dict[hand_ordinal], new_branch=True)

    def surrender(self):
        self.surrendered = True  # Turn surrendered mark to True.

    def stand(self, hand_ordinal='1'):
        if self.soft_dict[hand_ordinal]:  # If the stood hand is soft, finalize its display value.
            show_player_value(self.head_hand_ordinal, hand_ordinal, self.cards_dict[hand_ordinal],
                              value=self.value_dict[hand_ordinal], stand=True, soft=self.soft_dict[hand_ordinal])

    def hit_or_double_down(self, card, hand_ordinal='1', double_down=False):
        self.cards_dict[hand_ordinal].append(card)  # Append a new card into the hand's list.
        ordinary_21, value, soft, bust = track_properties(self.cards_dict[hand_ordinal])  # Judge hand properties.

        if double_down:  # If double down is selected, switch double down mark to True.
            self.double_down_dict[hand_ordinal] = True
        self.ordinary_21_dict[hand_ordinal], self.value_dict[hand_ordinal] = ordinary_21, value  # Update properties.
        self.soft_dict[hand_ordinal], self.bust_dict[hand_ordinal] = soft, bust

        show_player_value(self.head_hand_ordinal, hand_ordinal, self.cards_dict[hand_ordinal], value=value,
                          stand=self.double_down_dict[hand_ordinal], soft=soft, bust=bust)

    def split(self, card, hand_ordinal='1'):
        stand = True if self.aces_pair else False  # If the hand is Aces pair, stand right after split.

        # # Write notifications here.
        # print('\nAces pair can split just once, and no hits or double down allowed after splitting Aces.\n')

        self.cards_dict[str(self.splits + 2)] = [self.cards_dict[hand_ordinal][-1]]  # Move the split card to new hand.
        self.cards_dict[hand_ordinal] = [self.cards_dict[hand_ordinal][0], card]

        ordinary_21, value, soft, bust = track_properties(self.cards_dict[hand_ordinal])  # Judge hand properties.
        self.ordinary_21_dict[hand_ordinal] = ordinary_21  # Update new hand's properties.
        self.value_dict[hand_ordinal], self.soft_dict[hand_ordinal], self.bust_dict[hand_ordinal] = value, soft, bust

        show_player_value(self.head_hand_ordinal, hand_ordinal, self.cards_dict[hand_ordinal],
                          value=value, stand=stand, soft=soft, clear=True)

        self.splits += 1  # Add 1 to number of splits.
        if self.splits == 3:  # If reaches maximum.
            pass
            # # Write notifications here.
            # print('Your hand just reached ' + str(MAX_SPLITS) + ' splits and no more splits allowed.\n')

    def reload(self, card, hand_ordinal):  # Argument hand ordinal is the last "complete" hand's ordinal.
        stand = True if self.aces_pair else False

        hand_ordinal = str(int(hand_ordinal) + 1)  # The last "complete" hand's next ordinal is new hand's ordinal.
        if hand_ordinal not in self.cards_dict.keys():  # If new hand ordinal not among cards dictionary keys, return.
            return

        self.cards_dict[hand_ordinal].append(card)  # Update lists of cards, carriers and values for new hand.

        ordinary_21, value, soft, bust = track_properties(self.cards_dict[hand_ordinal])  # Judge hand properties.
        self.ordinary_21_dict[hand_ordinal] = ordinary_21  # Update new hand's properties.
        self.value_dict[hand_ordinal], self.soft_dict[hand_ordinal], self.bust_dict[hand_ordinal] = value, soft, bust
        self.double_down_dict[hand_ordinal] = False  # Default double down mark is False.

        show_player_value(self.head_hand_ordinal, hand_ordinal, self.cards_dict[hand_ordinal],
                          value=value, stand=stand, soft=soft, new_branch=True)
