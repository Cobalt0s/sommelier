from typing import Union, Optional

from sommelier.behave_wrapper import FlowListener
from sommelier.behave_wrapper.logging import StringFormatter, BeautyPrinter
from sommelier.utils import SimpleLogger


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
