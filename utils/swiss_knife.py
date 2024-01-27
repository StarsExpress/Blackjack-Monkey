from configs.app_config import IMAGES_FOLDER_PATH, RULES_PATHS_DICT
from configs.rules_config import MAX_BET
from configs.output_config import VALUES_COLORS, DANGER_ZONE
from utils.trackers import track_display_value
import os
from PIL import Image


def read_cards_images():
    images_dict = dict()
    images_names_list = os.listdir(IMAGES_FOLDER_PATH)

    for image_name in images_names_list:
        if image_name.endswith('.jpg'):  # Only read jpg files.
            image_path = os.path.join(IMAGES_FOLDER_PATH, image_name)
            images_dict.update({image_name.split('.')[0]: Image.open(image_path)})  # Use the string before dot as key.
    return images_dict


def read_rules():  # Read rules of available languages from rules folder.
    rules_dict = {}
    for key in RULES_PATHS_DICT.keys():  # Key is language name.
        file = open(RULES_PATHS_DICT[key], 'r', encoding='UTF-8')
        rules_dict.update({key: file.read()})
        file.close()
    return rules_dict


def remind_betting_amount(remaining_capital):  # Remind maximal feasible amount to bet for iterated hand.
    return f"{str(min(remaining_capital, MAX_BET))}. Only accept 100's multiples."


def find_ordinal_text(ordinal):  # Find corresponding text of ordinal.
    if ordinal == '1':
        return '1st'
    if ordinal == '2':
        return '2nd'
    if ordinal == '3':
        return '3rd'
    return '4th'  # Possible maximum branch is 4.


def assist_insurance_checkbox(non_bj_hands_list, hands_dict):  # Return options list for insurance checkbox.
    options_list = []
    for head_ordinal in non_bj_hands_list:  # For each non-Blackjack hand, provide ordinal and displayed value.
        displayed_value = track_display_value(hands_dict[head_ordinal].value_dict['1'],
                                              soft=hands_dict[head_ordinal].soft_dict['1'])
        options_list.append(f"Hand {head_ordinal}: {displayed_value}")
    return options_list


def find_ordinal(insurance_hands_list):  # Get ordinal from checkbox option: "Hand head_ordinal: displayed_value".
    # [1]: 1st item right next to 1st space. [:-1]: exclude colon.
    return [head_ordinal.split(' ')[1][:-1] for head_ordinal in insurance_hands_list]


def find_placed_insurance(insurance_hands_list, hands_dict):  # For each hand, placed insurance is half initial chips.
    if len(insurance_hands_list) == 0:  # If list is empty, return 0 as insurance amount.
        return 0
    return sum(hands_dict[head_ordinal].initial_chips for head_ordinal in insurance_hands_list) // 2


def find_value_color(value, soft, bust):  # Find corresponding color of hand value.
    if bust:
        return VALUES_COLORS['busted']
    if (soft is False) & (DANGER_ZONE['lower'] <= value <= DANGER_ZONE['upper']):
        return VALUES_COLORS['danger']  # Value color for hard values in danger zone.
    return VALUES_COLORS['safe']


def find_total_bets(hands_dict, insurance_hands_list):  # Find total bets placed in each round.
    # 1st term: sum bets from each head hand's branches, then sum again along all head hands.
    # 2nd term: sum all placed insurance (50% initial chips) for each hand of insurance hands list.
    return (sum(sum(hands_dict[key].chips_dict.values()) for key in hands_dict.keys()) +
            sum(hands_dict[hand].initial_chips for hand in insurance_hands_list) // 2)
