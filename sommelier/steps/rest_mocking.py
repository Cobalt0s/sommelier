from behave import given, then

from sommelier.utils.string_manipulations import StringUtils

from features import apiMockManager


@given('Associate svc {services} with ports {ports}')
def associate_svcs_ports(context, services, ports):
    svc_list = StringUtils.comma_separated_to_list(services)
    port_list = StringUtils.comma_separated_to_list(ports)
    context.ctx_manager.judge().assumption(len(svc_list) == len(port_list), "service names do not match ports")

    apiMockManager.define_svc_ports(svc_list, port_list)


@given('Define {svc} mock on {rest_call} with status {status}')
def define_svc_mock(context, svc, rest_call, status):
    define_svc_mock_with_alias(context, svc, None, rest_call, status)


@given('Define {svc} mock aliased with {alias} on {rest_call} with status {status}')
def define_svc_mock_with_alias(context, svc, alias, rest_call, status):
    rest_call_split = StringUtils.space_separated_to_list(rest_call)
    context.ctx_manager.judge().assumption(
        len(rest_call_split) == 2, "rest call must have space between operation and url 'GET /cats/1'"
    )
    operation = rest_call_split[0]
    url = rest_call_split[1]
    apiMockManager.create_mock(alias, svc, operation, url, status)


@given('Refer to mock {alias}, where')
def refer_to_mock(context, alias):
    apiMockManager.set_current(alias)


@given('mock with headers')
def mock_with_headers(context):
    apiMockManager.add_headers_to_current_mock()


@given('mock with request')
def mock_with_request(context):
    apiMockManager.add_request_to_current_mock()


@given('mock with response')
def mock_with_response(context):
    apiMockManager.add_response_to_current_mock()


@given('mock with response status {status}')
def mock_with_response_status(context, status):
    apiMockManager.add_response_status_to_current_mock(status)


@given('mock must be called {amount} times')
def mock_with_expected_calls(context, amount):
    apiMockManager.add_num_expected_calls_to_current_mock(amount)


@given('end of mock definition')
def mock_end(context):
    apiMockManager.end_mock_definition()


@then('All service mocks are satisfied')
def check_all_mocks(context):
    apiMockManager.is_satisfied()


@given('Mocks on {svcs} are removed')
def mock_svc_remove(context, svcs):
    services = StringUtils.comma_separated_to_list(svcs)
    for svc in services:
        apiMockManager.remove_svc(svc)


@given('All mocks are cleared')
def mock_clear_all(context):
    apiMockManager.clear_mocks()


@given('Mock named {alias} is removed')
def mock_name_remove(context, alias):
    apiMockManager.remove_mock(alias)
