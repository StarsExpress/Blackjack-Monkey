from configs.output_config import PLAYER_SCOPE, PLAYER_SUB_SCOPES, PROFITS_COLORS, TABLE_HEADERS
from configs.rules_config import BLACKJACK_PAY, INSURANCE_PAY
from widgets.layouts import clear_contents, write_text
from pywebio.output import put_table


# Display profit of input hand, and return chips.
def return_chips(head_ordinal: str, branch_ordinal: str = '1', chips: int = 0, surrender: bool = False,
                 early_pay: bool = False, insurance: int = 0, player_bj: bool = False, dealer_bj: bool = False,
                 player_bust: bool = False, player_value: int = 0, dealer_value: int = 0):
    # Chips = final bets placed at input hand. 0 dealer value = dealer is busted.
    # Insurance = 0 if player doesn't buy or win/loss result is unknown; 1 means win; -1 means loss.

    branch_scope = f'{PLAYER_SCOPE}_{head_ordinal}_{branch_ordinal}'  # Branch and profit scopes for input hand.
    profit_scope = f"{branch_scope}_{PLAYER_SUB_SCOPES['profit']}"
    clear_contents(profit_scope)  # Erase old value for new value.

    if surrender:  # Return 50% to surrendered hands. Player loses 50% of chips.
        put_table([[-chips // 2]], header=TABLE_HEADERS['profit'],
                  scope=profit_scope).style(f"color:{PROFITS_COLORS['loss']}")
        write_text('You surrender and lose 50%.', branch_scope, False)
        return chips // 2

    if player_bj & early_pay:  # Profit = chips if player opts for early pay on Blackjack.
        put_table([[chips]], header=TABLE_HEADERS['profit'],
                  scope=profit_scope).style(f"color:{PROFITS_COLORS['profit']}")
        write_text('You take early pay on Blackjack.', branch_scope, False)
        return chips * 2

    insurance_adjustment = (chips // 2) * INSURANCE_PAY if insurance == 1 else (0 if insurance == 0 else -chips // 2)
    insurance_message = '\nInsurance wins.' if insurance == 1 else ('' if insurance == 0 else '\nInsurance loses.')
    insurance_chips = (chips // 2) * (1 + INSURANCE_PAY) if insurance == 1 else 0

    if player_bust:  # Player's hand loses all chips if busted. Apply insurance adjustment.
        profit = insurance_adjustment - chips
        style = PROFITS_COLORS['loss'] if profit < 0 else PROFITS_COLORS['tie']
        put_table([[profit]], header=TABLE_HEADERS['profit'], scope=profit_scope).style(f"color:{style}")
        # Only notify hand busted message if player doesn't buy insurance or insurance result is unknown.
        bust_message = 'Your hand is busted.' if insurance == 0 else ''
        write_text(f'{bust_message}{insurance_message}', branch_scope, False)
        return insurance_chips

    if dealer_bj:  # If dealer has Blackjack.
        if player_bj:  # If player also has Blackjack, profit is 0.
            put_table([[0]], header=TABLE_HEADERS['profit'], scope=profit_scope).style(f"color:{PROFITS_COLORS['tie']}")
            write_text('Dealer and you both have Blackjack.', branch_scope, False)
            return chips

        # Otherwise, player's hand loses all chips. Apply insurance adjustment.
        profit = insurance_adjustment - chips
        style = PROFITS_COLORS['loss'] if profit < 0 else PROFITS_COLORS['tie']
        put_table([[profit]], header=TABLE_HEADERS['profit'], scope=profit_scope).style(f"color:{style}")
        write_text(f"Dealer has Blackjack and you don't.{insurance_message}", branch_scope, False)
        return insurance_chips

    if player_bj:  # Profit = chips * preset payout rate.
        put_table([[int(chips * BLACKJACK_PAY)]], header=TABLE_HEADERS['profit'],
                  scope=profit_scope).style(f"color:{PROFITS_COLORS['profit']}")
        write_text("You have Blackjack and dealer doesn't.", branch_scope, False)
        return int(chips * (1 + BLACKJACK_PAY))

    if player_value < dealer_value:  # If dealer wins, player's hand loses all chips. Apply insurance adjustment.
        put_table([[insurance_adjustment - chips]], header=TABLE_HEADERS['profit'],
                  scope=profit_scope).style(f"color:{PROFITS_COLORS['loss']}")
        write_text(f"Dealer's value > your value.{insurance_message}", branch_scope, False)
        return 0

    if player_value == dealer_value:  # If a tie happens, profit is 0. Apply insurance adjustment.
        style = PROFITS_COLORS['loss'] if insurance_adjustment < 0 else PROFITS_COLORS['tie']
        put_table([[insurance_adjustment]], header=TABLE_HEADERS['profit'], scope=profit_scope).style(f"color:{style}")
        write_text(f'You and dealer have the same value.{insurance_message}', branch_scope, False)
        return chips

    # If player wins, profit = chips. Apply insurance adjustment.
    put_table([[chips + insurance_adjustment]], header=TABLE_HEADERS['profit'],
              scope=profit_scope).style(f"color:{PROFITS_COLORS['profit']}")
    reason = "Dealer is busted but you aren't." if dealer_value == 0 else "Your value > dealer's value."
    write_text(f'{reason}{insurance_message}', branch_scope, False)
    return chips * 2
