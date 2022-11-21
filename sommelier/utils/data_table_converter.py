import json

from sommelier.utils.identifier_resolver import resolve_id_or_tautology
from sommelier.utils.string_manipulations import StringUtils


def table_as_2d_list(context_manager, position_of_value=1):
    list_2d = _table_to_2d_list(get_table(context_manager))

    result = []
    for item in list_2d:
        value = item[position_of_value]
        if StringUtils.is_array(value):
            value_result = []
            arr = StringUtils.extract_array(value)
            for x in StringUtils.comma_separated_to_list(arr):
                if x:
                    value_result.append(parse_json_value(context_manager, x))
        else:
            value_result = parse_json_value(context_manager, value)

        key = item[0]
        if position_of_value == 1:
            result.append([key, value_result])
        else:
            result.append(value_result)
    return result


def parse_json_value(context_manager, value):
    if value == "True" or value == "true":
        return True
    if value == "False" or value == "false":
        return False
    if value == "None" or value.lower() == "null":
        return None
    if value == "{}":
        return {}
    return resolve_id_or_tautology(context_manager, value)


def get_table(context_manager):
    payload = context_manager.get('payload')
    if payload is not None:
        table = []
        for k in payload:
            v = payload[k]
            if isinstance(v, dict):
                raise Exception("nested dictionaries for context.payload is not supported")
            table.append([k, v])
        # Clear the payload variable as it is temporary passed for side effects
        context_manager.set('payload', None)
        return CustomTable(table)
    return context_manager.table()


class CustomTable:

    def __init__(self, rows):
        self.rows = rows


def _table_to_2d_list(table):
    if isinstance(table, CustomTable):
        return table.rows

    if table is None:
        return []
    result = [table.headings]
    for row in table:
        result.append(row.cells)
    return result


def expand_nested_keys(payload):
    # To represent json in flattened form use `.` for specifying nested fields
    # * Given json:
    #
    # {name: Bob, education: {level: bachelor, grade: good}}
    #
    # * Flattened form:
    #
    # name: Bob
    # education.level: bachelor
    # eduction.grade: good

    nested_keys = []
    for k in payload:
        if '.' in k:
            nested_keys.append(k)

    for k in nested_keys:
        value = payload[k]
        current_obj = payload
        # Zoom into the key which will create new objects or reuse existing
        key_list = k.split('.')
        for i in range(len(key_list)):
            subkey = key_list[i]
            if subkey in current_obj:
                # reuse existing object and keep zooming
                current_obj = current_obj[subkey]
            else:
                if i == len(key_list) - 1:
                    # we reached the end and need to save value
                    current_obj[subkey] = value
                else:
                    # we are still zooming
                    current_obj[subkey] = {}
                current_obj = current_obj[subkey]

        # nobody needs fully qualified key at the end of this procedure
        del payload[k]

    return _convert_indexed_obj_to_arr(payload)


def _convert_indexed_obj_to_arr(payload):
    if not isinstance(payload, dict):
        return payload
    arr = []
    arr_key = None
    for k in payload:
        if StringUtils.is_array(k):
            arr_key = k
            arr.append(payload[k])
        else:
            payload[k] = _convert_indexed_obj_to_arr(payload[k])

    if arr_key is not None:
        return arr
    else:
        return payload


def display(data):
    print(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))


def perform_check(given, expected):
    result = expand_nested_keys(given)
    ok = (expected == result)
    if not ok:
        display(expected)
        display(result)
    else:
        print("Successful")


if __name__ == '__main__':
    test_cases = [
        {
            "given": {
                "data.[0].user": {
                    "name": "John"
                },
                "data.[1].user": {
                    "name": "Bob"
                }
            },
            "expected": {
                "data": [
                    {"user": {"name": "John"}},
                    {"user": {"name": "Bob"}}
                ]
            }
        },
        {
            "given": {
                "[0]": 1,
                "[1]": 2,
            },
            "expected": [1, 2]
        },
        {
            "given": {
                "data.first.[0]": "apple",
                "data.first.[1]": "banana",
                "data.second.[0]": "kiwi",
                "data.second.[1].box": "carrots",
            },
            "expected": {
                "data": {
                    "first": [
                        "apple",
                        "banana",
                    ],
                    "second": [
                        "kiwi",
                        {"box": "carrots"},
                    ]
                }
            }
        }
    ]

    for v in test_cases:
        perform_check(v["given"], v["expected"])
