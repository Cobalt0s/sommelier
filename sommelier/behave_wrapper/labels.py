from sommelier.utils import StringUtils


class LabelingMachine(object):

    def __init__(self, context_manager) -> None:
        self.context_manager = context_manager
        context_manager.attach_manager(self)
        context_manager.declare('mode_permanent_aliases', False)
        context_manager.declare('aliases_permanent')
        context_manager.declare('aliases')

    def create_alias(self, name, value):
        value = str(value)
        self.context_manager.set(f'aliases.{name}', value)
        if self.is_permanent_mode():
            # This alias should be persisted for the whole test execution and should not be reset
            self.context_manager.set(f'aliases_permanent.{name}', value)
            self.context_manager.log_info(f"ID[{name}] with Value[{value}]")

    def is_permanent_mode(self) -> bool:
        return self.context_manager.get('mode_permanent_aliases')

    def toggle_permanent_mode(self, mode_status):
        self.context_manager.set('mode_permanent_aliases', mode_status)

    def find(self, name):
        identifier = self.context_manager.get(f'aliases.{name}')
        if identifier is not None:
            return identifier
        # if Cucumber test is written correctly alias/variable should've existed
        self.context_manager.judge().assumption(
            False,
            f'Alias "{name}" is not found since no id is associated with it',
        )

    def alias_of(self, value):
        aliases = self.context_manager.get('aliases')
        for k, v in aliases.items():
            if v == value:
                return k
        # There is no alias with such value
        return None


    def resolve_or_tautology(self, name):
        if StringUtils.is_variable(name):
            name = StringUtils.extract_variable(name)
            if name == StringUtils.RANDOM_VAR:
                return StringUtils.get_random_string(10)
            return self.find(name)
        return name


