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

    def get_user_id(self):
        return self.ctx_m().get('user_id')

    def get_user_role(self):
        user = self.get_user_id()
        role = '0'
        roles = self.ctx_m().get('roles')
        if user in roles:
            role = roles[user]
        return role

