from configs.app_config import PORT
from app import Application
from pywebio import start_server


if __name__ == '__main__':
    app = Application()
    start_server(app.execute, port=PORT, debug=True, auto_open_webbrowser=True)
