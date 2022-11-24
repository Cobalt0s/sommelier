from typing import Optional

from sommelier.behave_wrapper.logging import DrunkLogger
from sommelier.ctx_manager import FlowListener
from sommelier.utils import JsonRetriever


class ResponseJsonHolder(FlowListener):

    def __init__(self) -> None:
        super().__init__(definitions=[
            ['result', None]
        ], managers={
            'logger': DrunkLogger,
        })
        self.logger: Optional[DrunkLogger] = None

    def __response_result(self):
        return self.ctx_m().get('result')

    def status(self):
        return self.__response_result().status_code

    def body(self, strict=True) -> Optional[JsonRetriever]:
        try:
            data = self.__response_result().json()
            if data is None:
                raise KeyError
            if isinstance(data, dict):
                return JsonRetriever(self, data)
            self.logger.error(f'json is not an object, got: {data}')
        except Exception:
            if strict:
                self.logger.error(f'json is missing in response with status {self.status()}')
            else:
                return None
