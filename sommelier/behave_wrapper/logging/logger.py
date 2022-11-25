from typing import Union, Optional

from sommelier.behave_wrapper import FlowListener
from sommelier.behave_wrapper.logging import StringFormatter, BeautyPrinter


class DrunkLogger(FlowListener):

    def __init__(self) -> None:
        super().__init__(managers={
            'beauty_printer': BeautyPrinter,
        })
        self.beauty_printer: Optional[BeautyPrinter] = None

    def info(self, text: Union[str, StringFormatter]):
        text = self.beauty_printer.resolve(text)
        print(f'[ 🍷 Info     ] {text}')

    def error(self, text: Union[str, StringFormatter], extra_details=None):
        text = self.beauty_printer.resolve(text)
        self.__log_header()
        print(f'[ 🍷 Error    ] {text}')
        if extra_details is not None:
            print(self.beauty_printer.resolve(
                StringFormatter('%%pretty!', [extra_details])
            ))
        assert False, "step failed"

    def fatal(self, text: Union[str, StringFormatter]):
        text = self.beauty_printer.resolve(text)
        self.__log_header()
        print(f'[ 💥 Fatal    ] {text}')
        assert False, "error in the test itself"

    def __log_header(self):
        gherkin_feature = self.ctx_m().context.feature
        if gherkin_feature is not None:
            gherkin_scenario = self.ctx_m().context.scenario
            print(f'[ 🌍 Scenario ] {gherkin_feature.name} >> {gherkin_scenario.name}')
