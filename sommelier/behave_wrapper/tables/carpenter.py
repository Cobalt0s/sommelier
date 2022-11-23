from sommelier.behave_wrapper.tables.builders import TableBuilder, CustomInCodeTable


class Carpenter(object):

    def __init__(self, context_manager) -> None:
        self.context_manager = context_manager
        context_manager.attach_manager(self)
        context_manager.declare('payload', None)

    def builder(self) -> TableBuilder:
        payload = self.context_manager.get('payload')
        if payload is not None:
            # Clear the payload variable
            # user provided it only as a replacement of behave table via code
            self.context_manager.set('payload', None)
            return CustomInCodeTable(self.context_manager, payload)
        return TableBuilder(self.context_manager)
