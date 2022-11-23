from sommelier.assertions.list import ResponseListChecker
from sommelier.assertions.json import AssertionMethodProvider, AssertionMethod


def require_var(variable, name):
    if variable is None:
        raise Exception(f"var {name} is not set")
