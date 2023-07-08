import random
import string
from typing import List

EMPTY = ""
SPACE = " "
DOUBLE_SPACE = SPACE + SPACE
COMMA = ","
DOT = "."


class StringUtils:
    RANDOM_VAR = '#'

    @staticmethod
    def list_to_comma_str(arr: list) -> str:
        return COMMA.join(arr)

    @staticmethod
    def comma_separated_to_list(text: str) -> List[str]:
        return text.replace(SPACE, EMPTY).split(COMMA)

    @staticmethod
    def dot_separated_to_list(text: str) -> List[str]:
        return [x for x in f"{text}.".split(DOT)][:-1]

    @staticmethod
    def space_separated_to_list(text: str) -> List[str]:
        while DOUBLE_SPACE in text:
            text = text.replace(DOUBLE_SPACE, SPACE)
        return text.split(SPACE)

    @staticmethod
    def is_array(text):
        return text.startswith('[') and text.endswith(']')

    @staticmethod
    def extract_array(text):
        if StringUtils.is_array(text):
            return text[1:-1]
        return text

    @staticmethod
    def is_variable(text):
        return text.startswith('$')

    @staticmethod
    def extract_variable(text):
        if StringUtils.is_variable(text):
            return text[1:]
        return text

    @staticmethod
    def is_literal_string(text: str):
        return text.startswith('`') and text.endswith('`')

    @staticmethod
    def extract_literal_string(text: str):
        if StringUtils.is_literal_string(text):
            return text[1:-1]
        return text

    @staticmethod
    def get_random_string(length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    @staticmethod
    def is_empty(text):
        return text is None or text == ""

    @staticmethod
    def try_convert_num(text):
        if StringUtils.is_literal_string(text):
            # user indicated that value must be a string despite being composed of numbers only
            return StringUtils.extract_literal_string(text)
        try:
            return int(text)
        except Exception:
            try:
                return float(text)
            except Exception:
                return text
