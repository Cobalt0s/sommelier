from core.utils import get_json


def context_contains(context, first_key, second_key, value):
    json = get_json(context)
    if first_key in json:
        _list_search(json[first_key], second_key, value, expected_to_find=True)
    else:
        assert True


def context_missing(context, first_key, second_key, value):
    json = get_json(context)
    if first_key in json:
        _list_search(json[first_key], second_key, value, expected_to_find=False)
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

    found_text = 'not found' if expected_to_find else 'found'
    assert found == expected_to_find, f"Element with key '{key}' and value '{value}' in {item_list} was {found_text}"
