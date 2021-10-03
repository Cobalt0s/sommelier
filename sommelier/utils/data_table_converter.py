from core.utils.identifier_resolver import resolve_id_or_tautology


def column_list(context):
    return table_as_2d_list(context, 0)


def table_as_dict(context):
    json = dict(table_as_2d_list(context))
    _expand_nested_keys(json)
    return json


def table_as_2d_list(context, position_of_value=1):
    list_2d = _table_to_2d_list(context.table)

    result = []
    for item in list_2d:
        value = item[position_of_value]
        if value.startswith('[') and value.endswith(']'):
            value_result = []
            for x in value[1:-1].replace(', ', ',').split(','):
                if x:
                    value_result.append(resolve_id_or_tautology(context, x))
        else:
            value_result = resolve_id_or_tautology(context, value)

        key = item[0]
        if position_of_value == 1:
            result.append([key, value_result])
        else:
            result.append(value_result)
    return result


def _table_to_2d_list(table):
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
