import time
from uuid import uuid4

from behave import given, then, when

from sommelier import response_validator, pagination_navigator, identifier_registry
from sommelier.utils import get_json


@then('Response status is {status}')
def check_response_status(context, status):
    response_validator.assert_status(status)


@then('Failure with code {code} and details')
def check_response_failure_code_and_details_json(context, code):
    response_validator.check_failure(code)


@then('Failure with code {code} on {details}')
def check_response_failure_code_and_details(context, code, details):
    response_validator.check_failure(code, details)


@then('Missing required keys')
def missing_required_keys(context):
    response_validator.missing_keys()


@then('Contains properties in response body')
def contains_properties(context):
    response_validator.contains_data()


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


@then('Data array contains element')
def data_array_contains_element(context):
    response_validator.contains_data_in_array()


@when('Save id as {item_id}')
def save_item_id(context, item_id):
    identifier_registry.create_alias_from_response(item_id)


@given('Define uuid for list {definitions}')
def define_uuids(context, definitions):
    for d in definitions.replace(" ", "").split(","):
        identifier_registry.create_alias(d, str(uuid4()))


@when('I use next page cursor')
def prepare_to_use_pagination(context):
    pagination_navigator.follow_next()


@then('Next page does not exist')
def next_page_missing(context):
    pagination_navigator.assert_no_next_page()


@when('After waiting for {duration} seconds')
def wait_time(context, duration):
    time.sleep(int(duration))


@when('Selecting one of the objects and saving as {item_id}')
def select_object_and_save(context, item_id):
    json = get_json(context)
    identifier = json.get('data').data[0]['id']
    identifier_registry.create_alias(item_id, identifier)
