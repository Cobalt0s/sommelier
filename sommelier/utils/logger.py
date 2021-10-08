

class Judge:

    def __init__(self, context):
        self.context = context

    def claim(self, condition, message):
        if not condition:
            log_error(self.context, message)

    def assumption(self, condition, message):
        if not condition:
            log_fatal(self.context, message)
        assert True


def log_error(context, text):
    print(f'🌍 {context.feature.name} >> {context.scenario.name}')
    print(f'[❌] ERROR 🍷 >> {text}')
    assert False, "step failed"


def log_fatal(context, text):
    print(f'🌍 {context.feature.name} >> {context.scenario.name}')
    print(f'[❌] FATAL 🍷 >> {text}')
    assert False, "error in the test itself"
