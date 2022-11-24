from typing import Optional

from sommelier.assertions import ResponseListChecker, AssertionMethodProvider, AssertionMethod
from sommelier.behave_wrapper import ResponseJsonHolder
from sommelier.behave_wrapper.tables import Carpenter
from sommelier.ctx_manager import FlowListener
from sommelier.utils import HttpStatusCodeUtils


class ResponseValidator(FlowListener):

    def __init__(self):
        super().__init__(managers={
            'carpenter': Carpenter,
            'response': ResponseJsonHolder,
        })
        self.carpenter: Optional[Carpenter] = None
        self.response: Optional[ResponseJsonHolder] = None

    def get_list(self, key):
        return ResponseListChecker(self.ctx_m(), key)

    def assert_status(self, status):
        status_code = HttpStatusCodeUtils.name_to_code(status)
        self.ctx_m().judge().assumption(status_code is not None,
                                        f'status code {status.upper()} is not supported')
        self.ctx_m().judge().expectation(
            status_code == self.response.status(),
            f"Expected {status_code} given {self.response.status()}"
        )

    def check_failure(self, code, details=None):
        json = self.response.body()
        failure_code = json.get('error.code').raw_str()
        failure_details = json.get('error.details')
        if details is None:
            # We have a dictionary of values to see in details
            assert code == failure_code, f"Expected error of failure '{code}' actual '{failure_code}'"
            expected_details = self.carpenter.builder().double().dict()
            for key in expected_details:
                x = expected_details[key]
                y = failure_details.get(key)
                self.ctx_m().judge().expectation(
                    x == y.raw(),
                    f"Expected `{x}` actual `{y}` for error.details.{key}"
                )
        else:
            # We have a single value in detail
            self.ctx_m().judge().expectation(
                code == failure_code,
                f"Expected error code '{code}' actual '{failure_code}'",
            )
            self.ctx_m().judge().expectation(
                details == failure_details,
                f"Expected `{details}` actual `{failure_details}` for error.details"
            )

    def missing_keys(self):
        json = self.response.body()
        failure_code = json.get('error.code').raw_str()
        failure_details = json.get('error.details').raw_array()

        code = 'missing-required-values'
        assert code == failure_code, f"Expected error of failure {code} actual '{failure_code}'"
        missing_values = self.carpenter.builder().singular().list()

        failure_details.sort()
        missing_values.sort()

        assert missing_values == failure_details, f"Expected {missing_values} actual {failure_details} in error details"

    def contains_data(self,
                      key: Optional[str] = None,
                      assertion_method: AssertionMethod = AssertionMethod.IN_OBJECT):
        self._apply_assert(key, AssertionMethodProvider.of(assertion_method))

    def contains_keys(self):
        expected_keys = self.carpenter.builder().singular().list()
        j = self.response.body()
        missing_keys = []
        for k in expected_keys:
            if not j.has(k):
                missing_keys.append(k)
        self.ctx_m().judge().assumption(
            len(missing_keys) == 0,
            f"Response doesn't include keys: {missing_keys}"
        )

    def _apply_assert(self, key, assertion_func):
        """
        Apply assert function on the nested object located under the key.
        Example:
            given response data of {'x': [1, 2, 3], 'y': {'name':'letter'}}
            you can apply assertion on list or object via assertion_func
            located under item_key which is x or y in our case
        """
        j = self.response.body()
        data = j.get(key)
        assertion_func(self.ctx_m(), data)

    def count_data(self, zoom, amount):
        amount = int(amount)

        json = self.response.body()
        elements = json.get(zoom).raw_array()
        size = len(elements)
        self.ctx_m().judge().expectation(
            amount == size,
            f"Expected {amount} elements on page, given {size}"
        )
