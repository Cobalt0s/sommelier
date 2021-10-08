from sommelier.utils import get_json
from sommelier.utils.logger import Judge


def context_contains(context, first_key, second_key, value):
    data = get_json(context)
    if data.has(first_key):
        _list_search(context, data.get(first_key).raw_array(), second_key, value, expected_to_find=True)
    else:
        assert True


def context_missing(context, first_key, second_key, value):
    data = get_json(context)
    if data.has(first_key):
        _list_search(context, data.get(first_key).raw_array(), second_key, value, expected_to_find=False)
    else:
        assert True


def _list_search(context, item_list, key, value, expected_to_find=True):
    assert item_list is not None and item_list is not []

    found = False
    for item in item_list:
        if key in item:
            found = item[key] == value
            if found:
                break

    found_text = 'should be present' if expected_to_find else 'should be missing'

    Judge(context).expectation(
        found == expected_to_find,
        f"Entry ('{key}': '{value}') {found_text}",
    )


