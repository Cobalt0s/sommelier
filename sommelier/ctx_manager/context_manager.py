from sommelier.logging import Judge, log_error, log_fatal, log_info
from sommelier.utils import JsonRetriever, StringUtils


# TODO all managers should register, rely on the context wrapper
# behave provides context variable which we operate on
# ideally all possible context interactions should be listed in here
class ContextManager(object):

    def __init__(self, context):
        context.ctx_manager = self
        self.context = context
        self.context.master = {}
        self.master = self.context.master
        self.declare("__managers__")

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

    def exists(self, key):
        try:
            self.get(key)
            return True
        except Exception:
            return False

    def get_json(self):
        try:
            data = self.response_result().json()
            if data is None:
                raise KeyError
            if isinstance(data, dict):
                return JsonRetriever(self, data)
            self.log_error(f'json is not an object, got: {data}')
        except Exception:
            self.log_error(f'json is missing in response with status {self.status_code()}')

    def judge(self):
        return Judge(self)

    def status_code(self):
        return self.response_result().status_code

    def response_result(self):
        return self.get('result')

    def response_result_has_json(self):
        return hasattr(self.response_result(), 'json')

    def declare(self, key, value=None):
        if value is None:
            value = {}
        # if value already exists we do NOT touch it
        if key not in self.master:
            self.master[key] = value

    def log_info(self, text):
        log_info(text)

    def log_error(self, text, extra_details=None):
        log_error(self, text, extra_details)

    def log_fatal(self, text):
        log_fatal(self, text)

    def feature(self):
        return self.context.feature

    def scenario(self):
        return self.context.scenario

    def attach_manager(self, manager):
        obj_name = manager.__class__.__name__
        if self.exists(f"__managers__.{obj_name}"):
            self.log_fatal(
                f'manager with name {obj_name} is already instantiated, manager instances can be only singletons')
        self.set(f"__managers__.{obj_name}", manager)

    def of(self, clazz):
        # TODO fatal if doesn't exist
        obj_name = clazz.__name__
        return self.get(f"__managers__.{obj_name}")
