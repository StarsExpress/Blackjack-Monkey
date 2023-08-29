from machines.shuffle_machine import ShuffleMachine
from roles.dealer import Dealer


class BlackjackGame:
    """Blackjack game."""

    def __init__(self):
        self.machine, self.dealer, self.capital = ShuffleMachine(), Dealer(), 0

    def set_up(self, capital):  # Set up capital amount and shuffle machine before each round.self.capital
        self.capital = capital  # Remaining capital amount.
        self.machine.load_and_shuffle()  # Load and shuffle cards.
        self.dealer.prepare(self.machine.draw())  # Dealer and player preparations.
        self.dealer.add_to_17_plus(self.machine)
