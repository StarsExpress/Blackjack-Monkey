from configs.app_config import HOST, PORT, DEBUG, REMOTE_ACCESS
from app import Application
from pywebio.platform.tornado_http import start_server

if __name__ == '__main__':
    app = Application()
    start_server(app.execute, host=HOST, port=PORT, debug=DEBUG, remote_access=REMOTE_ACCESS)
