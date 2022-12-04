class SimpleLogger(object):

    @staticmethod
    def info(text: str):
        print(f'[ 🍷 Info     ] {text}')

    @staticmethod
    def error(text: str, extra_details=None, context=None):
        SimpleLogger.__log_header(context)
        print(f'[ 🍷 Error    ] {text}')
        if extra_details is not None:
            print(extra_details)
        assert False, "step failed"

    @staticmethod
    def fatal(text: str, context=None):
        SimpleLogger.__log_header(context)
        print(f'[ 💥 Fatal    ] {text}')
        assert False, "error in the test itself"

    @staticmethod
    def __log_header(context):
        if context is None:
            return
        gherkin_feature = context.feature
        if gherkin_feature is not None:
            gherkin_scenario = context.scenario
            print(f'[ 🌍 Scenario ] {gherkin_feature.name} >> {gherkin_scenario.name}')
