from behave import given

from sommelier import identifier_registry


@given('I am user {user_name}')
def select_user(context, user_name):
    identifier_registry.select_user(user_name)


@given('Grant user {user_name} role {role}')
def grant_role(context, user_name, role):
    role_num = '0'
    if role == 'admin':
        role_num = '1'
    identifier_registry.grant_user_role(user_name, role_num)
