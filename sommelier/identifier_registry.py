from sommelier.utils.identifier_resolver import resolve_alias, create_alias


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

    def create_alias_from_response(self, alias_id, key=None):
        # Try to get id from the last response data
        code = self.context_manager.status_code()

        self.context_manager.judge().expectation(
            code < 300,
            f'Response is not ok "{code}", cannot extract id',
        )

        json = self.context_manager.get_json()
        if key is not None:
            create_alias(self.context_manager, alias_id, json.get(key))
        else:
            create_alias(self.context_manager, alias_id, json.get('id'))

    def create_alias(self, alias_id, identifier):
        create_alias(self.context_manager, alias_id, identifier)

    def resolve_alias(self, alias_id):
        return resolve_alias(self.context_manager, alias_id)

    def select_user(self, user_alias):
        self.context_manager.set('user_id', resolve_alias(self.context_manager, user_alias))

    def grant_user_role(self, user_alias, role):
        user_id = resolve_alias(self.context_manager, user_alias)
        self.context_manager.set(f'roles.{user_id}', role)
