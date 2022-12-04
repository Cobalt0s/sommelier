from sommelier.utils import StringUtils


ERROR_PREFIX = "[ 💥 ContextManager ]"


class ContextKeyError(Exception):

    def __init__(self, key) -> None:
        super().__init__(
            f"{ERROR_PREFIX} couldn't find {key}"
        )


class ImmutableManagerError(Exception):

    def __init__(self, name) -> None:
        super().__init__(
            f'{ERROR_PREFIX} manager instances can only be singletons, {name} is already instantiated'
        )


class ContextManager(object):

    def __init__(self, context):
        context.ctx_manager = self
        self.context = context
        self.context.master = {}
        self.master = self.context.master
        self.declare("__managers__", {})

    # attach some data to context, particular class can manage a subset of such values
    def set(self, key, value):
        zoom = StringUtils.dot_separated_to_list(key)
        data = self.master
        try:
            for i in range(len(zoom) - 1):
                data = data[zoom[i]]
            data[zoom[-1]] = value
        except Exception:
            raise ContextKeyError(key)

    def get(self, key, strict=True):
        zoom = StringUtils.dot_separated_to_list(key)
        data = self.master
        try:
            for z in zoom:
                data = data[z]
            return data
        except Exception:
            if strict:
                raise ContextKeyError(key)
            return None

    # sometimes values just should exist, doesn't override value if present
    def declare(self, key, value):
        # KEY is a zoom of a Nested Dictionary
        # if value already exists we do NOT touch it
        zoom = StringUtils.dot_separated_to_list(key)
        data = self.master

        for i in range(len(zoom) - 1):
            key = zoom[i]
            # automatically creates all the dictionaries as it walks
            if key not in data:
                data[key] = {}
            data = data[key]
        # finally we are at the last element which will hold the desired data
        last_key = zoom[-1]
        if last_key not in data:
            data[last_key] = value

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
            raise ImmutableManagerError(obj_name)
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
