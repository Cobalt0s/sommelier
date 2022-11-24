from behave.runner import Context

from sommelier.behave_wrapper import ContextManager


class ContextProvider(object):

    def __init__(self) -> None:
        super().__init__()
        self.context_manager = None

    def set(self, context: Context):
        if self.context_manager is not None:
            raise Exception('context was already set on ContextProvider')
        self.context_manager = ContextManager(context)

    def get_manager(self) -> ContextManager:
        if self.context_manager is None:
            raise Exception('tried getting Null Behave context, precondition: context must be set on provider')
        return self.context_manager
