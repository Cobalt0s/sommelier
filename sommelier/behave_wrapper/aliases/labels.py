from sommelier.behave_wrapper import FlowListener
from sommelier.utils import SimpleLogger


class UnknownAlias(Exception):

    def __init__(self, name) -> None:
        super().__init__(f'Alias "{name}" is not found since no id is associated with it')


class LabelingMachine(FlowListener):

    def __init__(self) -> None:
        super().__init__(definitions=[
            ['aliases_permanent', {}],
            ['aliases', {}],
        ], permanent={
            'aliases_permanent': 'aliases'
        })

    def create_alias(self, name: str, value: any):
        self.ctx_m().set(f'aliases.{name}', value)
        if self.is_permanent_mode():
            # This alias should be persisted for the whole test execution and should not be reset
            self.ctx_m().set(f'aliases_permanent.{name}', value)
            SimpleLogger.info(f"ID[{name}] with Value[{str(value)}]")

    def find(self, name):
        identifier = self.ctx_m().get(f'aliases.{name}')
        if identifier is not None:
            return identifier
        raise UnknownAlias(name)

    def find_many(self, names: list) -> list:
        result = []
        for n in names:
            result.append(self.find(n))
        return result

    def alias_of(self, value):
        aliases = self.ctx_m().get('aliases')
        for k, v in aliases.items():
            if v == value:
                return k
        # There is no alias with such value
        return None
