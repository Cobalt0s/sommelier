from sommelier.utils.identifier_resolver import resolve_id_or_tautology
from sommelier.utils.string_manipulations import StringUtils


def column_list(context):
    return table_as_2d_list(context, 0)


def table_as_dict(context):
    json = dict(table_as_2d_list(context))
    _expand_nested_keys(json)
    return json


def table_as_2d_list(context, position_of_value=1):
    list_2d = _table_to_2d_list(get_table(context))

    result = []
    for item in list_2d:
        value = item[position_of_value]
        if StringUtils.is_array(value):
            value_result = []
            arr = StringUtils.extract_array(value)
            for x in StringUtils.comma_separated_to_list(arr):
                if x:
                    value_result.append(parse_json_value(context, x))
        else:
            value_result = parse_json_value(context, value)

        key = item[0]
        if position_of_value == 1:
            result.append([key, value_result])
        else:
            result.append(value_result)
    return result


def parse_json_value(context, value):
    if value == "True" or value == "true":
        return True
    if value == "False" or value == "false":
        return False
    if value == "None" or value.lower() == "null":
        return None
    if value == "{}":
        return {}
    return resolve_id_or_tautology(context, value)


def get_table(context):
    if "payload" in context and context.payload is not None:
        table = []
        for k in context.payload:
            v = context.payload[k]
            if isinstance(v, dict):
                raise Exception("nested dictionaries for context.payload is not supported")
            table.append([k, v])
        # Clear the payload variable as it is temporary passed for side effects
        context.payload = None
        return CustomTable(table)
    return context.table


class CustomTable:

    def __init__(self, rows):
        self.rows = rows


def _table_to_2d_list(table):
    if isinstance(table, CustomTable):
        return table.rows

    if table is None:
        return []
    result = [table.headings]
    for row in table:
        result.append(row.cells)
    return result


def _expand_nested_keys(json):
    # To represent json in flattened form use `.` for specifying nested fields
    # * Given json:
    #
    # {name: Bob, education: {level: bachelor, grade: good}}
    #
    # * Flattened form:
    #
    # name: Bob
    # education.level: bachelor
    # eduction.grade: good

    nested_keys = []
    for k in json:
        if '.' in k:
            nested_keys.append(k)

    for k in nested_keys:
        value = json[k]
        current_obj = json
        # Zoom into the key which will create new objects or reuse existing
        key_list = k.split('.')
        for i in range(len(key_list)):
            subkey = key_list[i]
            if subkey in current_obj:
                # reuse existing object and keep zooming
                current_obj = current_obj[subkey]
            else:
                if i == len(key_list) - 1:
                    # we reached the end and need to save value
                    current_obj[subkey] = value
                else:
                    # we are still zooming
                    current_obj[subkey] = {}
                current_obj = current_obj[subkey]

        # nobody needs fully qualified key at the end of this procedure
        del json[k]
