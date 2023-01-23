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


@given('Grant user {user_name} roles {roles}')
def grant_role(context, user_name, roles):
    user_registry.grant_user_role(user_name, roles)


@given('Application of {app_name}')
def set_application_name(context, app_name):
    user_registry.select_application(app_name)
