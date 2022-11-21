import time
from uuid import uuid4

from behave import given, then, when

from sommelier import response_validator, pagination_navigator, identifier_registry
from sommelier.utils.string_manipulations import StringUtils


@then('Response status is {status}')
def check_response_status(context, status):
    response_validator.assert_status(status)


@then('Failure with code {code} and details')
def check_response_failure_code_and_details_json(context, code):
    response_validator.check_failure(code)


@then('Failure with code {code} on {details}')
def check_response_failure_code_and_details(context, code, details):
    response_validator.check_failure(code, details)


@then('Contains properties in response body')
def contains_properties(context):
    response_validator.contains_data()


@then('Contains keys in response body')
def contains_keys(context):
    response_validator.contains_keys()


@then('Contains properties inside object named {item_key}')
def contains_properties(context, item_key):
    response_validator.contains_data(item_key, response_validator.IN_OBJECT)


@then('Contains properties inside list named {item_key}')
def contains_properties(context, item_key):
    response_validator.contains_data(item_key, response_validator.IN_LIST)


@then('Does not contain properties inside list {item_key}')
def contains_properties(context, item_key):
    response_validator.contains_data(item_key, response_validator.NOT_IN_LIST)


@then('Number of {zoom} on page is {amount}')
def count_elements_on_page(context, zoom, amount):
    response_validator.count_data(zoom, amount)


@when('Save id as {item_id}')
def save_item_id(context, item_id):
    identifier_registry.create_alias_from_response(item_id)


@when('Save id located in {key} as {item_id}')
def save_item_id_with_zoom(context, key, item_id):
    identifier_registry.create_alias_from_response(item_id, key)


@given('Define uuid for list {definitions}')
def define_uuids(context, definitions):
    for d in StringUtils.comma_separated_to_list(definitions):
        identifier_registry.create_alias(d, str(uuid4()))


@when('I use next page cursor')
def prepare_to_use_pagination(context):
    pagination_navigator.follow_next()


@when('I clear pagination parameters')
def clear_pagination(context):
    pagination_navigator.reset()


@then('Next page does not exist')
def next_page_missing(context):
    pagination_navigator.assert_no_next_page()


@when('After waiting for {duration} seconds')
def wait_time(context, duration):
    time.sleep(float(duration))


@when('After waiting for {duration} ms')
def wait_ms(context, duration):
    ms = float(duration)
    wait_time(context, ms * 0.001)


@when('Selecting one of the objects and saving as {item_id}')
def select_object_and_save(context, item_id):
    json = context.ctx_manager.get_json()
    identifier = json.get('data.[0].id').raw_str()
    identifier_registry.create_alias(item_id, identifier)
