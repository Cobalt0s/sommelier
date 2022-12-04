from typing import Optional

from sommelier.behave_wrapper import FlowListener
from sommelier.behave_wrapper.logging import DrunkLogger, StringFormatter
from sommelier.behave_wrapper.responses import ResponseJsonHolder


class Judge(FlowListener):

    def __init__(self) -> None:
        super().__init__(managers={
            'drunk_logger': DrunkLogger,
            'response_holder': ResponseJsonHolder,
        })
        self.drunk_logger: Optional[DrunkLogger] = None
        self.response_holder: Optional[ResponseJsonHolder] = None

    def expectation(self, condition, message, extra_details=None, api_enhancements=True):
        if condition:
            return
        if api_enhancements:
            operation, path = self.response_holder.description()
            self.drunk_logger.info(f'Request {operation} {path}')
            extra_details = self.__init_extra_details(extra_details)
        self.drunk_logger.error(message, extra_details)

    def __init_extra_details(self, extra_details):
        if extra_details is not None:
            return extra_details
        # if no extra details where specified get them inside response holder
        json = self.response_holder.body(strict=False)
        if json is None:
            return "No JSON"
        return json.raw()

    def assumption(self, condition, message):
        if not condition:
            self.drunk_logger.fatal(message)
        assert True
