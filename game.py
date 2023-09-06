from configs.rules_config import MIN_BET, MAX_BET, BLACKJACK_PAYOUT
from configs.input_config import DEFAULT_PLAYER_NAME, CHIPS_DICT
from utils.swiss_knife import remind_betting_amount
from widgets.layouts import set_cards_tabs
from widgets.interactions import get_chips, get_early_pay, get_action
from widgets.notifications import notify_inadequate_capital, update_cumulated_capital
from machines.shuffle_machine import ShuffleMachine
from roles.dealer import Dealer
from roles.player import Player


class BlackjackGame:
    """Blackjack game."""

    def __init__(self):
        self.machine, self.dealer, self.player, self.capital = ShuffleMachine(), Dealer(), Player(), 0
        self.player_name = DEFAULT_PLAYER_NAME

    def check_chips(self, chips):  # Check if placed bets are valid.
        # PyWebIO's input validation function only accepts one argument.
        # This function is defined here to receive self.capital as a self-updating global variable.
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

        for i in range(head_hands):  # Iterate through all wanted head hands.
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
        # Sort Blackjack head hands from higher to lower ordinal.
        bj_head_hands_list = sorted(filter(lambda x: self.player.hands_dict[x].blackjack,
                                           self.player.hands_dict.keys()), reverse=True)

        final_bj_hands_list = []  # List of Blackjack hands waiting for dealer in the end.

        # If dealer has chance of Blackjack, early pay mode is on.
        early_pay_mode = True if self.dealer.cards_list[0] in ['A', 'K', 'Q', 'J', '10'] else False

        for bj_head_ordinal in bj_head_hands_list:  # Iterate through all Blackjack head hands.
            if early_pay_mode:  # If dealer is checking early pay.
                option = get_early_pay(bj_head_ordinal)
                if option == 'take':  # For early pay, pay on 1-1 payout rate.
                    self.capital += self.player.chips_dict[bj_head_ordinal] * 2
                    update_cumulated_capital(self.player_name, self.capital)
                    # # Display profits here.
                    self.player.hands_dict[bj_head_ordinal].early_pay = True  # Mark such hand as early-paid.
                    continue

                final_bj_hands_list += [bj_head_ordinal]  # For non-early-pay, append to final Blackjack list.
                continue

            # If dealer has 0 Blackjack chance, pay "clinching" Blackjack by preset payout rate.
            self.capital += int(self.player.chips_dict[bj_head_ordinal] * (1 + BLACKJACK_PAYOUT))
            update_cumulated_capital(self.player_name, self.capital)
            # # Display profits here.

        non_bj_head_hands_list = sorted(filter(lambda x: self.player.hands_dict[x].blackjack is False,
                                               self.player.hands_dict.keys()))  # List of non-Blackjack head hands.

        if len(non_bj_head_hands_list) > 0:  # If at least one non-Blackjack head hand to be played.
            head_ordinal = non_bj_head_hands_list[0]  # Start from the hand with the lowest ordinal.

            while True:  # Iterate through all head hands.
                if head_ordinal not in non_bj_head_hands_list:  # If all head hands are played, break while.
                    break

                head_hand_object = self.player.hands_dict[head_ordinal]  # Head hand object.
                head_hand_chips = self.player.chips_dict[head_ordinal]  # Head hand initial chips amount.

                branch_hands_list = list(head_hand_object.cards_dict.keys())  # Branch hands of iterated head hand.
                branch_ordinal, split_mark = '1', False  # Branch ordinal starts by 1. Default split mark is False.

                while True:  # Iterate through all branch hands.
                    if branch_ordinal not in branch_hands_list:  # If all branch hands are played, break while.
                        break

                    action = get_action((head_ordinal, branch_ordinal),
                                        head_hand_object.cards_dict[branch_ordinal], self.dealer.cards_list[0],
                                        head_hand_object.splits, self.capital, head_hand_chips)

                    if action == 'surrender':  # If surrender is chosen.
                        returned_chips = int(head_hand_chips * 0.5)  # Return half the initial bet.
                        self.capital += returned_chips
                        update_cumulated_capital(self.player_name, self.capital)
                        head_hand_object.surrender()
                        # # Display losses here.
                        break  # Break branch iteration for any surrender.

                    if action in ['stand', 'double_down']:  # If action is either stand or double down.
                        if action == 'stand':  # If stand is chosen.
                            head_hand_object.stand(branch_ordinal)

                        if action == 'double_down':  # If double down is chosen.
                            self.capital -= head_hand_chips  # Deduct additional bet from capital.
                            head_hand_object.hit_or_double_down(self.machine.draw(), branch_ordinal, True)
                            update_cumulated_capital(self.player_name, self.capital)

                            if head_hand_object.bust_dict[branch_ordinal]:  # Display busted loss.
                                # # Display losses here.
                                pass

                        if split_mark:  # For split branch, reload the closest isolated hand and update list.
                            head_hand_object.reload(self.machine.draw(), branch_ordinal)
                            branch_hands_list = list(head_hand_object.cards_dict.keys())

                        if branch_ordinal == branch_hands_list[-1]:
                            break  # For last branch, break branch iteration.
                        # Otherwise, go to next branch.
                        branch_ordinal = branch_hands_list[branch_hands_list.index(branch_ordinal) + 1]

                    if action == 'hit':  # If hit is chosen.
                        head_hand_object.hit_or_double_down(self.machine.draw(), branch_ordinal)

                        # Busted and ordinary 21 marks of iterated branch hand.
                        bust_mark = head_hand_object.bust_dict[branch_ordinal]
                        ordinary_21_mark = head_hand_object.ordinary_21_dict[branch_ordinal]

                        if bust_mark | ordinary_21_mark:  # If busted or reaches 21 after hit.
                            if bust_mark:  # Display busted loss.
                                # # Display losses here.
                                pass

                            if split_mark:  # For split branch, reload the closest isolated hand and update list.
                                head_hand_object.reload(self.machine.draw(), branch_ordinal)
                                branch_hands_list = list(head_hand_object.cards_dict.keys())

                            if branch_ordinal == branch_hands_list[-1]:
                                break  # For last branch, break branch iteration.
                            # Otherwise, go to next branch.
                            branch_ordinal = branch_hands_list[branch_hands_list.index(branch_ordinal) + 1]

                    if action == 'split':  # If split is chosen.
                        self.capital -= head_hand_chips  # Deduct additional bet from capital.
                        update_cumulated_capital(self.player_name, self.capital)

                        head_hand_object.split(self.machine.draw(), branch_ordinal)
                        if head_hand_object.aces_pair:  # If an Aces pair is being split.
                            head_hand_object.reload(self.machine.draw(), branch_ordinal)
                            break  # Directly reload the second branch hand and break branch iteration.

                        split_mark = True  # Turn the split mark to True.

                if head_ordinal == non_bj_head_hands_list[-1]:  # For the last head hand, break head iteration.
                    break
                head_ordinal = non_bj_head_hands_list[non_bj_head_hands_list.index(head_ordinal) + 1]  # Next head hand.

        # # List of head hands with at least one branch hand that isn't Blackjack, surrendered or busted.
        # final_head_hands_list = [head_ordinal for head_ordinal in self.player.hands_dict.keys()
        #                          if (self.player.hands_dict[head_ordinal].blackjack is False) &
        #                          (self.player.hands_dict[head_ordinal].surrendered is False) &
        #                          (list(self.player.hands_dict[head_ordinal].bust_dict.values()).count(False) > 0)]

        self.dealer.add_to_17_plus(self.machine)
