from sommelier.behave_wrapper.aliases import LabelingMachine
from sommelier.utils import StringUtils

TABLE_SPECIAL_VALUES = {
    'TRUE': True,
    'FALSE': False,
    'NONE': None,
    'NULL': None,
    '{}': {},
}


def process_json_value(context_manager, value):
    value = value.upper()
    if value not in TABLE_SPECIAL_VALUES:
        if StringUtils.is_variable(value):
            alias = StringUtils.extract_variable(value)
            if alias == StringUtils.RANDOM_VAR:
                return StringUtils.get_random_string(10)
            # this alias is an abstraction of an actual value, need to resolve
            return context_manager.of(LabelingMachine).find(alias)
        # value is raw, acts as tautology, value comes in and goes out
        return value
    return TABLE_SPECIAL_VALUES[value]


def table_as_2d_list(context_manager, list_2d, position_of_value=1):
    result = []
    for item in list_2d:
        value = item[position_of_value]
        if StringUtils.is_array(value):
            value_result = []
            arr = StringUtils.extract_array(value)
            for x in StringUtils.comma_separated_to_list(arr):
                if x:
                    value_result.append(process_json_value(context_manager, x))
        else:
            value_result = process_json_value(context_manager, value)

        if position_of_value == 1:
            key = item[0]
            result.append([key, value_result])
        else:
            result.append(value_result)
    return result
