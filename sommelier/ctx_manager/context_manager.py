from sommelier.behave_wrapper.logging import DrunkLogger, Judge
from sommelier.utils import StringUtils


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

    def declare(self, key, value=None):
        if value is None:
            value = {}
        # if value already exists we do NOT touch it
        if key not in self.master:
            self.master[key] = value

    def exists(self, key):
        try:
            self.get(key)
            return True
        except Exception:
            return False

    def judge(self):
        return self.of(Judge)

    def log_error(self, text, extra_details=None):
        self.of(DrunkLogger).error(text, extra_details)

    def log_fatal(self, text):
        self.of(DrunkLogger).fatal(text)

    def attach_manager(self, manager):
        obj_name = manager.__class__.__name__
        if self.exists(f"__managers__.{obj_name}"):
            self.log_fatal(
                f'manager with name {obj_name} is already instantiated, manager instances can be only singletons')
        self.set(f"__managers__.{obj_name}", manager)

    def of(self, clazz):
        obj_name = clazz.__name__
        return self.get(f"__managers__.{obj_name}")
