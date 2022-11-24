from typing import Optional

from sommelier.behave_wrapper import LabelingMachine
from sommelier.behave_wrapper.logging import DrunkLogger, Judge
from sommelier.ctx_manager import FlowListener
from sommelier.utils import JsonRetriever


class ResponseJsonHolder(FlowListener):

    def __init__(self) -> None:
        super().__init__(definitions=[
            ['result', None]
        ], managers={
            'logger': DrunkLogger,
            'judge': Judge,
            'labeling_machine': LabelingMachine,
        })
        self.logger: Optional[DrunkLogger] = None
        self.judge: Optional[Judge] = None
        self.labeling_machine: Optional[LabelingMachine] = None

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

    def save_value_as(self, key, alias):
        # TODO a general response manager should exist
        # TODO identifier registry should be repurposed to UserRegistry
        # Try to get id from the last response data
        code = self.status()

        self.judge.expectation(
            code < 300,
            f'Response is not ok "{code}", cannot extract id',
            )
        value = self.body().get(key)
        self.labeling_machine.create_alias(alias, value)
