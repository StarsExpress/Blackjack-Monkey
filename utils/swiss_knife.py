from configs.rules_config import MAX_BET
from configs.output_config import VALUE_COLORS, DANGER_ZONE


def remind_betting_amount(remaining_capital):  # Remind maximal feasible amount to bet for iterated hand.
    return f"{str(min(remaining_capital, MAX_BET))}. Only accept 100's multiples."


def find_ordinal_text(ordinal):  # Find corresponding text of ordinal.
    if ordinal == '1':
        return '1st'
    if ordinal == '2':
        return '2nd'
    if ordinal == '3':
        return '3rd'
    if ordinal == '4':
        return '4th'


def find_value_color(value, soft, bust):  # Find corresponding color of hand value.
    if bust:
        return VALUE_COLORS['busted']
    if (soft is False) & (DANGER_ZONE['lower'] <= value <= DANGER_ZONE['upper']):
        return VALUE_COLORS['danger']  # Value color for hard values in danger zone.
    return VALUE_COLORS['safe']
