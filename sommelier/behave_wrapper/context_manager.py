from sommelier.utils import StringUtils


class ContextManager(object):

    def __init__(self, context):
        context.ctx_manager = self
        self.context = context
        self.context.master = {}
        self.master = self.context.master
        self.declare("__managers__")

    # attach some data to context, particular class can manage a subset of such values
    def set(self, key, value):
        zoom = StringUtils.dot_separated_to_list(key)
        data = self.master
        try:
            for i in range(len(zoom)-1):
                data = data[zoom[i]]
            data[zoom[-1]] = value
        except Exception:
            logger = self.of('DrunkLogger')
            logger.fatal(f"couldn't find {key} in ctx manager")

    def get(self, key):
        zoom = StringUtils.dot_separated_to_list(key)
        data = self.master
        try:
            for z in zoom:
                data = data[z]
            return data
        except Exception:
            logger = self.of('DrunkLogger')
            logger.fatal(f"couldn't find {key} in ctx manager")

    # sometimes values just should exist, doesn't override value if present
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

    # manager gets assigned to manage a subset of variables on context
    # it is good to store all managers as singletons to reach for their methods
    def attach_manager(self, manager):
        obj_name = manager.__class__.__name__
        if self.exists(f"__managers__.{obj_name}"):
            logger = self.of('DrunkLogger')
            logger.fatal(
                f'manager with name {obj_name} is already instantiated, manager instances can be only singletons')
        self.set(f"__managers__.{obj_name}", manager)

    # retrieve the bean of a manager
    def of(self, clazz):
        if isinstance(clazz, str):
            # allow arbitrary strings fo custom calls
            # this also "resolves" any circular dependencies in class imports, cheating in python style 🤷
            obj_name = clazz
        else:
            obj_name = clazz.__name__
        return self.get(f"__managers__.{obj_name}")
