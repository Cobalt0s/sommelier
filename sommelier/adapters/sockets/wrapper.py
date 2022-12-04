import asyncio
import json
import threading

import websockets

from sommelier.utils import ThreadSafeList, SimpleLogger


def bake_cookie(cookies):
    pairs = []
    for k, v in cookies.items():
        pairs.append(k + "=" + v)
    return "; ".join(pairs)


class WebSocketWrapper(threading.Thread):

    def __init__(self, address: str, reader_mode: bool, cookies: dict = None) -> None:
        threading.Thread.__init__(self)
        self.reader_mode = reader_mode
        self.loop = asyncio.get_event_loop()
        self.address = address
        self.aborted = False
        self.input_stream = ThreadSafeList()
        self.output_stream = ThreadSafeList()
        if cookies is None:
            cookies = {}
        self.cookie = bake_cookie(cookies)

    def schedule_start(self):
        self.start()

    def schedule_shutdown(self):
        self.aborted = True

    async def ws_loop(self):
        async with websockets.connect(self.address, extra_headers={"Cookie": self.cookie}) as websocket:
            SimpleLogger.info("websocket connected")
            while not self.aborted:
                # We are using this web socket for writes only
                if not self.reader_mode:
                    data = self.input_stream.pop()
                    if data is None:
                        # No data to send, keep polling
                        continue
                    SimpleLogger.info(f"Sending to WS: {data}")
                    await websocket.send(data)
                # WS for reading only
                if self.reader_mode:
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=1)
                    except asyncio.exceptions.TimeoutError:
                        continue
                    SimpleLogger.info(f"Receiving from WS: {response}")
                    self.output_stream.append(response)
        SimpleLogger.info("websocket disconnected")

    def run(self):
        self.loop.run_until_complete(self.ws_loop())


class WebSocketWriter(WebSocketWrapper):

    def __init__(self, address: str, cookies: dict = None) -> None:
        super().__init__(address, False, cookies)

    def write(self, data):
        data = json.dumps(data)
        return self.input_stream.append(data)


class WebSocketReader(WebSocketWrapper):

    def __init__(self, address: str, cookies: dict = None) -> None:
        super().__init__(address, True, cookies)

    def read_all(self):
        result = []
        while True:
            pop = self.output_stream.pop()
            if pop is None:
                return result
            result.append(pop)

    def read_one(self):
        return self.output_stream.pop()
