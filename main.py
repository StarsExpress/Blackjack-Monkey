from configs.app_config import HOST, PORT, DEBUG, REMOTE_ACCESS
from app import Application
from pywebio import start_server


def main():
    app = Application()
    app.execute()


if __name__ == '__main__':
    start_server(main, host=HOST, port=PORT, debug=DEBUG, remote_access=REMOTE_ACCESS)
