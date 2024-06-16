"""All app configurations."""

import os

APP_BASE_PATH = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)  # Where Python files are stored.

IMAGES_FOLDER_PATH = os.path.join(APP_BASE_PATH, "images")

RULES_PATHS_DICT = {
    "english": os.path.join(APP_BASE_PATH, "rules", "english.txt"),
    "traditional": os.path.join(APP_BASE_PATH, "rules", "traditional.txt"),
    "simplified": os.path.join(APP_BASE_PATH, "rules", "simplified.txt"),
}

PAGE_NAME = "🎰Job's Here"
PAGE_THEME = "sketchy"
PAGE_TITLE = "♠️♥️Jack's Online Blackjack♦️♣️"

DEALER_SLEEP = 1  # Sleep: pause before next line of code.
EARLY_EXIT_SLEEP = 2
GAME_END_SLEEP = 2

HOST = "0.0.0.0"
PORT = 8080
DEBUG = False
REMOTE_ACCESS = True
