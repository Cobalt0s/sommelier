from typing import Optional

from sommelier.behave_wrapper import FlowListener
from sommelier.behave_wrapper.logging import Judge
from sommelier.behave_wrapper.responses import ResponseJsonHolder


class PaginationNavigator(FlowListener):

    def __init__(self):
        super().__init__(definitions=[
            ['pagination', {}],
        ], managers={
            'response': ResponseJsonHolder,
            'judge': Judge,
        })
        self.response: Optional[ResponseJsonHolder] = None
        self.judge: Optional[Judge] = None

    def reset(self):
        self.ctx_m().set('pagination', {})

    def follow_next(self):
        pagination = self.response.body().get('pagination').get('next').raw_str()
        self.ctx_m().set('pagination', pagination)

    def assert_no_next_page(self):
        self.judge.expectation(
            self.response.body().get('pagination').get('next').raw_str() is None,
            f"Next page actually is present"
        )
