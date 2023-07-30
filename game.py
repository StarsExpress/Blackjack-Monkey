from config import MINIMUM_BET, MAXIMUM_BET, BLACKJACK_PAYOUT
from machines.shuffle_machine import ShuffleMachine
from roles.dealer import Dealer
from roles.player import Player
from utils.displayer import show_out_of_money, show_game_invalid_input, show_early_pay, show_result, show_actions
from utils.action_eligibility import offer_early_pay_option, find_eligible_actions
from utils.judges import judge_returned_chips


class BlackjackGame:
    """Blackjack game."""

    def __init__(self):
        self.machine, self.dealer, self.player, self.capital = ShuffleMachine(), Dealer(), Player(), 0

    def set_up(self, head_hands, capital):  # Set up capital amount and shuffle machine before each round.self.capital
        self.capital = capital  # Remaining capital amount.
        self.machine.load_and_shuffle()  # Load and shuffle cards.

        chips_list = []  # List of chips for each hand.
        for i in range(head_hands):  # Iterate through all wanted head hands.
            if self.capital < MINIMUM_BET:  # If remaining capital isn't enough for another head hand, break for loop.
                show_out_of_money(self.capital)
                break

            while True:  # Make sure input if valid.
                chips = str(input('Put your chips for hand ' + str(i + 1) + ': '))
                if chips.strip().isdigit() is False:  # If stripped input isn't integer, continue while.
                    show_game_invalid_input(not_digit=True)
                    continue
                if int(chips) < MINIMUM_BET:  # If input < minimum bet, continue while.
                    show_game_invalid_input(below_minimum=True)
                    continue
                if int(chips) > self.capital:  # If input > remaining capital, continue while.
                    show_game_invalid_input(remaining_capital=self.capital, over_capital=True)
                    continue
                if int(chips) > MAXIMUM_BET:  # If input > maximum bet, continue while.
                    show_game_invalid_input(over_maximum=True)
                    continue
                if int(chips) % 100 != 0:  # If input isn't 100's multiple, continue while.
                    show_game_invalid_input(not_100_multiple=True)
                    continue
                break

            chips = int(chips.strip())  # Turn stripped string to integer.
            self.capital -= chips  # Deduct chips amount from capital.
            chips_list.append(chips)  # Append chips to list.

        self.dealer.prepare(self.machine.draw())  # Dealer and player preparations.
        self.player.prepare(chips_list, [list(self.machine.draw(True)) for _ in range(len(chips_list))])

    def start(self):  # Start a new round.
        final_bj_hands_list = []  # List of Blackjack hand that has to wait for dealer in the end.
        # List of reverse-sorted Blackjack head hands.
        bj_head_hands_list = sorted(filter(lambda x: self.player.hands_dict[x].blackjack,
                                           self.player.hands_dict.keys()), reverse=True)

        early_pay_mode, options_str, options_dict = False, None, None  # Default early pay mode is False.
        if self.dealer.cards_list[0] in ['A', 'K', 'Q', 'J', '10']:  # If dealer has Blackjack chance.
            early_pay_mode = True  # Early pay mode is on.
            options_str, options_dict = offer_early_pay_option()

        for bj_head_ordinal in bj_head_hands_list:  # Iterate through all Blackjack head hands.
            if early_pay_mode:  # If dealer is checking early pay.
                show_early_pay(bj_head_ordinal)
                while True:  # Make sure eligible option is selected.
                    selection = str(input(options_str)).strip()
                    if selection not in options_dict.keys():  # If invalid option is selected, continue while.
                        show_game_invalid_input(invalid_option=True)
                        continue
                    print('\n')  # Print a space line.
                    break

                if options_dict[selection] == 'Take':  # If player opts to take early pay.
                    returned_chips = self.player.chips_dict[bj_head_ordinal] * 2
                    self.capital += returned_chips  # Return chips to capital.
                    show_result(bj_head_ordinal, '1', returned_chips, self.player.chips_dict[bj_head_ordinal])
                    self.player.hands_dict[bj_head_ordinal].early_pay = True  # Change early pay mark to True.
                    continue  # Continue to next Blackjack head hand.

                final_bj_hands_list += [bj_head_ordinal]  # Add non-early-paid Blackjack hand to final Blackjack list.
                continue  # Continue to next Blackjack head hand.

            returned_chips = int(self.player.chips_dict[bj_head_ordinal] * (1 + BLACKJACK_PAYOUT))
            self.capital += returned_chips  # Return chips for clinching Blackjack hand to capital.
            show_result(bj_head_ordinal, '1', returned_chips, self.player.chips_dict[bj_head_ordinal])

        print('\n')  # Print a space line.
        non_bj_head_hands_list = sorted(filter(lambda x: self.player.hands_dict[x].blackjack is False,
                                               self.player.hands_dict.keys()))  # List of non-Blackjack head hands.
        if len(non_bj_head_hands_list) > 0:  # If at least one non-Blackjack head hand.
            head_ordinal = non_bj_head_hands_list[0]  # Head hand ordinal starts from 1.

            while True:  # Iterate through all head hands.
                if head_ordinal not in non_bj_head_hands_list:  # If all head hands have been played.
                    break  # Break head iteration.

                head_hand_object = self.player.hands_dict[head_ordinal]  # Head hand object.
                head_hand_chips = self.player.chips_dict[head_ordinal]  # Head hand initial chips amount.

                branch_hands_list = list(head_hand_object.cards_dict.keys())  # Branch hands of iterated head hand.
                branch_ordinal, split_mark = '1', False  # Branch hand ordinal starts by 1. Default split mark is False.

                while True:  # Iterate through all branch hands.
                    if branch_ordinal not in branch_hands_list:  # If branch hands are all played.
                        break  # Break branch iteration

                    show_actions(head_ordinal, branch_ordinal, head_hand_object.cards_dict[branch_ordinal],
                                 self.capital, head_hand_chips, split_mark)
                    actions_str, actions_dict = find_eligible_actions(
                        head_hand_object.cards_dict[branch_ordinal], self.dealer.cards_list[0],
                        head_hand_object.splits, self.capital, head_hand_chips)

                    while True:  # Make sure eligible action is selected.
                        selection = str(input(actions_str)).strip()
                        if selection not in actions_dict.keys():  # If invalid action is selected, continue while.
                            show_game_invalid_input(invalid_action=True)
                            continue
                        print('\n')  # Print a space line.
                        break

                    if actions_dict[selection] == 'Surrender':  # If surrender is chosen.
                        returned_chips = int(head_hand_chips * 0.5)  # Return half the initial bet.
                        self.capital += returned_chips
                        show_result(head_ordinal, '1', returned_chips, head_hand_chips)

                        head_hand_object.surrender()  # Break branch iteration for any surrender.
                        break

                    if actions_dict[selection] in ['Stand', 'Double Down']:  # If action is either stand or double down.
                        if actions_dict[selection] == 'Stand':  # If stand is chosen.
                            head_hand_object.stand(branch_ordinal, split_mark)

                        if actions_dict[selection] == 'Double Down':  # If double down is chosen.
                            self.capital -= head_hand_chips  # Deduct additional bet from capital.
                            head_hand_object.hit_or_double_down(
                                self.machine.draw(), branch_ordinal, True, split_mark)

                            if head_hand_object.bust_dict[branch_ordinal]:  # Display busted loss.
                                show_result(head_ordinal, branch_ordinal, 0, head_hand_chips, split_mark, True)

                        if split_mark:  # If this branch a split, reload the closest isolated hand and update list.
                            head_hand_object.reload(self.machine.draw(), branch_ordinal)
                            branch_hands_list = list(head_hand_object.cards_dict.keys())

                        if branch_ordinal == branch_hands_list[-1]:
                            break  # If is the last branch hand, break branch iteration.

                        branch_ordinal = branch_hands_list[branch_hands_list.index(branch_ordinal) + 1]  # Next branch.

                    if actions_dict[selection] == 'Hit':  # If hit is chosen.
                        head_hand_object.hit_or_double_down(self.machine.draw(), branch_ordinal, False, split_mark)

                        # Busted and ordinary 21 marks of iterated branch hand.
                        bust_mark = head_hand_object.bust_dict[branch_ordinal]
                        ordinary_21_mark = head_hand_object.ordinary_21_dict[branch_ordinal]

                        if bust_mark | ordinary_21_mark:  # If busted or reaches 21 after hit.
                            if bust_mark:  # Display busted loss.
                                show_result(head_ordinal, branch_ordinal, 0, head_hand_chips, split_mark)

                            if split_mark:  # If a branch is a split, reload the closest isolated hand and update list.
                                head_hand_object.reload(self.machine.draw(), branch_ordinal)
                                branch_hands_list = list(head_hand_object.cards_dict.keys())

                            if branch_ordinal == branch_hands_list[-1]:  # For last branch hand, break branch iteration.
                                break
                            # Go to next branch hand.
                            branch_ordinal = branch_hands_list[branch_hands_list.index(branch_ordinal) + 1]

                    if actions_dict[selection] == 'Split':  # If split is chosen.
                        self.capital -= head_hand_chips  # Deduct additional bet from capital.

                        head_hand_object.split(self.machine.draw(), branch_ordinal)
                        if head_hand_object.aces_pair:  # If an Aces pair is being split.
                            head_hand_object.reload(self.machine.draw(), branch_ordinal)
                            break  # Directly reload the second branch hand and break branch iteration.

                        split_mark = True  # Turn the split mark to True.

                if head_ordinal == non_bj_head_hands_list[-1]:  # For the last head hand, break head iteration.
                    break
                head_ordinal = non_bj_head_hands_list[non_bj_head_hands_list.index(head_ordinal) + 1]  # Next head hand.

        # List of head hands with at least one branch hand that isn't Blackjack, surrendered or busted.
        final_head_hands_list = [head_ordinal for head_ordinal in self.player.hands_dict.keys()
                                 if (self.player.hands_dict[head_ordinal].blackjack is False) &
                                 (self.player.hands_dict[head_ordinal].surrendered is False) &
                                 (list(self.player.hands_dict[head_ordinal].bust_dict.values()).count(False) > 0)]

        # Check if player's hands are all Blackjack.
        player_all_blackjack = True if (len(final_head_hands_list) == 0) & (len(final_bj_hands_list) > 0) else False

        # Add non-early-paid Blackjack hands into final head hands list. Sort by reversed keys.
        final_head_hands_list = sorted(final_head_hands_list + final_bj_hands_list, reverse=True)
        if len(final_head_hands_list) == 0:  # If no remaining hands to be judged.
            print('You have no hands left to be judged in this round.\n')
            return

        self.dealer.add_to_17_plus(self.machine, player_all_blackjack)  # Dealer adds to 17 or more.
        dealer_value = 0 if self.dealer.bust else self.dealer.value  # If dealer is busted, set dealer value as 0.

        for head_ordinal in final_head_hands_list:  # Iterate through all final head hands.
            head_hand_object = self.player.hands_dict[head_ordinal]  # Head hand object.
            initial_chips = self.player.chips_dict[head_ordinal]  # Initial chips of head hand.
            split_mark = True if head_hand_object.splits > 0 else False  # If head hand split.

            # Reverse sorted list of branch hands that are not early-paid Blackjack, nor surrendered or busted.
            branch_hands_list = sorted(filter(lambda x: (head_hand_object.early_pay is False) &
                                                        (head_hand_object.surrendered is False) &
                                                        (head_hand_object.bust_dict[x] is False),
                                              head_hand_object.cards_dict.keys()), reverse=True)

            for branch_ordinal in branch_hands_list:  # Iterate through all branch hands.
                branch_value = head_hand_object.value_dict[branch_ordinal]  # Branch hand value.
                branch_bj = head_hand_object.blackjack  # If branch hand has Blackjack.
                branch_double_down = head_hand_object.double_down_dict[branch_ordinal]  # If branch hand doubled down.

                returned_chips, reason = judge_returned_chips(initial_chips, branch_value, dealer_value, branch_bj,
                                                              self.dealer.blackjack, branch_double_down)
                self.capital += returned_chips  # Return chips to capital.
                show_result(head_ordinal, branch_ordinal, returned_chips, initial_chips,
                            split_mark, branch_double_down, reason)


if __name__ == '__main__':
    game_main = BlackjackGame()
    game_main.set_up(2, 2000)
    game_main.start()
