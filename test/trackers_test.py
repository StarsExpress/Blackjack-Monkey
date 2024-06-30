from utils.trackers import update_properties, track_display_value


def test_trackers():
    assert update_properties(['A'] * 11) == (21, True, False)
    assert update_properties(['A'] * 12) == (12, False, False)
    assert track_display_value(18, soft=True, stand=True) == '18'
    assert track_display_value(18, soft=True, stand=False) == '18/8'


if __name__ == '__main__':
    test_trackers()
