from sommelier.utils.logger import Judge

from sommelier.utils import get_json


class PaginationNavigator:

    def __init__(self):
        self.context = None

    def set_context(self, context):
        self.context = context

    def reset(self):
        self.context.pagination = {}

    def follow_next(self):
        self.context.pagination = get_json(self.context).get('pagination').get('next').raw_str()

    def assert_no_next_page(self):
        Judge(self.context).expectation(
            get_json(self.context).get('pagination').get('next').raw_str() is None,
            f"Next page actually is present"
        )

