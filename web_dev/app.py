from flask import Flask, render_template, request
from shuffle_machine import ShuffleMachine
import os

app = Flask(__name__)
environment_configuration = os.environ['CONFIGURATION_SETUP']
app.config.from_object(environment_configuration)

shuffle_machine = ShuffleMachine()


@app.route('/game page', methods=['GET', 'POST'])
def game_page():
    card_name = ''
    if request.method == 'POST':
        if request.form['draw_button'] == 'Draw':
            shuffle_machine.shuffle_deck()
            card_value = shuffle_machine.draw_one_card()

            if card_value >= 11:
                card_name = 'J' if card_value == 11 else ('Q' if card_value == 12 else 'K' if card_value == 13 else 'A')
            else:
                card_name = str(card_value)

            shuffle_machine.reload_deck()

            return render_template('game_page.html', card_name=card_name)

    return render_template('game_page.html', card_name=card_name)


if __name__ == '__main__':
    app.run()
