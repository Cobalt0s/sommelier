from sommelier.behave_wrapper import FlowListener
from sommelier.behave_wrapper.tables.builders import TableBuilder, CustomInCodeTable


class Carpenter(FlowListener):

    def __init__(self) -> None:
        super().__init__(definitions=[
            ['payload', None],
        ])

    def builder(self) -> TableBuilder:
        payload = self.ctx_m().get('payload')
        if payload is not None:
            # Clear the payload variable
            # user provided it only as a replacement of behave table via code
            self.ctx_m().set('payload', None)
            return CustomInCodeTable(self.ctx_m(), payload)
        return TableBuilder(self.ctx_m())

    def use(self, custom_table):
        self.ctx_m().set('payload', custom_table)
