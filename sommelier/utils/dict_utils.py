from typing import Optional


class DictUtils:

    @staticmethod
    def equals(first: Optional[dict], second: Optional[dict]):
        f_empty = first is None
        s_empty = second is None
        if f_empty and s_empty:
            # both empty, hence same
            return True
        if f_empty or s_empty:
            # one is empty while the other isn't
            return False
        if len(first) != len(second):
            # different number of keys, hence not the same
            return False
        DictUtils.sort_dict(first)
        DictUtils.sort_dict(second)
        return first == second

    @staticmethod
    def sort_dict(obj: dict):
        for k, v in obj.items():
            if isinstance(v, dict):
                DictUtils.sort_dict(v)
            if isinstance(v, list):
                v.sort()


class DefaultsUtils:

    @staticmethod
    def dict(value: Optional[dict]) -> dict:
        if value is None:
            return {}
        return value

    @staticmethod
    def list(value: Optional[list]) -> list:
        if value is None:
            return []
        return value

    @staticmethod
    def num(value: Optional[any], default_value: int = 0) -> int:
        if value is None:
            return default_value
        return int(value)

    @staticmethod
    def str(value: Optional[str], default_value: str = '') -> str:
        if value is None:
            return default_value
        return value
