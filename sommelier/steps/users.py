from behave import given

from sommelier import identifier_registry


@given('I am user {user_name}')
def select_user(context, user_name):
    identifier_registry.select_user(user_name)
