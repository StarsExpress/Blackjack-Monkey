from pywebio.platform.tornado_http import start_server
from configs.app_config import HOST, PORT, DEBUG, REMOTE_ACCESS
from app import Application


def main():
    """
    Initializes and starts web game server.

    Main method creates an Application instance for each visited player,
    and starts a web server to host visits.
    """
    app = Application()
    app.execute()


if __name__ == '__main__':
    start_server(main, host=HOST, port=PORT, debug=DEBUG, remote_access=REMOTE_ACCESS)
