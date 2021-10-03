from core.utils import get_json, table_as_dict
from core.utils.assertions import (
    assert_json_properties_in_object,
    assert_json_properties_in_list,
    assert_json_properties_not_in_list,
)
from core.utils.data_table_converter import column_list
from core.utils.json_zoomer import zoom_in_json
from core.utils.list_lookup import context_contains, context_missing

STATUS_CODES = {
    'OK': 200,
    'CREATED': 201,
    'NO CONTENT': 204,
    'BAD REQUEST': 400,
    'UNAUTHORIZED': 401,
    'NOT FOUND': 404,
    'CONFLICT': 409,
    'SERVER ERROR': 500,
    'NOT IMPLEMENTED': 501,
}


class ResponseListChecker(object):

    def __init__(self, context, identifier_registry, nested_key):
        self.context = context
        self.identifier_registry = identifier_registry
        self.nested_key = nested_key

    def contains(self, k, v):
        context_contains(self.context, self.nested_key, k, v)

    def missing(self, k, v):
        context_missing(self.context, self.nested_key, k, v)

    def contains_id(self, identifier):
        self.contains('id', self.identifier_registry.resolve_alias(identifier))

    def missing_id(self, identifier):
        self.missing('id', self.identifier_registry.resolve_alias(identifier))


class ResponseValidator(object):

    IN_OBJECT = 1
    IN_LIST = 2
    NOT_IN_LIST = 3

    def __init__(self, identifier_registry):
        self.context = None
        self.identifier_registry = identifier_registry
        self.assertion_methods = {
            self.IN_OBJECT: assert_json_properties_in_object,
            self.IN_LIST: assert_json_properties_in_list,
            self.NOT_IN_LIST: assert_json_properties_not_in_list,
        }

    def set_context(self, context):
        self.context = context

    def get_list(self, key):
        return ResponseListChecker(self.context, self.identifier_registry, key)

    def assert_status(self, status):
        status_code = STATUS_CODES[status.upper()]
        assert status_code is not None
        assert status_code == self.context.result.status_code, \
            f"Expected {status_code} given {self.context.result.status_code} {self._extract_error_for_debugging()}"

    def _extract_error_for_debugging(self):
        if self.context.result.status_code == STATUS_CODES['UNAUTHORIZED']:
            return 'Request is Unauthorized, need to login'
        if hasattr(self.context.result, 'json'):
            json = get_json(self.context)
            error_of_failure_present = 'error' in json
            error = f"[Failure: {json['error']}']" if error_of_failure_present else ''
            return error
        return ''

    def check_failure(self, code, details=None):
        error = get_json(self.context)['error']
        failure_code = error['code']
        failure_details = error['details']
        if details is None:
            # We have a dictionary of values to see in details
            assert code == failure_code, f"Expected error of failure '{code}' actual '{failure_code}'"
            expected_details = table_as_dict(self.context)
            for key in expected_details:
                x = expected_details[key]
                y = failure_details[key]
                assert x == y, f"Expected {x} actual {y} for {key} in error details"
        else:
            # We have a single value in detail
            assert code == failure_code, f"Expected error of failure '{code}' actual '{failure_code}'"
            assert details == failure_details, f"Expected {details} actual {failure_details} in error details"

    def missing_keys(self):
        error = get_json(self.context)['error']
        failure_code = error['code']
        failure_details = error['details']

        code = 'missing-required-values'
        assert code == failure_code, f"Expected error of failure {code} actual '{failure_code}'"
        missing_values = column_list(self.context)

        failure_details.sort()
        missing_values.sort()

        assert missing_values == failure_details, f"Expected {missing_values} actual {failure_details} in error details"

    def contains_data(self, item_key=None, assertion_type=None):
        if item_key is None:
            json = get_json(self.context)
            assert_json_properties_in_object(self.context, json)
        else:
            if assertion_type is None:
                raise Exception(f'Specify an assertion method for {item_key}, ex: list/object')
            self._apply_assert(item_key, self.assertion_methods[assertion_type])

    def _apply_assert(self, item_key, assertion_func):
        """
        Apply assert function on the nested object located under the key.
        Example:
            given response data of {'x': [1, 2, 3], 'y': {'name':'letter'}}
            you can apply assertion on list or object via assertion_func
            located under item_key which is x or y in our case
        """
        json = get_json(self.context)
        if item_key in json:
            assertion_func(self.context, json[item_key])
        else:
            raise Exception(f'Missing key "{item_key}" in response body {json}')

    def count_data(self, zoom, amount):
        amount = int(amount)
        elements = zoom_in_json(get_json(self.context), zoom)
        size = len(elements)
        assert amount == size, f"Expected {amount} elements on page, given {size}"
