from utils.judges import judge_blackjack


def test_blackjack_judge():
    assert judge_blackjack(['10', 'A'], False) is True
    assert judge_blackjack(['5', 'A'], False) is False
    assert judge_blackjack(['5', 'A'], True) is False
    assert judge_blackjack(['10', 'A'], True) is False


if __name__ == '__main__':
    test_blackjack_judge()
