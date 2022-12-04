from behave import given, then

from sommelier.behave_wrapper import judge
from sommelier.managers import api_mock
from sommelier.utils import StringUtils

#
#
# Out of the Box
#
#


@given('Define mock on {rest_call} with status {status}')
def define_svc_mock(context, rest_call, status):
    define_svc_mock_with_alias(context, alias=None, rest_call=rest_call, status=status)


@given('Define mock aliased {alias} on {rest_call} with status {status}')
def define_svc_mock_with_alias(context, alias, rest_call, status):
    rest_call_split = StringUtils.space_separated_to_list(rest_call)
    judge.assumption(
        len(rest_call_split) == 2, "rest call must have space between operation and url 'GET /cats/1'"
    )
    operation = rest_call_split[0]
    url = rest_call_split[1]
    if alias is None:
        alias = StringUtils.get_random_string(3)
    api_mock.create_mock(alias, operation, url, status)


@given('Refer to mock {alias}, where')
def refer_to_mock(context, alias):
    api_mock.set_current(alias)


@given('mock with headers')
def mock_with_headers(context):
    api_mock.add_headers_to_current_mock()


@given('mock with request')
def mock_with_request(context):
    api_mock.add_request_to_current_mock()


@given('mock with response')
def mock_with_response(context):
    api_mock.add_response_to_current_mock()


@given('mock with response status {status}')
def mock_with_response_status(context, status):
    api_mock.add_response_status_to_current_mock(status)


@given('mock must be called {amount} times')
def mock_with_expected_calls(context, amount):
    api_mock.add_num_expected_calls_to_current_mock(amount)


@given('end of mock definition')
def mock_end(context):
    api_mock.end_mock_definition()


@then('All service mocks are satisfied')
def check_all_mocks(context):
    api_mock.is_satisfied()


@given('All mocks are cleared')
def mock_clear_all(context):
    api_mock.clear_mocks()


@given('Ignore calls to mock service')
def ignore_calls_mock_svc(context):
    api_mock.ignore_calls()
