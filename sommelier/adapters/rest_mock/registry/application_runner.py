import threading

from flask import Flask
from werkzeug.serving import make_server


DEFAULT_PORT = 7000


class ServerThread(threading.Thread):
    # https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c

    def __init__(self, app: Flask):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', DEFAULT_PORT, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def schedule_shutdown(self):
        self.server.shutdown()

    def schedule_start(self):
        self.start()
