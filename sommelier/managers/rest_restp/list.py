
from sommelier.behave_wrapper import response_json_holder, judge, labeling_machine
from sommelier.behave_wrapper.logging import StringFormatter


def context_contains(first_key, second_key, value):
    data = response_json_holder.body()
    if data.has(first_key):
        _list_search(data.get(first_key).raw_array(), second_key, value, expected_to_find=True)
    else:
        assert True


def context_missing(first_key, second_key, value):
    data = response_json_holder.body()
    if data.has(first_key):
        _list_search(data.get(first_key).raw_array(), second_key, value, expected_to_find=False)
    else:
        assert True


def _list_search(item_list, key, value, expected_to_find=True):
    assert item_list is not None and item_list is not []

    found = False
    for item in item_list:
        if key in item:
            found = item[key] == value
            if found:
                break

    found_text = 'should be present' if expected_to_find else 'should be missing'

    judge.expectation(
        found == expected_to_find,
        StringFormatter(f"Entry ['%%!': '%%alias!'] %%!", [
            key,
            value,
            found_text,
        ]),
    )


class ResponseListChecker(object):

    def __init__(self, nested_key):
        self.nested_key = nested_key

    def contains(self, k, v):
        context_contains(self.nested_key, k, v)

    def missing(self, k, v):
        context_missing(self.nested_key, k, v)

    def contains_id(self, identifier):
        self.contains('id', labeling_machine.find(identifier))

    def missing_id(self, identifier):
        self.missing('id', labeling_machine.find(identifier))
