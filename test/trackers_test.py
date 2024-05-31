from utils.trackers import update_properties, track_display_value


if __name__ == '__main__':
    print(update_properties(['A'] * 11))
    print(track_display_value(18, soft=True, stand=True))
