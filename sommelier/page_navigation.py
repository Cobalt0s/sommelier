from sommelier.logging import Judge

from sommelier.utils import get_json


class PaginationNavigator:

    def __init__(self):
        self.context_manager = None

    def set_ctx_manager(self, context_manager):
        self.context_manager = context_manager

    def reset(self):
        self.context_manager.set('pagination', {})

    def follow_next(self):
        pagination = self.context_manager.get_json().get('pagination').get('next').raw_str()
        self.context_manager.set('pagination', pagination)

    def assert_no_next_page(self):
        self.context_manager.judge().expectation(
            self.context_manager.get_json().get('pagination').get('next').raw_str() is None,
            f"Next page actually is present"
        )
