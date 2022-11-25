from typing import Optional

from sommelier.behave_wrapper import FlowListener
from sommelier.behave_wrapper.aliases import LabelingMachine
from sommelier.behave_wrapper.logging import DrunkLogger
from sommelier.utils import JsonRetriever


class ResponseJsonHolder(FlowListener):

    def __init__(self) -> None:
        super().__init__(definitions=[
            ['result', None],
            ['requests_verb', None],
            ['url', None],
        ], managers={
            'logger': DrunkLogger,
            'labeling_machine': LabelingMachine,
        })
        self.logger: Optional[DrunkLogger] = None
        self.labeling_machine: Optional[LabelingMachine] = None

    ##########################################################
    # setters
    def with_description(self, operation, path):
        self.ctx_m().set('requests_verb', operation)
        self.ctx_m().set('url', path)

    def hold(self, response):
        self.ctx_m().set('result', response)

    ##########################################################
    # getters
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
                return JsonRetriever(self.ctx_m(), data)
            self.logger.error(f'json is not an object, got: {data}')
        except Exception:
            if strict:
                self.logger.error(f'json is missing in response with status {self.status()}')
            else:
                return None

    ##########################################################
    # operating on response data
    def save_value_as(self, key, alias):
        code = self.status()

        # TODO use judge (for now that is circular dependency)
        if code > 300:
            json = self.body(strict=False)
            if json is None:
                return "No JSON"
            self.logger.error(f'Response is not ok "{code}", cannot extract id', json.raw())
        value = self.body().get(key)
        self.labeling_machine.create_alias(alias, value)
