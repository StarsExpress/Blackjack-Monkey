from configs.rules_config import MIN_BET, MAX_BET, MAX_TOTAL_VALUE
from configs.input_config import DEFAULT_PLAYER_NAME, CHIPS_DICT
from utils.swiss_knife import remind_betting_amount
from widgets.layouts import set_cards_tabs
from widgets.interactions import get_chips, get_early_pay, get_action
from widgets.notifications import notify_inadequate_capital, update_cumulated_capital, notify_early_exit
from widgets.chips import return_chips
from machines.shuffle_machine import ShuffleMachine
from roles.dealer import Dealer
from roles.player import Player


class Blackjack:
    """Blackjack game."""

    def __init__(self):
        self.machine, self.dealer, self.player, self.capital = ShuffleMachine(), Dealer(), Player(), 0
        self.player_name = DEFAULT_PLAYER_NAME

    def check_chips(self, chips):  # Check if placed bets are valid.
        # PyWebIO's input validation function only accepts one argument.
        # Defined here to receive self.capital as an updating global variable.
        if chips < MIN_BET:
            return f'Placed chips must >= minimum bet {str(MIN_BET)}.'
        if chips > MAX_BET:
            return f'Placed chips must <= maximum bet {str(MAX_BET)}.'
        if chips > self.capital:
            return f'Placed chips must <= remaining capital {str(self.capital)}.'
        if chips % 100 != 0:
            return 'Placed chips must be in units of 100.'

    def set_up(self, head_hands, capital, player_name):
        self.capital = capital
        self.machine.load_and_shuffle()

        if player_name is not None:  # If player enters name, use it to replace the default name.
            self.player_name = player_name

        chips_list = []
        chips_dict = CHIPS_DICT.copy()  # Make a copy to prevent changing config's values.

        for i in range(head_hands):  # Iterate through all desired head hands.
            if self.capital < MIN_BET:  # If remaining capital isn't enough for another head hand.
                notify_inadequate_capital(self.capital, hands=True)
                break

            chips_dict.update({'label': f"{CHIPS_DICT['label']} {str(i + 1)}:"})
            # Update holder text with respect to remaining capital as maximal feasible bet.
            chips_dict.update({'holder': f"{CHIPS_DICT['holder']} {remind_betting_amount(self.capital)}"})

            chips = get_chips(chips_dict, self.check_chips)  # Pass validation function check_chips.
            self.capital -= chips  # Deduct chips amount from capital.
            chips_list.append(chips)
            update_cumulated_capital(self.player_name, self.capital)

        self.dealer.prepare(self.machine.draw())
        set_cards_tabs(head_hands)  # Place tabs for all hands, and deal cards to them.
        self.player.prepare(chips_list, [list(self.machine.draw(True)) for _ in range(len(chips_list))])

    def start(self):  # Start a new round.
        # Sort Blackjack hands from higher to lower ordinal.
        bj_hands_list = sorted(filter(lambda x: self.player.hands_dict[x].blackjack,
                                      self.player.hands_dict.keys()), reverse=True)

        vague_bj_hands_list = []  # Blackjack hands waiting for dealer's final value to get results.

        for bj_hand_ordinal in bj_hands_list:  # Iterate through all Blackjack head hands.
            if self.dealer.early_pay:  # If dealer has to check early pay.
                if get_early_pay(bj_hand_ordinal) == 'take':  # If player takes early pay.
                    self.capital += return_chips(bj_hand_ordinal, player_bj=True, early_pay=True,
                                                 chips=self.player.hands_dict[bj_hand_ordinal].initial_chips)
                    update_cumulated_capital(self.player_name, self.capital)
                    continue  # Go to next Blackjack head hand.

                vague_bj_hands_list += [bj_hand_ordinal]  # For non-early-pay, append to vague list.
                continue  # Go to next Blackjack head hand.

            # If dealer has 0 Blackjack chance.
            self.capital += return_chips(bj_hand_ordinal, player_bj=True,
                                         chips=self.player.hands_dict[bj_hand_ordinal].initial_chips)
            update_cumulated_capital(self.player_name, self.capital)

        non_bj_head_hands_list = sorted(filter(lambda x: self.player.hands_dict[x].blackjack is False,
                                               self.player.hands_dict.keys()))  # List of non-Blackjack head hands.

        if len(non_bj_head_hands_list) > 0:
            head_ordinal = non_bj_head_hands_list[0]  # Start from the lowest ordinal.

            while True:  # Iterate through all head hands.
                if head_ordinal not in non_bj_head_hands_list:
                    break  # If all head hands are played, end head iteration.

                head_hand_object = self.player.hands_dict[head_ordinal]  # Head hand object.
                initial_chips = self.player.hands_dict[head_ordinal].initial_chips  # Initial chips placed.

                branches_list = list(head_hand_object.cards_dict.keys())  # Branches of iterated head hand.
                branch_ordinal = '1'  # Start from 1st branch.

                while True:  # Iterate through all branches.
                    if branch_ordinal not in branches_list:
                        break  # If all branches are played, end branch iteration to go to next head.

                    action = get_action((head_ordinal, branch_ordinal),
                                        head_hand_object.cards_dict[branch_ordinal], self.dealer.cards_list[0],
                                        head_hand_object.splits, self.capital, initial_chips)

                    if action == 'surrender':
                        self.capital += return_chips(head_ordinal, chips=initial_chips, surrender=True)
                        update_cumulated_capital(self.player_name, self.capital)
                        head_hand_object.surrender()
                        break  # End branch iteration to go to next head.

                    if action in ['stand', 'double_down']:
                        if action == 'stand':
                            head_hand_object.stand(branch_ordinal)

                        if action == 'double_down':
                            self.capital -= initial_chips  # Deduct additional bet from capital.
                            update_cumulated_capital(self.player_name, self.capital)
                            head_hand_object.hit_or_double_down(self.machine.draw(), branch_ordinal, True)

                            if head_hand_object.bust_dict[branch_ordinal]:  # Display busted loss.
                                return_chips(head_ordinal, branch_ordinal=branch_ordinal, player_bust=True,
                                             chips=head_hand_object.chips_dict[branch_ordinal])

                        # For split branch, reload closest isolated branch and update list.
                        if head_hand_object.splits > 0:
                            head_hand_object.reload(self.machine.draw(), branch_ordinal)
                            branches_list = list(head_hand_object.cards_dict.keys())

                        if branch_ordinal == branches_list[-1]:
                            break  # For last branch, end branch iteration to go to next head.
                        # Otherwise, go to next branch.
                        branch_ordinal = branches_list[branches_list.index(branch_ordinal) + 1]

                    if action == 'hit':  # If hit is chosen.
                        head_hand_object.hit_or_double_down(self.machine.draw(), branch_ordinal)
                        bust_mark = head_hand_object.bust_dict[branch_ordinal]  # Busted mark of iterated branch.

                        # If busted or reaches 21 after hit.
                        if bust_mark | (head_hand_object.value_dict[branch_ordinal] == MAX_TOTAL_VALUE):
                            if bust_mark:  # Display busted loss.
                                return_chips(head_ordinal, branch_ordinal=branch_ordinal, player_bust=True,
                                             chips=head_hand_object.chips_dict[branch_ordinal])

                            # For split branch, reload closest isolated branch and update list.
                            if head_hand_object.splits > 0:
                                head_hand_object.reload(self.machine.draw(), branch_ordinal)
                                branches_list = list(head_hand_object.cards_dict.keys())

                            if branch_ordinal == branches_list[-1]:
                                break  # For last branch, end branch iteration to go to next head.
                            # Otherwise, go to next branch.
                            branch_ordinal = branches_list[branches_list.index(branch_ordinal) + 1]

                    if action == 'split':  # If split is chosen.
                        self.capital -= initial_chips  # Deduct additional bet from capital.
                        update_cumulated_capital(self.player_name, self.capital)

                        head_hand_object.split(self.machine.draw(), branch_ordinal)
                        if head_hand_object.aces_pair:  # If an Aces pair is being split.
                            head_hand_object.reload(self.machine.draw(), branch_ordinal)
                            break  # Reload 2nd branch and break branch iteration to go to next head.

                if head_ordinal == non_bj_head_hands_list[-1]:
                    break  # For the last head hand, end head iteration.
                # Otherwise, go to next head hand.
                head_ordinal = non_bj_head_hands_list[non_bj_head_hands_list.index(head_ordinal) + 1]

        # List of head hands with 1+ branch that isn't Blackjack, surrendered or busted.
        final_head_hands_list = [head_ordinal for head_ordinal in self.player.hands_dict.keys() if
                                 (self.player.hands_dict[head_ordinal].blackjack is False) &
                                 (self.player.hands_dict[head_ordinal].surrendered is False) &
                                 (list(self.player.hands_dict[head_ordinal].bust_dict.values()).count(False) > 0)]

        final_head_hands_list += vague_bj_hands_list  # Add non-early-paid Blackjack hands into final head hands list.
        if len(final_head_hands_list) == 0:  # If no remaining hands to be judged.
            notify_early_exit()
            return

        # Check if player's remaining hands are all Blackjack awaiting dealer's results.
        player_all_blackjack = True if (len(vague_bj_hands_list) == len(final_head_hands_list)) else False
        self.dealer.add_to_17_plus(self.machine, player_all_blackjack)

        for head_ordinal in final_head_hands_list:  # Iterate through all final head hands.
            head_hand_object = self.player.hands_dict[head_ordinal]  # Head hand object.
            branches_list = list(filter(lambda x: head_hand_object.bust_dict[x] is False,
                                        head_hand_object.cards_dict.keys()))  # List of branches that are not busted.

            for branch_ordinal in branches_list:  # Iterate through all branches.
                branch_chips = head_hand_object.chips_dict[branch_ordinal]
                branch_value = head_hand_object.value_dict[branch_ordinal]

                self.capital += return_chips(head_ordinal, branch_ordinal, branch_chips, False, False,
                                             head_hand_object.blackjack, self.dealer.blackjack,
                                             False, branch_value, self.dealer.value)
                update_cumulated_capital(self.player_name, self.capital)
