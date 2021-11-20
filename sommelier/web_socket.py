import requests

from sommelier.utils import table_as_dict
from sommelier.utils.assertions import require_var


class WsSocketManager:

    def __init__(self, wsm_host, wsm_port, svc_host, svc_port):
        require_var(wsm_host, "host")
        require_var(wsm_port, "port")
        require_var(svc_host, "ws_host")
        require_var(svc_port, "ws_port")
        self.host_url = f'http://{wsm_host}:{wsm_port}'
        self.svc_host = svc_host
        self.svc_port = svc_port
        self.context = None

    def set_context(self, context):
        self.context = context

    def create_socket(self, ws_name, cookie, topics):

        self.context.result = requests.post(
            f'{self.host_url}/sockets',
            json={
                "host": self.svc_host,
                "port": self.svc_port,
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
