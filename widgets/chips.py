from configs.output_config import PLAYER_SCOPE, PLAYER_SUB_SCOPES, PROFITS_COLORS
from configs.rules_config import BLACKJACK_PAY
from widgets.layouts import clear_contents, write_text
from pywebio.output import put_table


# Display profit of input hand, and return chips.
# Arguments: chips = final bets placed at input hand; 0 dealer value = dealer is busted.
def return_chips(head_ordinal, branch_ordinal='1', chips=0, surrender=False, early_pay=False,
                 player_bj=False, dealer_bj=False, player_bust=False, player_value=0, dealer_value=0):
    branch_scope = f'{PLAYER_SCOPE}_{head_ordinal}_{branch_ordinal}'  # Branch and profit scopes for input hand.
    profit_scope = f"{branch_scope}_{PLAYER_SUB_SCOPES['profit']}"
    clear_contents(profit_scope)  # Erase old value for new value.

    if surrender:  # Return 50% to surrendered hands. Player loses 50% of chips.
        put_table([[-chips // 2]], scope=profit_scope).style(f"color:{PROFITS_COLORS['loss']}")
        write_text('You surrender and lose 50%.', branch_scope, False)
        return chips // 2

    if player_bj & early_pay:  # Profit = chips if player opts for early pay on Blackjack.
        put_table([[chips]], scope=profit_scope).style(f"color:{PROFITS_COLORS['profit']}")
        write_text('You take early pay on Blackjack.', branch_scope, False)
        return chips * 2

    if player_bust:  # Player loses all chips if busted.
        put_table([[-chips]], scope=profit_scope).style(f"color:{PROFITS_COLORS['loss']}")
        write_text('Your hand is busted.', branch_scope, False)
        return  # Don't have to return 0, as busted hands are 100% lost even if dealer goes busted.

    if dealer_bj:  # If dealer has Blackjack.
        if player_bj:  # If player also has Blackjack, profit is 0.
            put_table([[0]], scope=profit_scope).style(f"color:{PROFITS_COLORS['tie']}")
            write_text('Dealer and you both have Blackjack.', branch_scope, False)
            return chips

        put_table([[-chips]], scope=profit_scope).style(f"color:{PROFITS_COLORS['loss']}")
        write_text("Dealer has Blackjack and you don't.", branch_scope, False)
        return 0  # Otherwise, player loses all chips.

    if player_bj:  # Profit = chips * preset payout rate.
        put_table([[int(chips * BLACKJACK_PAY)]], scope=profit_scope).style(f"color:{PROFITS_COLORS['profit']}")
        write_text("You have Blackjack and dealer doesn't.", branch_scope, False)
        return int(chips * (1 + BLACKJACK_PAY))

    if player_value < dealer_value:  # If dealer wins, player loses all chips.
        put_table([[-chips]], scope=profit_scope).style(f"color:{PROFITS_COLORS['loss']}")
        write_text("Dealer's value > your value.", branch_scope, False)
        return 0

    if player_value == dealer_value:  # If a tie happens, profit is 0.
        put_table([[0]], scope=profit_scope).style(f"color:{PROFITS_COLORS['tie']}")
        write_text('You and dealer have the same value.', branch_scope, False)
        return chips

    reason = "Dealer is busted but you aren't." if dealer_value == 0 else "Your value > dealer's value."
    put_table([[chips]], scope=profit_scope).style(f"color:{PROFITS_COLORS['profit']}")
    write_text(reason, branch_scope, False)
    return chips * 2  # If player wins, profit = chips.
