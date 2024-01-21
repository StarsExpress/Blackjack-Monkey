from app import Application
from pywebio import start_server


if __name__ == '__main__':
    app = Application()
    start_server(app.execute)

