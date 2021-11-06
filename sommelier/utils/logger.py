import json


class Judge:

    def __init__(self, context):
        self.context = context

    def expectation(self, condition, message, extra_details=None):
        if condition:
            return
        log_info(self.context, f'Request {self.context.requests_verb} {self.context.url}')

        if extra_details is None:
            extra_details = "No JSON"
            if hasattr(self.context.result, 'json'):
                try:
                    extra_details = self.context.result.json()
                except Exception:
                    pass

        log_error(self.context, message, extra_details)

    def assumption(self, condition, message):
        if not condition:
            log_fatal(self.context, message)
        assert True


def log_header(context):
    if context.feature is not None:
        print(f'[ 🌍 Scenario ] {context.feature.name} >> {context.scenario.name}')


def log_info(context, text):
    print(f'[ 🍷 Info     ] {text}')


def log_error(context, text, extra_details=None):
    log_header(context)
    print(f'[ 🍷 Error    ] {text}')
    if extra_details is not None:
        print(pretty(extra_details))
    assert False, "step failed"


def log_fatal(context, text):
    log_header(context)
    print(f'[ 💥 Fatal    ] {text}')
    assert False, "error in the test itself"


def pretty(data):
    return json.dumps(data, sort_keys=True, indent=4)
