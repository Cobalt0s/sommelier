from sommelier.ctx_manager import FlowListener


class LabelingMachine(FlowListener):

    def __init__(self) -> None:
        super().__init__(definitions=[
            ['mode_permanent_aliases', False],
            ['aliases_permanent', {}],
            ['aliases', {}],
        ], permanent={
            'aliases_permanent': 'aliases'
        })

    def create_alias(self, name, value):
        value = str(value)
        self.ctx_m().set(f'aliases.{name}', value)
        if self.__is_permanent_mode():
            # This alias should be persisted for the whole test execution and should not be reset
            self.ctx_m().set(f'aliases_permanent.{name}', value)
            self.ctx_m().log_info(f"ID[{name}] with Value[{value}]")

    def __is_permanent_mode(self) -> bool:
        return self.ctx_m().get('mode_permanent_aliases')

    def toggle_permanent_mode(self, mode_status):
        self.ctx_m().set('mode_permanent_aliases', mode_status)

    def find(self, name):
        identifier = self.ctx_m().get(f'aliases.{name}')
        if identifier is not None:
            return identifier
        # if Cucumber test is written correctly alias/variable should've existed
        self.ctx_m().judge().assumption(
            False,
            f'Alias "{name}" is not found since no id is associated with it',
        )

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
