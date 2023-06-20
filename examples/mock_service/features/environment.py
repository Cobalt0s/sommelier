from sommelier.behave_wrapper import global_test_flow_controller
from sommelier.steps.event_processing import topic_must_be_empty
from sommelier.steps.response_processing import wait_time


def before_all(context):
    global_test_flow_controller.before_all(context)


def before_scenario(context, scenario):
    global_test_flow_controller.before_scenario()


def after_scenario(context, scenario):
    global_test_flow_controller.after_scenario()


def after_all(context):
    global_test_flow_controller.after_all()
