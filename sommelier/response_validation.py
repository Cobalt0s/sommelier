from sommelier.utils.assertions import (
    assert_json_properties_in_object,
    assert_json_properties_in_list,
    assert_json_properties_not_in_list,
)

STATUS_CODES = {
    'OK': 200,
    'CREATED': 201,
    'NO CONTENT': 204,
    'BAD REQUEST': 400,
    'UNAUTHORIZED': 401,
    'FORBIDDEN': 403,
    'NOT FOUND': 404,
    'CONFLICT': 409,
    'SERVER ERROR': 500,
    'NOT IMPLEMENTED': 501,
}


class ResponseListChecker(object):

    def __init__(self, context_manager, identifier_registry, nested_key):
        self.context_manager = context_manager
        self.identifier_registry = identifier_registry
        self.nested_key = nested_key

    def contains(self, k, v):
        self.context_manager.context_contains(self.nested_key, k, v)

    def missing(self, k, v):
        self.context_manager.context_missing(self.nested_key, k, v)

    def contains_id(self, identifier):
        self.contains('id', self.identifier_registry.resolve_alias(identifier))

    def missing_id(self, identifier):
        self.missing('id', self.identifier_registry.resolve_alias(identifier))


class ResponseValidator(object):

    IN_OBJECT = 1
    IN_LIST = 2
    NOT_IN_LIST = 3

    def __init__(self, identifier_registry):
        self.context_manager = None
        self.identifier_registry = identifier_registry
        self.assertion_methods = {
            self.IN_OBJECT: assert_json_properties_in_object,
            self.IN_LIST: assert_json_properties_in_list,
            self.NOT_IN_LIST: assert_json_properties_not_in_list,
        }

    def set_ctx_manager(self, context_manager):
        self.context_manager = context_manager

    def get_list(self, key):
        return ResponseListChecker(self.context_manager, self.identifier_registry, key)

    def assert_status(self, status):
        self.context_manager.judge().assumption(status.upper() in STATUS_CODES, f'status code {status.upper()} is not supported')
        status_code = STATUS_CODES[status.upper()]
        self.context_manager.judge().expectation(
            status_code == self.context_manager.status_code(),
            f"Expected {status_code} given {self.context_manager.status_code()}"
        )

    def check_failure(self, code, details=None):
        json = self.context_manager.get_json()
        failure_code = json.get('error.code').raw_str()
        failure_details = json.get('error.details')
        if details is None:
            # We have a dictionary of values to see in details
            assert code == failure_code, f"Expected error of failure '{code}' actual '{failure_code}'"
            expected_details = self.context_manager.get_table_dict()
            for key in expected_details:
                x = expected_details[key]
                y = failure_details.get(key)
                self.context_manager.judge().expectation(
                    x == y.data,  ### TODO do not use .data, use getter
                    f"Expected `{x}` actual `{y}` for error.details.{key}"
                )
        else:
            # We have a single value in detail
            self.context_manager.judge().expectation(
                code == failure_code,
                f"Expected error code '{code}' actual '{failure_code}'",
            )
            self.context_manager.judge().expectation(
                details == failure_details,
                f"Expected `{details}` actual `{failure_details}` for error.details"
            )

    def missing_keys(self):
        json = self.context_manager.get_json()
        failure_code = json.get('error.code').raw_str()
        failure_details = json.get('error.details').raw_array()

        code = 'missing-required-values'
        assert code == failure_code, f"Expected error of failure {code} actual '{failure_code}'"
        missing_values = self.context_manager.column_list()

        failure_details.sort()
        missing_values.sort()

        assert missing_values == failure_details, f"Expected {missing_values} actual {failure_details} in error details"

    def contains_data(self, item_key=None, assertion_type=None):
        if item_key is None:
            self.context_manager.assert_json_properties_in_object()
        else:
            if assertion_type is None:
                raise Exception(f'Specify an assertion method for {item_key}, ex: list/object')
            self._apply_assert(item_key, self.assertion_methods[assertion_type])

    def contains_keys(self):
        expected_keys = self.context_manager.column_list()
        j = self.context_manager.get_json()
        missing_keys = []
        for k in expected_keys:
            if not j.has(k):
                missing_keys.append(k)
        self.context_manager.judge().assumption(
            len(missing_keys) == 0,
            f"Response doesn't include keys: {missing_keys}"
        )

    def _apply_assert(self, item_key, assertion_func):
        """
        Apply assert function on the nested object located under the key.
        Example:
            given response data of {'x': [1, 2, 3], 'y': {'name':'letter'}}
            you can apply assertion on list or object via assertion_func
            located under item_key which is x or y in our case
        """
        assertion_func(self.context_manager, self.context_manager.get_json().get(item_key))

    def count_data(self, zoom, amount):
        amount = int(amount)

        json = self.context_manager.get_json()
        elements = json.get(zoom).raw_array()
        size = len(elements)
        self.context_manager.judge().expectation(
            amount == size,
            f"Expected {amount} elements on page, given {size}"
        )
