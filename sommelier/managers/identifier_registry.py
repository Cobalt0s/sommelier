from typing import Optional

from sommelier.behave_wrapper import FlowListener
from sommelier.behave_wrapper.aliases import LabelingMachine


class UserRegistry(FlowListener):

    def __init__(self):
        super().__init__(definitions=[
            ['user_id', None],
            ['roles', {}],
        ], managers={
            'labeling_machine': LabelingMachine,
        })
        self.labeling_machine: Optional[LabelingMachine] = None

    def select_user(self, user_alias):
        user_id = self.labeling_machine.find(user_alias)
        self.ctx_m().set('user_id', user_id)

    def grant_user_role(self, user_alias, role):
        user_id = self.labeling_machine.find(user_alias)
        self.ctx_m().set(f'roles.{user_id}', role)
