from configs.rules_config import NUMBER_OF_DECKS, CARDS_LIST, SUITS_DICT
from copy import deepcopy
import random
from random import shuffle
from collections import Counter
import json


class ShuffleMachine:
    """Shuffles and draws cards."""

    def __init__(self):
        self.cards_list = []  # List of cards.
        self.suits_dict = {}  # Dictionary of suits for each card type.

    def load_and_shuffle(self):  # Clear list and dictionary before loading all decks of cards into machine.
        self.cards_list.clear()
        self.cards_list.extend(CARDS_LIST * NUMBER_OF_DECKS)
        shuffle(self.cards_list)  # Only cards list needs shuffling.

        self.suits_dict = deepcopy(SUITS_DICT)

    def draw(self, two_cards=False):  # Draw from front at index 0.
        if two_cards:  # If two cards are needed.
            card_1 = self.cards_list.pop(0)
            card_2 = self.cards_list.pop(0)
            suit_1 = self.suits_dict[card_1].pop(random.randrange(len(self.suits_dict[card_1])))
            suit_2 = self.suits_dict[card_2].pop(random.randrange(len(self.suits_dict[card_2])))

            return card_1, card_2, suit_1, suit_2

        card = self.cards_list.pop(0)
        suit = self.suits_dict[card].pop(random.randrange(len(self.suits_dict[card])))
        return card, suit

    def show_cards_count(self):  # Print each card's count if list is not empty.
        if len(self.cards_list) <= 0:
            print('No loaded cards yet.')
            return
        cards_dict = dict(sorted(dict(Counter(self.cards_list)).items()))
        print(json.dumps(cards_dict, indent=2))
