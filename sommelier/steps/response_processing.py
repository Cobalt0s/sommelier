import time
from uuid import uuid4

from behave import given, then, when

from sommelier.behave_wrapper import response_json_holder, labeling_machine
from sommelier.managers import response_validator, AssertionMethod
from sommelier.utils import StringUtils


#
#
# Out of the Box
#
#


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
    response_validator.contains_data(item_key, AssertionMethod.IN_OBJECT)


@then('Contains properties inside list named {item_key}')
def contains_properties(context, item_key):
    response_validator.contains_data(item_key, AssertionMethod.IN_LIST)


@then('Does not contain properties inside list {item_key}')
def contains_properties(context, item_key):
    response_validator.contains_data(item_key, AssertionMethod.NOT_IN_LIST)


@then('Number of {zoom} on page is {amount}')
def count_elements_on_page(context, zoom, amount):
    response_validator.count_data(zoom, amount)


@when('Save id as {item_id}')
def save_item_id(context, item_id):
    response_json_holder.save_value_as('id', item_id)


@when('Save id located in {key} as {item_id}')
def save_item_id_with_zoom(context, key, item_id):
    response_json_holder.save_value_as(key, item_id)


@given('Define uuid for list {definitions}')
def define_uuids(context, definitions):
    for d in StringUtils.comma_separated_to_list(definitions):
        labeling_machine.create_alias(d, str(uuid4()))


@when('After waiting for {duration} seconds')
def wait_time(context, duration):
    time.sleep(float(duration))


@when('After waiting for {duration} ms')
def wait_ms(context, duration):
    ms = float(duration)
    wait_time(context, ms * 0.001)


@when('Selecting one of the objects and saving as {item_id}')
def select_object_and_save(context, item_id):
    json = response_json_holder.body()
    identifier = json.get('data.[0].id').raw_str()
    labeling_machine.create_alias(item_id, identifier)
