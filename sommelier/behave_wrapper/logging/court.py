from typing import Optional

from sommelier.behave_wrapper import ResponseJsonHolder
from sommelier.behave_wrapper.logging import DrunkLogger, StringFormatter
from sommelier.ctx_manager import FlowListener


class Judge(FlowListener):

    def __init__(self) -> None:
        super().__init__(managers={
            'drunk_logger': DrunkLogger,
            'response': ResponseJsonHolder,
        })
        self.drunk_logger: Optional[DrunkLogger] = None
        self.response: Optional[ResponseJsonHolder] = None

    def expectation(self, condition, message, extra_details=None, api_enhancements=True):
        if condition:
            return
        if api_enhancements:
            self.drunk_logger.info(StringFormatter(
                f'Request {self.ctx_m().get("requests_verb")} {self.ctx_m().get("url")}', [
                    # TODO, this should not be in the judge!
                ],
            ))
            extra_details = self.__init_extra_details(extra_details)
        self.drunk_logger.error(message, extra_details)

    def __init_extra_details(self, extra_details):
        if extra_details is not None:
            return extra_details
        # if no extra details where specified get them inside response holder
        json = self.response.body(strict=False)
        if json is None:
            return "No JSON"
        return json.raw()

    def assumption(self, condition, message):
        if not condition:
            self.drunk_logger.fatal(message)
        assert True
