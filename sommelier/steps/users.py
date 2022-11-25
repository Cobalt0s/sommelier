from behave import given

from sommelier.managers import user_registry

#
#
# Out of the Box
#
#


@given('I am user {user_name}')
def select_user(context, user_name):
    user_registry.select_user(user_name)


@given('Grant user {user_name} role {role}')
def grant_role(context, user_name, role):
    role_num = '0'
    if role == 'admin':
        role_num = '1'
    user_registry.grant_user_role(user_name, role_num)
