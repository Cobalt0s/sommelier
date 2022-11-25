from typing import Union, Optional

from sommelier.behave_wrapper import FlowListener
from sommelier.behave_wrapper.logging import StringFormatter, BeautyPrinter


class SimpleLogger(object):

    @staticmethod
    def info(text: str):
        print(f'[ 🍷 Info     ] {text}')

    @staticmethod
    def error(text: str, extra_details=None, context=None):
        SimpleLogger.__log_header(context)
        print(f'[ 🍷 Error    ] {text}')
        if extra_details is not None:
            print(extra_details)
        assert False, "step failed"

    @staticmethod
    def fatal(text: str, context=None):
        SimpleLogger.__log_header(context)
        print(f'[ 💥 Fatal    ] {text}')
        assert False, "error in the test itself"

    @staticmethod
    def __log_header(context):
        if context is None:
            return
        gherkin_feature = context.feature
        if gherkin_feature is not None:
            gherkin_scenario = context.scenario
            print(f'[ 🌍 Scenario ] {gherkin_feature.name} >> {gherkin_scenario.name}')


class DrunkLogger(FlowListener):

    def __init__(self) -> None:
        super().__init__(managers={
            'beauty_printer': BeautyPrinter,
        })
        self.beauty_printer: Optional[BeautyPrinter] = None

    def info(self, text: Union[str, StringFormatter]):
        text = self.beauty_printer.resolve(text)
        SimpleLogger.info(text)

    def error(self, text: Union[str, StringFormatter], extra_details=None):
        text = self.beauty_printer.resolve(text)
        if extra_details is not None:
            extra_details = self.beauty_printer.resolve(
                StringFormatter('%%pretty!', [extra_details])
            )
        SimpleLogger.error(text, extra_details, self.ctx_m().context)

    def fatal(self, text: Union[str, StringFormatter]):
        text = self.beauty_printer.resolve(text)
        SimpleLogger.fatal(text, self.ctx_m().context)
