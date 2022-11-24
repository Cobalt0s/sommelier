from typing import Optional

from sommelier.behave_wrapper import LabelingMachine, ResponseJsonHolder
from sommelier.ctx_manager import FlowListener


class IdentifierRegistry(FlowListener):

    def __init__(self):
        super().__init__(definitions=[
            ['user_id', None],
            ['roles', {}],
        ], managers={
            'response': ResponseJsonHolder,
        })
        self.response: Optional[ResponseJsonHolder] = None

    def create_alias_from_response(self, alias, key):
        # TODO a general response manager should exist
        # TODO identifier registry should be repurposed to UserRegistry
        # Try to get id from the last response data
        code = self.response.status()

        self.ctx_m().judge().expectation(
            code < 300,
            f'Response is not ok "{code}", cannot extract id',
        )
        json = self.response.body()
        self.ctx_m().of(LabelingMachine).create_alias(alias, json.get(key))

    def select_user(self, user_alias):
        user_id = self.ctx_m().of(LabelingMachine).find(user_alias)
        self.ctx_m().set('user_id', user_id)

    def grant_user_role(self, user_alias, role):
        user_id = self.ctx_m().of(LabelingMachine).find(user_alias)
        self.ctx_m().set(f'roles.{user_id}', role)
