from sommelier.behave_wrapper import LabelingMachine


class IdentifierRegistry:

    def __init__(self):
        self.context_manager = None

    def set_ctx_manager(self, context_manager):
        self.context_manager = context_manager

    def reset(self):
        self.context_manager.set('id_aliases', {})
        self.context_manager.declare('permanent_aliases')
        self.context_manager.set('id_aliases', {**self.context_manager.get('permanent_aliases')})
        self.context_manager.set('user_id', None)
        self.context_manager.set('roles', {})

    def create_alias_from_response(self, alias, key):
        # TODO a general response manager should exist
        # TODO identifier registry should be repurposed to UserRegistry
        # Try to get id from the last response data
        code = self.context_manager.status_code()

        self.context_manager.judge().expectation(
            code < 300,
            f'Response is not ok "{code}", cannot extract id',
        )
        json = self.context_manager.get_json()
        self.context_manager.of(LabelingMachine).create_alias(alias, json.get(key))

    def select_user(self, user_alias):
        user_id = self.context_manager.of(LabelingMachine).find(user_alias)
        self.context_manager.set('user_id', user_id)

    def grant_user_role(self, user_alias, role):
        user_id = self.context_manager.of(LabelingMachine).find(user_alias)
        self.context_manager.set(f'roles.{user_id}', role)
