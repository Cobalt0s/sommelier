import json
from typing import Optional

from sommelier.adapters.sockets import (
    WebSocketReader, WebSocketWriter
)
from sommelier.behave_wrapper import FlowListener, response_json_holder
from sommelier.behave_wrapper.tables import carpenter
from sommelier.utils import require_var


class WSocketManager(FlowListener):
    """
    This is a one way web socket manager
    Manager allows to do read, write or both but via 2 different ws
    Tests written in behave are sequential and WS manager fits into this idea
    """

    def __init__(self, host):
        super().__init__()
        require_var(host, "host")
        self.host = host
        self.reader: Optional[WebSocketReader] = None
        self.writer: Optional[WebSocketWriter] = None

    def after_all(self):
        super().after_all()
        self.disconnect_all()

    def create_socket(self, reader):
        cookies = carpenter.builder().double().dict()
        if reader:
            self.reader = WebSocketReader(self.host, cookies)
            self.reader.schedule_start()
        else:
            self.writer = WebSocketWriter(self.host, cookies)
            self.writer.schedule_start()

    def read_data(self):
        response_json_holder.with_description("WS-Read", self.host)
        text = self.reader.read_one()
        data = json.loads(text)
        response_json_holder.hold(data)

    def write_data(self):
        data = carpenter.builder().double().dict()
        self.writer.write(data)

    def disconnect_all(self):
        if self.reader is not None:
            self.reader.schedule_shutdown()
        if self.writer is not None:
            self.writer.schedule_shutdown()
