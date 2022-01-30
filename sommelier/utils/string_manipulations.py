EMPTY = ""
SPACE = " "
DOUBLE_SPACE = SPACE + SPACE
COMMA = ","
DOT = "."


class StringUtils:

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
