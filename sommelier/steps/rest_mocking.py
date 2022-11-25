from behave import given, then

from sommelier.behave_wrapper import judge
from sommelier.managers.api_mock import APIMockManager
from sommelier.utils import StringUtils

#
#
# Must instantiate APIMockManager to use these steps
#
#


@given('Associate svc {services} with ports {ports}')
def associate_svcs_ports(context, services, ports):
    api_mock_manager: APIMockManager = context.ctx_manager.of(APIMockManager)

    svc_list = StringUtils.comma_separated_to_list(services)
    port_list = StringUtils.comma_separated_to_list(ports)
    judge.assumption(len(svc_list) == len(port_list), "service names do not match ports")

    api_mock_manager.define_svc_ports(svc_list, port_list)


@given('Define {svc} mock on {rest_call} with status {status}')
def define_svc_mock(context, svc, rest_call, status):
    define_svc_mock_with_alias(context, svc, None, rest_call, status)


@given('Define {svc} mock aliased with {alias} on {rest_call} with status {status}')
def define_svc_mock_with_alias(context, svc, alias, rest_call, status):
    api_mock_manager: APIMockManager = context.ctx_manager.of(APIMockManager)
    rest_call_split = StringUtils.space_separated_to_list(rest_call)
    judge.assumption(
        len(rest_call_split) == 2, "rest call must have space between operation and url 'GET /cats/1'"
    )
    operation = rest_call_split[0]
    url = rest_call_split[1]
    api_mock_manager.create_mock(alias, svc, operation, url, status)


@given('Refer to mock {alias}, where')
def refer_to_mock(context, alias):
    api_mock_manager: APIMockManager = context.ctx_manager.of(APIMockManager)
    api_mock_manager.set_current(alias)


@given('mock with headers')
def mock_with_headers(context):
    api_mock_manager: APIMockManager = context.ctx_manager.of(APIMockManager)
    api_mock_manager.add_headers_to_current_mock()


@given('mock with request')
def mock_with_request(context):
    api_mock_manager: APIMockManager = context.ctx_manager.of(APIMockManager)
    api_mock_manager.add_request_to_current_mock()


@given('mock with response')
def mock_with_response(context):
    api_mock_manager: APIMockManager = context.ctx_manager.of(APIMockManager)
    api_mock_manager.add_response_to_current_mock()


@given('mock with response status {status}')
def mock_with_response_status(context, status):
    api_mock_manager: APIMockManager = context.ctx_manager.of(APIMockManager)
    api_mock_manager.add_response_status_to_current_mock(status)


@given('mock must be called {amount} times')
def mock_with_expected_calls(context, amount):
    api_mock_manager: APIMockManager = context.ctx_manager.of(APIMockManager)
    api_mock_manager.add_num_expected_calls_to_current_mock(amount)


@given('end of mock definition')
def mock_end(context):
    api_mock_manager: APIMockManager = context.ctx_manager.of(APIMockManager)
    api_mock_manager.end_mock_definition()


@then('All service mocks are satisfied')
def check_all_mocks(context):
    api_mock_manager: APIMockManager = context.ctx_manager.of(APIMockManager)
    api_mock_manager.is_satisfied()


@given('Mocks on {svcs} are removed')
def mock_svc_remove(context, svcs):
    api_mock_manager: APIMockManager = context.ctx_manager.of(APIMockManager)
    services = StringUtils.comma_separated_to_list(svcs)
    for svc in services:
        api_mock_manager.remove_svc(svc)


@given('All mocks are cleared')
def mock_clear_all(context):
    api_mock_manager: APIMockManager = context.ctx_manager.of(APIMockManager)
    api_mock_manager.clear_mocks()


@given('Mock named {alias} is removed')
def mock_name_remove(context, alias):
    api_mock_manager: APIMockManager = context.ctx_manager.of(APIMockManager)
    api_mock_manager.remove_mock(alias)
