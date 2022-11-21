from sommelier.logging import Judge, log_error, log_fatal
from sommelier.utils import get_json
from sommelier.utils.assertions import assert_json_properties_in_object
from sommelier.utils.data_table_converter import table_as_2d_list, expand_nested_keys
from sommelier.utils.list_lookup import context_contains, context_missing
from sommelier.utils.string_manipulations import StringUtils

# TODO all managers should register, rely on the context wrapper
# behave provides context variable which we operate on
# ideally all possible context interactions should be listed in here

class ContextManager(object):

    def __init__(self, context):
        context.ctx_manager = self
        self.context = context
        self.context.master = {}
        self.master = self.context.master
        # TODO must declare variables in a better way
        self.set('flag_use_permanent_id', False)

    def set(self, key, value):
        zoom = StringUtils.dot_separated_to_list(key)
        data = self.master
        try:
            for i in range(len(zoom)-1):
                data = data[zoom[i]]
            data[zoom[-1]] = value
        except Exception:
            self.log_fatal(f"couldn't find {key} in ctx manager")

    def get(self, key):
        zoom = StringUtils.dot_separated_to_list(key)
        data = self.master
        try:
            for z in zoom:
                data = data[z]
            return data
        except Exception:
            self.log_fatal(f"couldn't find {key} in ctx manager")

    def get_table_dict(self):
        payload = dict(table_as_2d_list(self))
        return expand_nested_keys(payload)

    def get_json(self):
        return get_json(self)

    def column_list(self):
        return table_as_2d_list(self, 0)

    def judge(self):
        return Judge(self)

    def status_code(self):
        return self.response_result().status_code

    def response_result(self):
        return self.get('result')

    def response_result_has_json(self):
        return hasattr(self.response_result(), 'json')

    def declare(self, key):
        # if value already exists we do NOT touch it
        if key not in self.master:
            self.master[key] = {}

    def context_contains(self, first_key, second_key, value):
        context_contains(self.context, first_key, second_key, value)

    def context_missing(self, first_key, second_key, value):
        context_missing(self.context, first_key, second_key, value)

    def assert_json_properties_in_object(self):
        json = self.get_json()
        assert_json_properties_in_object(self, json)

    def log_error(self, text, extra_details=None):
        log_error(self, text, extra_details)

    def log_fatal(self, text):
        log_fatal(self, text)

    def table(self):
        return self.context.table

    def feature(self):
        return self.context.feature

    def scenario(self):
        return self.context.scenario
