from typing import Optional

from sommelier.behave_wrapper import FlowListener
from sommelier.behave_wrapper.aliases import LabelingMachine


class UserRegistry(FlowListener):

    def __init__(self):
        super().__init__(definitions=[
            ['user_id', None],
            ['roles', {}],
            ['roles_permanent', {}],
            ['apps', {}],
            ['apps_permanent', {}],
        ], permanent={
            'apps_permanent': 'apps',
            'roles_permanent': 'roles'
        }, managers={
            'labeling_machine': LabelingMachine,
        })
        self.labeling_machine: Optional[LabelingMachine] = None

    def select_user(self, user_alias):
        user_id = self.labeling_machine.find(user_alias)
        self.ctx_m().set('user_id', user_id)

    def grant_user_role(self, user_alias, role):
        user_id = self.labeling_machine.find(user_alias)
        self.ctx_m().set(f'roles.{user_id}', role)
        if self.is_permanent_mode():
            self.ctx_m().set(f'roles_permanent.{user_id}', role)

    def assign_user_app(self, user_alias, app_id):
        user_id = self.labeling_machine.find(user_alias)
        self.ctx_m().set(f'apps.{user_id}', app_id)
        if self.is_permanent_mode():
            self.ctx_m().set(f'apps_permanent.{user_id}', app_id)

    def get_user_id(self):
        return self.ctx_m().get('user_id')

    def get_user_role(self):
        user = self.get_user_id()
        role = ''
        roles = self.ctx_m().get('roles')
        if user in roles:
            role = roles[user]
        return role

    def get_user_app(self):
        user = self.get_user_id()
        app_id = 'no-app-name'
        apps = self.ctx_m().get('apps')
        if user in apps:
            app_id = apps[user]
        return app_id
