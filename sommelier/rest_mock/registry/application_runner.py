import multiprocessing
from flask import Flask


class ApplicationRunner(object):

    def __init__(self, identifier, port) -> None:
        self.identifier = identifier
        self.service = Flask(__name__)
        self.process = multiprocessing.Process(target=self.__server_runner(port), args=())

    def __server_runner(self, port):
        self.service.run(host="localhost", port=port, debug=True)

    def start_daemon(self):
        self.process.start()

    def stop_daemon(self):
        print(f"Stopping service {self.identifier}")
        self.process.terminate()
