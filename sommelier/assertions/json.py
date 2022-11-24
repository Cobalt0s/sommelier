from enum import Enum

from sommelier.behave_wrapper.logging import StringFormatter
from sommelier.behave_wrapper.tables import Carpenter


def _bool_operation(use_or):
    if use_or:
        return lambda x, y: x or y
    return lambda x, y: x and y


def assert_json_properties_in_object(context_manager, json):
    for zoom, expected_value in context_manager.of(Carpenter).builder().double().rows():
        given_value = str(json.get(zoom).raw())

        context_manager.judge().expectation(
            expected_value == given_value,
            StringFormatter('Expected %%alias! given %%alias! for key %%!', [
                expected_value,
                given_value,
                zoom,
            ]),
        )


def _assert_json_properties_in_list(context_manager, json, contains):
    for zoom, expected_value in context_manager.of(Carpenter).builder().double().rows():
        assertion_flag = not contains
        operation = _bool_operation(use_or=contains)
        for v in json.retriever_array():
            given_value = v.get(zoom).raw_str()
            assertion_flag = operation(assertion_flag, (expected_value == given_value))

        context_manager.judge().expectation(
            assertion_flag,
            StringFormatter('Expected %%alias! was not found inside %%!', [
                expected_value,
                zoom,
            ]),
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
