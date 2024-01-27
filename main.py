from app import Application
from pywebio.platform.tornado_http import start_server


if __name__ == '__main__':
    app = Application()
    start_server(app.execute, debug=False)
