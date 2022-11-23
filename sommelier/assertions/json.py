from enum import Enum

from sommelier.logging import find_alias


def _bool_operation(use_or):
    if use_or:
        return lambda x, y: x or y
    return lambda x, y: x and y


def assert_json_properties_in_object(context_manager, json):
    for zoom, expected_value in context_manager.get_table_2d().items():
        given_value = str(json.get(zoom).raw())

        context_manager.judge().expectation(
            expected_value == given_value,
            f"Expected {find_alias(context_manager, expected_value)} given {find_alias(context_manager, given_value)} for key {zoom}",
        )


def _assert_json_properties_in_list(context_manager, json, contains):
    for zoom, expected_value in context_manager.get_table_2d().items():
        assertion_flag = not contains
        operation = _bool_operation(use_or=contains)
        for v in json.retriever_array():
            given_value = v.get(zoom).raw_str()
            assertion_flag = operation(assertion_flag, (expected_value == given_value))

        context_manager.judge().expectation(
            assertion_flag,
            f"Expected {find_alias(context_manager, expected_value)} was not found inside {zoom}",
        )


def assert_json_properties_in_list(context_manager, json):
    _assert_json_properties_in_list(context_manager, json, contains=True)


def assert_json_properties_not_in_list(context_manager, json):
    _assert_json_properties_in_list(context_manager, json, contains=False)


class AssertionMethod(Enum):
    IN_OBJECT = 1
    IN_LIST = 2
    NOT_IN_LIST = 3


class AssertionMethodProvider:
    METHODS = {
        AssertionMethod.IN_OBJECT: assert_json_properties_in_object,
        AssertionMethod.IN_LIST: assert_json_properties_in_list,
        AssertionMethod.NOT_IN_LIST: assert_json_properties_not_in_list,
    }

    @staticmethod
    def of(assertion_method: AssertionMethod):
        return AssertionMethodProvider.METHODS[assertion_method]
