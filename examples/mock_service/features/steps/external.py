from behave import when

from features import external_api


@when('Make external call')
def make_external_call(context):
    external_api.post('/callback', [])
