import copy
from typing import List

from sommelier.behave_wrapper import ContextManager
from sommelier.behave_wrapper.provider import ContextProvider


class FlowListener(object):

    # * definitions is a list of 2d lists
    #   each 2d list includes variable name that should be declared on Behave context
    #   and variable value which is a default for that data type
    # * permanent is a map of pairs
    #   key is variable name -- holds set of values reused in every scenario, aka permanent
    #   value is variable name -- holds temporary + permanent values (automatically sets it up)
    # * dependencies is a dict of names to managers which are attached to ContextManager
    def __init__(self,
                 definitions: List[list] = None,
                 permanent: dict = None,
                 managers: dict = None) -> None:
        super().__init__()
        global_test_flow_controller.register(self)
        if definitions is None:
            definitions = []
        self.__variable_definitions = definitions
        if permanent is None:
            permanent = {}
        self.__permanent_variable_definitions = permanent
        if managers is None:
            managers = {}
        self.__manager_dependencies = managers

    @staticmethod
    def ctx_m() -> ContextManager:
        # every implementation should get context manager only this way
        return global_context_provider.get_manager()

    def before_all(self):
        for name, default_val in self._instantiate_default_vars():
            self.ctx_m().declare(name, default_val)
        context_manager = global_context_provider.get_manager()
        for name, manager_clazz in self.__manager_dependencies.items():
            manager = context_manager.of(manager_clazz)
            setattr(self, name, manager)

    def before_feature(self):
        pass

    def before_scenario(self):
        for name, default_val in self._instantiate_default_vars():
            if name not in self.__permanent_variable_definitions:
                # omit resetting permanent variables
                self.ctx_m().set(name, default_val)

        for permanent_name, name in self.__permanent_variable_definitions.items():
            # no shared objects should exist with the permanent version of a variable declaration
            values = copy.deepcopy(self.ctx_m().get(permanent_name))
            # prepopulate with permanent fields
            self.ctx_m().set(name, values)

    def before_step(self):
        pass

    def after_step(self):
        pass

    def after_scenario(self):
        pass

    def after_feature(self):
        pass

    def after_all(self):
        pass

    def _instantiate_default_vars(self):
        # create a deep copy as we don't want to pass pointer and hence mess up default values
        # this ensures that default variable definitions are IMMUTABLE, they serve as Template
        instantiated = []
        # lists of 2d lists is unpacked
        for name, v in self.__variable_definitions:
            instantiated.append((name, copy.deepcopy(v)))
        return instantiated


class FlowController(object):
    def __init__(self) -> None:
        super().__init__()
        self.flow_listeners = []

    def register(self, listener: FlowListener):
        self.flow_listeners.append(listener)

    def before_all(self, context):
        global_context_provider.set(context)
        context_manager = global_context_provider.get_manager()

        for listener in self.flow_listeners:
            context_manager.attach_manager(listener)
            listener.before_all()

    def before_feature(self):
        for listener in self.flow_listeners:
            listener.before_feature()

    def before_scenario(self):
        for listener in self.flow_listeners:
            listener.before_scenario()

    def before_step(self):
        for listener in self.flow_listeners:
            listener.before_step()

    def after_step(self):
        for listener in self.flow_listeners:
            listener.after_step()

    def after_scenario(self):
        for listener in self.flow_listeners:
            listener.after_scenario()

    def after_feature(self):
        for listener in self.flow_listeners:
            listener.after_feature()

    def after_all(self):
        for listener in self.flow_listeners:
            listener.after_all()


global_context_provider = ContextProvider()
global_test_flow_controller = FlowController()
