from sommelier import response_validator, pagination_navigator
from sommelier.managers.rest_clients import identifier_registry
from features import api, event_manager


def before_all(context):
    api.set_context(context)
    response_validator.set_context(context)

    event_manager.set_context(context)
    pagination_navigator.set_context(context)
    identifier_registry.set_context(context)


def before_scenario(context, scenario):
    pagination_navigator.reset()
    identifier_registry.reset()
    event_manager.reset()
