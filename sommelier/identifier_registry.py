from sommelier.logging import Judge

from sommelier.utils import get_json
from sommelier.utils.identifier_resolver import resolve_alias, create_alias, clear_aliases


class IdentifierRegistry:

    def __init__(self):
        self.context = None

    def set_context(self, context):
        self.context = context

    def reset(self):
        clear_aliases(self.context)
        self.context.user_id = None

    def create_alias_from_response(self, alias_id, key=None):
        # Try to get id from the last response data
        code = self.context.result.status_code

        Judge(self.context).expectation(
            code < 300,
            f'Response is not ok "{code}", cannot extract id',
        )

        json = get_json(self.context)
        if key is not None:
            create_alias(self.context, alias_id, json.get(key))
        else:
            create_alias(self.context, alias_id, json.get('id'))

    def create_alias(self, alias_id, identifier):
        create_alias(self.context, alias_id, identifier)

    def resolve_alias(self, alias_id):
        return resolve_alias(self.context, alias_id)

    def select_user(self, user_alias):
        self.context.user_id = resolve_alias(self.context, user_alias)

