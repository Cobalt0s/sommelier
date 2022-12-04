import re

from typing import Optional


class StringFormatter(object):

    def __init__(self, text: str, args: Optional[list]) -> None:
        super().__init__()
        self.text = text
        self.args = args
        r_format = r'%%(.*?)!'
        self.pattern = re.compile(r_format)

    def str(self, resolvers) -> str:
        # empty regex group means to use tautology
        resolvers[''] = lambda x: x

        func_names = re.findall(self.pattern, self.text)
        indexes = [x.span() for x in re.finditer(self.pattern, self.text)]
        # func names which are part of Regex Group are mapped to start & end indexes in text
        matches = list(zip(func_names, indexes))

        num_matches = len(matches)
        if num_matches != len(self.args):
            raise Exception(f"{self.text} doesn't match number of args {self.args}")

        letters = list(self.text)
        for m in range(num_matches - 1, -1, -1):
            # since we may add more characters by inserting new values in order to rely on the indexes we collected
            # we must start insertion from the end as it doesn't distort/shift characters in the left part and
            # the right hand side is considered a complete string
            func_name, index = matches[m]

            f = resolvers[func_name]
            if f is None:
                raise Exception(f"cannot resolve method specified in String Format [{self.text}] of %%{func_name}!")
            value = f(self.args[m])

            letters[index[0]:index[1]] = str(value)
        return "".join(letters)

    # TODO pretty print dictionary difference using
    #       * dictdiffer.diff(x, y)
    #       * special function that should compare 2 values
    #       * special function that should compare 1 against the best match in list
