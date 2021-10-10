from sommelier.utils.logger import Judge

from sommelier.utils.data_table_converter import table_as_2d_list


def assert_json_properties_in_object(context, json):
    for row in table_as_2d_list(context):
        zoom = row[0]
        expected_value = str(row[1])
        given_value = str(json.get(zoom).raw())

        Judge(context).expectation(
            expected_value == given_value,
            f"Expected {expected_value} given {given_value} for key {zoom}",
        )


def assert_json_properties_in_list(context, json):
    _assert_json_properties_in_list(context, json, contains=True)


def assert_json_properties_not_in_list(context, json):
    _assert_json_properties_in_list(context, json, contains=False)


def _assert_json_properties_in_list(context, json, contains):
    for row in table_as_2d_list(context):
        zoom = row[0]
        expected_value = str(row[1])

        assertion_flag = not contains
        operation = _bool_operation(use_or=contains)
        for v in json.retriever_array():
            given_value = v.get(zoom).raw_str()
            assertion_flag = operation(assertion_flag, (expected_value == given_value))

        Judge(context).expectation(
            assertion_flag,
            f"Expected {expected_value} was not find inside {zoom}",
        )


def _bool_operation(use_or):
    if use_or:
        return lambda x, y: x or y
    return lambda x, y: x and y
