import requests

from core.utils import table_as_dict


class WsSocketManager:

    def __init__(self, host, port, ws_host, ws_port):
        self.host_url = f'http://{host}:{port}'
        self.ws_host = ws_host
        self.ws_port = ws_port
        self.context = None

    def set_context(self, context):
        self.context = context

    def create_socket(self, ws_name, cookie, topics):
        self.context.result = requests.post(
            f'{self.host_url}/sockets',
            json={
                "host": self.ws_host,
                "port": self.ws_port,
                "name": ws_name,
                "cookie": cookie,
                "topics": topics
            }
        )

    def get_message_from_topic(self, ws_name, topic):
        self.context.result = requests.get(
            f'{self.host_url}/sockets/{ws_name}/topics/{topic}/messages',
        )

    def write_message_to_topic(self, ws_name, topic):
        self.context.result = requests.post(
            f'{self.host_url}/sockets/{ws_name}/topics/{topic}/messages',
            json=table_as_dict(self.context)
        )
