def query_param_to_string(value):
    if isinstance(value, list):
        return ','.join(value)
    return str(value)


def query_params(pagination, params_dict=None):
    if params_dict is None:
        params_dict = {}
    result_dict = {}
    if len(pagination) != 0:
        # Feature scenario may explicitly override pagination query parameters later
        result_dict['pageNum'] = pagination

    result_dict.update(params_dict)

    if len(result_dict.keys()) != 0:
        result = '?'
        for key, value in result_dict.items():
            result += str(key) + '=' + query_param_to_string(value) + '&'
        return result
    return ''
