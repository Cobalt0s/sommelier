from sommelier.ctx_manager import FlowListener


class PaginationNavigator(FlowListener):

    def __init__(self):
        super().__init__(definitions=[
            ['pagination', {}],
        ])

    def reset(self):
        self.ctx_m().set('pagination', {})

    def follow_next(self):
        pagination = self.ctx_m().get_json().get('pagination').get('next').raw_str()
        self.ctx_m().set('pagination', pagination)

    def assert_no_next_page(self):
        self.ctx_m().judge().expectation(
            self.ctx_m().get_json().get('pagination').get('next').raw_str() is None,
            f"Next page actually is present"
        )
