import random
import string

EMPTY = ""
SPACE = " "
DOUBLE_SPACE = SPACE + SPACE
COMMA = ","
DOT = "."


class StringUtils:

    RANDOM_VAR = '#'

    @staticmethod
    def comma_separated_to_list(text):
        return text.replace(SPACE, EMPTY).split(COMMA)

    @staticmethod
    def dot_separated_to_list(text):
        return [x for x in f"{text}.".split(DOT)][:-1]

    @staticmethod
    def space_separated_to_list(text):
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
    def get_random_string(length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    @staticmethod
    def is_empty(text):
        return text is None or text == ""

