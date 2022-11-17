from sommelier.logging import find_alias

from sommelier.utils.data_table_converter import table_as_2d_list


def assert_json_properties_in_object(context_manager, json):
    for row in table_as_2d_list(context_manager):
        zoom = row[0]
        expected_value = str(row[1])
        given_value = str(json.get(zoom).raw())

        context_manager.judge().expectation(
            expected_value == given_value,
            f"Expected {find_alias(context_manager, expected_value)} given {find_alias(context_manager, given_value)} for key {zoom}",
        )


def assert_json_properties_in_list(context_manager, json):
    _assert_json_properties_in_list(context_manager, json, contains=True)


def assert_json_properties_not_in_list(context_manager, json):
    _assert_json_properties_in_list(context_manager, json, contains=False)


def _assert_json_properties_in_list(context_manager, json, contains):
    for row in table_as_2d_list(context_manager):
        zoom = row[0]
        expected_value = str(row[1])

        assertion_flag = not contains
        operation = _bool_operation(use_or=contains)
        for v in json.retriever_array():
            given_value = v.get(zoom).raw_str()
            assertion_flag = operation(assertion_flag, (expected_value == given_value))

        context_manager.judge().expectation(
            assertion_flag,
            f"Expected {find_alias(context_manager, expected_value)} was not found inside {zoom}",
        )


def _bool_operation(use_or):
    if use_or:
        return lambda x, y: x or y
    return lambda x, y: x and y


def require_var(variable, name):
    if variable is None:
        raise Exception(f"var {name} is not set")
