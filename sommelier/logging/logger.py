import json


class Judge:

    def __init__(self, context_manager):
        self.context_manager = context_manager

    def expectation(self, condition, message, extra_details=None, api_enhancements=True):
        if condition:
            return

        if api_enhancements:
            log_info(f'Request {self.context_manager.get("requests_verb")} {self.context_manager.get("url")}')
            if extra_details is None:
                extra_details = "No JSON"
                if self.context_manager.response_result_has_json():
                    try:
                        extra_details = self.context_manager.get_json().raw()
                    except Exception:
                        pass

        self.context_manager.log_error(message, extra_details)

    def assumption(self, condition, message):
        if not condition:
            self.context_manager.log_fatal(message)
        assert True


def log_header(context_manager):
    behave_feature = context_manager.feature()
    if behave_feature is not None:
        print(f'[ 🌍 Scenario ] {behave_feature.name} >> {context_manager.scenario().name}')


def log_info(text):
    print(f'[ 🍷 Info     ] {text}')


def log_error(context_manager, text, extra_details=None):
    log_header(context_manager)
    print(f'[ 🍷 Error    ] {text}')
    if extra_details is not None:
        print(pretty(context_manager, extra_details))
    assert False, "step failed"


def log_fatal(context_manager, text):
    log_header(context_manager)
    print(f'[ 💥 Fatal    ] {text}')
    assert False, "error in the test itself"


def pretty(context_manager, data):
    wrapped = {
        "_": data,
    }
    __resolve_dict(context_manager, wrapped)
    data = wrapped['_']
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4)


def find_alias(context_manager, value):
    id_aliases = context_manager.get('id_aliases')
    for k in id_aliases:
        v = id_aliases[k]
        if v == value:
            return f'🍹{k} ({v})'
    return value


def __resolve_list(context_manager, arr):
    result = []
    for v in arr:
        if isinstance(v, dict):
            __resolve_dict(context_manager, v)
            result.append(v)
        else:
            result.append(find_alias(context_manager, v))
    return result


def __resolve_dict(context_manager, data):
    for k in data:
        v = data[k]
        if isinstance(v, dict):
            __resolve_dict(context_manager, v)
        elif isinstance(v, list):
            data[k] = __resolve_list(context_manager, v)
        else:
            data[k] = find_alias(context_manager, v)
