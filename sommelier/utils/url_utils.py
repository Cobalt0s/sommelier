from typing import Tuple


def query_param_to_string(value):
    if isinstance(value, list):
        return ','.join(value)
    return str(value)


class UrlUtils(object):

    @staticmethod
    def make_query_params(params_dict=None, pagination=None) -> str:
        if params_dict is None:
            params_dict = {}
        result_dict = {}
        if pagination is not None and len(pagination) != 0:
            # Feature scenario may explicitly override pagination query parameters later
            result_dict['pageNum'] = pagination
        result_dict.update(params_dict)

        # convert dictionary (key/value pairs) into query params
        if len(result_dict.keys()) != 0:
            result = '?'
            for key, value in result_dict.items():
                result += str(key) + '=' + query_param_to_string(value) + '&'
            return result
        return ''

    @staticmethod
    def split_url_query_params(full_url) -> Tuple[str, dict]:
        if full_url is None or full_url == "":
            return "", {}
        url_parts = full_url.split('?')
        url = url_parts[0]
        query_params = {}
        if len(url_parts) == 2:
            qps = url_parts[1].split('&')
            for qp in qps:
                kv = qp.split('=')
                # TODO check for 2 exact values
                # TODO some QP may not have values, only keys
                query_params[kv[0]] = kv[1]
        return url, query_params



