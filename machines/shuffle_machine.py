from configs.rules_config import NUMBER_OF_DECKS, CARDS_LIST, SUITS_DICT
from copy import deepcopy
import random
from random import shuffle
from collections import Counter
import json


class ShuffleMachine:
    """
    A class to shuffle and draw cards.

    Attributes:
    cards_list: list of cards in shuffle machine.
    suits_dict: dictionary of suits for each card type.

    Methods:
    load_and_shuffle(): refill cards and shuffle them.
    draw(two_cards: bool = False): draw 1 or 2 cards from deck's front.
    show_cards_count(): print each card's count if cards list isn't empty.
    """

    def __init__(self):
        self.cards_list = []  # List of cards.
        self.suits_dict = {}  # Dictionary of suits for each card type.

    def load_and_shuffle(self):
        self.cards_list.clear()
        self.cards_list.extend(CARDS_LIST * NUMBER_OF_DECKS)
        shuffle(self.cards_list)  # Only cards list needs shuffling.

        self.suits_dict = deepcopy(SUITS_DICT)

    def draw(self, two_cards: bool = False):
        if two_cards:  # If two cards are needed.
            card_1 = self.cards_list.pop(0)
            card_2 = self.cards_list.pop(0)
            suit_1 = self.suits_dict[card_1].pop(random.randrange(len(self.suits_dict[card_1])))
            suit_2 = self.suits_dict[card_2].pop(random.randrange(len(self.suits_dict[card_2])))

            return card_1, card_2, suit_1, suit_2

        card = self.cards_list.pop(0)
        suit = self.suits_dict[card].pop(random.randrange(len(self.suits_dict[card])))
        return card, suit

    def show_cards_count(self):
        if len(self.cards_list) <= 0:
            print('No loaded cards yet.')
            return
        cards_dict = dict(sorted(dict(Counter(self.cards_list)).items()))
        print(json.dumps(cards_dict, indent=2))
