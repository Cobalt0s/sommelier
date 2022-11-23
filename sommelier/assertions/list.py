from sommelier.logging import find_alias


def context_contains(context_manager, first_key, second_key, value):
    data = context_manager.get_json()
    if data.has(first_key):
        _list_search(context_manager, data.get(first_key).raw_array(), second_key, value, expected_to_find=True)
    else:
        assert True


def context_missing(context_manager, first_key, second_key, value):
    data = context_manager.get_json()
    if data.has(first_key):
        _list_search(context_manager, data.get(first_key).raw_array(), second_key, value, expected_to_find=False)
    else:
        assert True


def _list_search(context_manager, item_list, key, value, expected_to_find=True):
    assert item_list is not None and item_list is not []

    found = False
    for item in item_list:
        if key in item:
            found = item[key] == value
            if found:
                break

    found_text = 'should be present' if expected_to_find else 'should be missing'

    context_manager.judge().expectation(
        found == expected_to_find,
        f"Entry ['{key}': '{find_alias(context_manager, value)}'] {found_text}",
        )


class ResponseListChecker(object):

    def __init__(self, context_manager, identifier_registry, nested_key):
        self.context_manager = context_manager
        self.identifier_registry = identifier_registry
        self.nested_key = nested_key

    def contains(self, k, v):
        context_contains(self.context_manager, self.nested_key, k, v)

    def missing(self, k, v):
        context_missing(self.context_manager, self.nested_key, k, v)

    def contains_id(self, identifier):
        self.contains('id', self.identifier_registry.resolve_alias(identifier))

    def missing_id(self, identifier):
        self.missing('id', self.identifier_registry.resolve_alias(identifier))
