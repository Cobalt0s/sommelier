from sommelier.behave_wrapper import LabelingMachine, ResponseJsonHolder

from sommelier.behave_wrapper.logging import StringFormatter, Judge


def context_contains(context_manager, first_key, second_key, value):
    data = context_manager.of(ResponseJsonHolder).body()
    if data.has(first_key):
        _list_search(context_manager, data.get(first_key).raw_array(), second_key, value, expected_to_find=True)
    else:
        assert True


def context_missing(context_manager, first_key, second_key, value):
    data = context_manager.of(ResponseJsonHolder).body()
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

    context_manager.of(Judge).expectation(
        found == expected_to_find,
        StringFormatter(f"Entry ['%%!': '%%alias!'] %%!", [
            key,
            value,
            found_text,
        ]),
    )


class ResponseListChecker(object):

    def __init__(self, context_manager, nested_key):
        self.context_manager = context_manager
        self.nested_key = nested_key
        self.labeling_machine = self.context_manager.of(LabelingMachine)

    def contains(self, k, v):
        context_contains(self.context_manager, self.nested_key, k, v)

    def missing(self, k, v):
        context_missing(self.context_manager, self.nested_key, k, v)

    def contains_id(self, identifier):
        self.contains('id', self.labeling_machine.find(identifier))

    def missing_id(self, identifier):
        self.missing('id', self.labeling_machine.find(identifier))
