import json
from abc import abstractmethod
from typing import Tuple

from sommelier.utils import StringUtils


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


if __name__ == '__main__':
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


class TableXDimensions(object):
    # Represents parsed Behave Table

    def __init__(self, data) -> None:
        self.data = data

    @abstractmethod
    def rows(self):
        # Can iterate over each row
        pass


class Table2D(TableXDimensions):
    # Contains 2 columns

    def __init__(self, data) -> None:
        super().__init__(data)

    def rows(self) -> Tuple[str, str]:
        for row in self.data:
            yield str(row[0]), str(row[1])

    def dict(self) -> dict:
        # convert from CSV notation to JSON aka Python dictionary
        payload = dict(self.data)
        return expand_nested_keys(payload)


class Table1D(TableXDimensions):
    # Contains 1 column

    def __init__(self, data) -> None:
        super().__init__(data)

    def rows(self) -> str:
        for row in self.data:
            yield str(row[0])

    def list(self) -> list:
        return self.data

