
class DictUtils:

    @staticmethod
    def is_declared(obj, key):
        return key in obj

    @staticmethod
    def declare(obj, key, value):
        if not DictUtils.is_declared(obj, key):
            setattr(obj, key, value)
