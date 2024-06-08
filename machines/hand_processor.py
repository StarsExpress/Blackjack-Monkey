from configs.rules_config import MAX_SPLITS
from utils.judges import judge_blackjack
from utils.trackers import update_properties
from widgets.cards import show_player_value
from widgets.notifications import remind_splits_rules


class HandProcessor:
    """Store card values and process surrender, stand, hit, double down and split for a given hand."""

    def __init__(self, head_ordinal: str, chips: int, cards_list: list[str], suits_list: list[str]):
        # Initial chips: amount placed at start. It helps track chips of "split" branches.
        self.head_ordinal, self.initial_chips, self.insurance, self.splits = head_ordinal, chips, 0, 0
        self.blackjack, self.surrendered = judge_blackjack(cards_list), False
        self.aces_pair = True if cards_list == ['A', 'A'] else False  # Aces pair mark.

        self.chips_dict, self.double_down_dict = {'1': chips}, {'1': False}
        self.cards_dict, self.suits_dict = {'1': cards_list}, {'1': suits_list}

        value, soft, bust = update_properties(cards_list)
        self.value_dict, self.soft_dict, self.bust_dict = {'1': value}, {'1': soft}, {'1': bust}

    def display_properties(self, branch_ordinal: str = '1'):
        show_player_value(self.head_ordinal, branch_ordinal, cards_list=self.cards_dict[branch_ordinal],
                          suits_list=self.suits_dict[branch_ordinal], value=self.value_dict[branch_ordinal],
                          chips=self.chips_dict[branch_ordinal], insurance=self.insurance, blackjack=self.blackjack,
                          soft=self.soft_dict[branch_ordinal], new_branch=True)

    def surrender(self):
        self.surrendered = True  # Turn surrendered mark to True.

    def set_insurance_value(self, branch_ordinal: str = '1'):
        self.insurance = self.chips_dict['1'] // 2  # Insurance amount is 50% of initially placed bet.
        show_player_value(self.head_ordinal, branch_ordinal, chips=self.chips_dict['1'],
                          insurance=self.insurance, update_chips=True, insurance_only=True)

    def stand(self, branch_ordinal: str = '1'):
        if self.soft_dict[branch_ordinal]:  # If the stood hand is soft, finalize its display value.
            show_player_value(self.head_ordinal, branch_ordinal, cards_list=self.cards_dict[branch_ordinal],
                              value=self.value_dict[branch_ordinal], value_only=True,
                              stand=True, soft=self.soft_dict[branch_ordinal])

    def hit_or_double_down(self, card: str, suit: str, branch_ordinal: str = '1', double_down: bool = False):
        self.cards_dict[branch_ordinal].append(card)  # Append a new card into the hand's list.
        self.suits_dict[branch_ordinal].append(suit)

        value, soft, bust = update_properties(self.cards_dict[branch_ordinal])
        self.value_dict[branch_ordinal] = value
        self.soft_dict[branch_ordinal], self.bust_dict[branch_ordinal] = soft, bust

        if double_down:  # If double down is selected, double chips and switch double down mark to True.
            self.chips_dict[branch_ordinal] *= 2
            self.double_down_dict[branch_ordinal] = True

        show_player_value(self.head_ordinal, branch_ordinal, cards_list=self.cards_dict[branch_ordinal],
                          suits_list=self.suits_dict[branch_ordinal], value=value, insurance=self.insurance,
                          stand=self.double_down_dict[branch_ordinal], soft=soft, bust=bust,
                          chips=self.chips_dict[branch_ordinal], update_chips=self.double_down_dict[branch_ordinal])

    def split(self, card: str, suit: str, branch_ordinal: str = '1'):
        stand = True if self.aces_pair else False  # If the hand is Aces pair, stand right after split.
        self.cards_dict[str(self.splits + 2)] = [self.cards_dict[branch_ordinal][-1]]  # Move split card to new branch.
        self.cards_dict[branch_ordinal] = [self.cards_dict[branch_ordinal][0], card]

        self.suits_dict[str(self.splits + 2)] = [self.suits_dict[branch_ordinal][-1]]
        self.suits_dict[branch_ordinal] = [self.suits_dict[branch_ordinal][0], suit]

        value, soft, bust = update_properties(self.cards_dict[branch_ordinal])
        self.value_dict[branch_ordinal] = value
        self.soft_dict[branch_ordinal], self.bust_dict[branch_ordinal] = soft, bust

        show_player_value(self.head_ordinal, branch_ordinal, cards_list=self.cards_dict[branch_ordinal],
                          suits_list=self.suits_dict[branch_ordinal], value=value,
                          stand=stand, soft=soft, first_split=True)

        self.splits += 1  # Add 1 to number of splits.
        if self.splits == MAX_SPLITS:
            remind_splits_rules(self.head_ordinal)

    def reload(self, card: str, suit: str, branch_ordinal: str = '1'):  # Branch ordinal: last branch with 2+ cards.
        branch_ordinal = str(int(branch_ordinal) + 1)  # Last "complete" branch's next ordinal = the new branch.
        if branch_ordinal not in self.cards_dict.keys():
            return

        self.chips_dict[branch_ordinal], self.double_down_dict[branch_ordinal] = self.initial_chips, False
        self.cards_dict[branch_ordinal].append(card)
        self.suits_dict[branch_ordinal].append(suit)

        value, soft, bust = update_properties(self.cards_dict[branch_ordinal])
        self.value_dict[branch_ordinal] = value
        self.soft_dict[branch_ordinal], self.bust_dict[branch_ordinal] = soft, bust

        stand = True if self.aces_pair else False  # If the hand is Aces pair, stand right after reloading.
        show_player_value(self.head_ordinal, branch_ordinal, cards_list=self.cards_dict[branch_ordinal],
                          suits_list=self.suits_dict[branch_ordinal], value=value,
                          chips=self.chips_dict[branch_ordinal], stand=stand, soft=soft, new_branch=True)
