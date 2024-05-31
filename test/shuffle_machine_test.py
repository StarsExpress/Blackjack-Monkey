from machines.shuffle_machine import ShuffleMachine


if __name__ == '__main__':
    machine_main = ShuffleMachine()
    machine_main.load_and_shuffle()
    print('Card counts after initialization:')
    machine_main.show_cards_count()

    print('\nDrawn card and suit:', machine_main.draw(), '\nCard counts:')
    machine_main.show_cards_count()

    print('\nDrawn cards and suits:', machine_main.draw(True), '\nCard counts:')
    machine_main.show_cards_count()

    machine_main.load_and_shuffle()
    print('\nCard counts after reloading:')
    machine_main.show_cards_count()
