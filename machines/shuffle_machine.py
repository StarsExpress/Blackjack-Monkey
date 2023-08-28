from configs.game_config import NUMBER_OF_DECKS, CARDS_LIST
from random import shuffle
from collections import Counter
import json


class ShuffleMachine:
    """Shuffles and draws cards."""

    def __init__(self):
        self.number_of_decks = NUMBER_OF_DECKS  # Number of decks of cards.
        self.cards_list = []  # List of cards.

    def load_and_shuffle(self):
        self.cards_list = CARDS_LIST * NUMBER_OF_DECKS  # Load all decks of cards into machine.
        shuffle(self.cards_list)  # Shuffle cards list.

    def draw(self, two_cards=False):
        if two_cards:  # If two cards are needed.
            card_1 = self.cards_list.pop(0)
            card_2 = self.cards_list.pop(0)
            return card_1, card_2  # Return the first two cards of cards list.
        return self.cards_list.pop(0)  # Return the first card of cards list.

    def show_cards_count(self):  # Print each card's count if list is not empty.
        if len(self.cards_list) <= 0:
            print('No loaded cards yet.')
            return
        cards_dict = dict(sorted(dict(Counter(self.cards_list)).items()))
        print(json.dumps(cards_dict, indent=2))


if __name__ == '__main__':
    machine_main = ShuffleMachine()
    machine_main.load_and_shuffle()
    print('Card counts after initialization:')
    machine_main.show_cards_count()
    print('\nDrawn card:', machine_main.draw(), '\nCard counts:')
    machine_main.show_cards_count()
    print('\nDrawn card:', machine_main.draw(), '\nCard counts:')
    machine_main.show_cards_count()
    print('\nDrawn card:', machine_main.draw(True), '\nCard counts:')
    machine_main.show_cards_count()
    machine_main.load_and_shuffle()
    print('\nCard counts after reload:')
    machine_main.show_cards_count()
