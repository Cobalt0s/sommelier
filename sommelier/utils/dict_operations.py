
class DictUtils:

    @staticmethod
    def equals(first, second):
        f_empty = first is None
        s_empty = second is None
        if f_empty and s_empty:
            return True
        if f_empty or s_empty:
            return False

    @staticmethod
    def sort_dict(obj):
        for k, v in obj.values():
            if isinstance(v, dict):
                DictUtils.sort_dict(v)
            if isinstance(v, list):
                v.sort()
