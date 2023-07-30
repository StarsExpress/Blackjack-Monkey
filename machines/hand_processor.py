from config import SPLITS_MAXIMUM
from utils.judges import judge_blackjack
from utils.properties_tracker import track_properties
from utils.displayer import show_cards, show_value


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

    def print_properties(self, hand_ordinal='1'):
        show_cards(self.head_hand_ordinal, hand_ordinal, self.cards_dict[hand_ordinal])
        show_value(self.double_down_dict[hand_ordinal], False, self.value_dict[hand_ordinal],
                   self.soft_dict[hand_ordinal], self.ordinary_21_dict[hand_ordinal], self.blackjack)

    def surrender(self):
        self.surrendered = True  # Turn surrendered mark to True.
        print('Hand ' + self.head_hand_ordinal + ' has surrendered.\n')

    def stand(self, hand_ordinal='1', split_mark=False):
        show_cards(self.head_hand_ordinal, hand_ordinal, self.cards_dict[hand_ordinal], split_mark)
        show_value(False, True, self.value_dict[hand_ordinal], self.soft_dict[hand_ordinal])

    def hit_or_double_down(self, card, hand_ordinal='1', double_down=False, split_mark=False):
        if double_down:  # If double down is selected.
            self.double_down_dict[hand_ordinal] = True  # Switch double down mark to True.

        self.cards_dict[hand_ordinal].append(card)  # Append a new card into the hand's list.
        ordinary_21, value, soft, bust = track_properties(self.cards_dict[hand_ordinal])  # Judge hand properties.
        show_cards(self.head_hand_ordinal, hand_ordinal, self.cards_dict[hand_ordinal], split_mark)
        show_value(double_down, False, value, soft, ordinary_21)

        if bust:
            print('Your hand is busted.\n')

        self.ordinary_21_dict[hand_ordinal], self.value_dict[hand_ordinal] = ordinary_21, value  # Update properties.
        self.soft_dict[hand_ordinal], self.bust_dict[hand_ordinal] = soft, bust

    def split(self, card, hand_ordinal):
        if self.aces_pair:
            print('\nAces pair can split just once, and no hits or double down allowed after splitting Aces.\n')

        self.cards_dict[str(self.splits + 2)] = [self.cards_dict[hand_ordinal][-1]]  # Move the split card to new hand.
        self.cards_dict[hand_ordinal] = [self.cards_dict[hand_ordinal][0], card]

        ordinary_21, value, soft, bust = track_properties(self.cards_dict[hand_ordinal])  # Judge hand properties.
        self.ordinary_21_dict[hand_ordinal] = ordinary_21  # Update new hand's properties.
        self.value_dict[hand_ordinal], self.soft_dict[hand_ordinal], self.bust_dict[hand_ordinal] = value, soft, bust

        show_cards(self.head_hand_ordinal, hand_ordinal, self.cards_dict[hand_ordinal], True)
        show_value(False, False, value, soft, ordinary_21, split_aces=self.aces_pair)

        self.splits += 1  # Add 1 to number of splits.
        if self.splits == 3:  # If number of splits just reaches maximum.
            print('Your hand just reached ' + str(SPLITS_MAXIMUM) + ' splits and no more splits allowed.\n')

    def reload(self, card, hand_ordinal):  # Argument hand ordinal is the last "complete" hand's ordinal.
        hand_ordinal = str(int(hand_ordinal) + 1)  # The last "complete" hand's next ordinal is new hand's ordinal.
        if hand_ordinal not in self.cards_dict.keys():  # If new hand ordinal not among cards dictionary keys, return.
            return

        self.cards_dict[hand_ordinal].append(card)  # Update lists of cards, carriers and values for new hand.
        ordinary_21, value, soft, bust = track_properties(self.cards_dict[hand_ordinal])  # Judge hand properties.
        self.ordinary_21_dict[hand_ordinal] = ordinary_21  # Update new hand's properties.
        self.value_dict[hand_ordinal], self.soft_dict[hand_ordinal], self.bust_dict[hand_ordinal] = value, soft, bust
        self.double_down_dict[hand_ordinal] = False  # Default double down mark is False.

        show_cards(self.head_hand_ordinal, hand_ordinal, self.cards_dict[hand_ordinal], True)
        show_value(False, False, value, soft, ordinary_21, split_aces=self.aces_pair)


if __name__ == '__main__':
    processor_main = HandProcessor('3', ['8', '8'])
    processor_main.print_properties()
    processor_main.split('A', '1')
    processor_main.reload('8', '1')
    processor_main.split('10', '2')
