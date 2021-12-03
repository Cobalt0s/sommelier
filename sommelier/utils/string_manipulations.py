
class StringUtils:

    @staticmethod
    def comma_separated_to_list(text):
        return text.replace(" ", "").split(",")

    @staticmethod
    def dot_separated_to_list(text):
        return [x for x in f"{text}.".split('.')][:-1]

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
