from behave import then, when

from sommelier.managers import pagination_navigator

#
#
# Out of the Box
#
#


@when('I use next page cursor')
def prepare_to_use_pagination(context):
    pagination_navigator.follow_next()


@when('I clear pagination parameters')
def clear_pagination(context):
    pagination_navigator.reset()


@then('Next page does not exist')
def next_page_missing(context):
    pagination_navigator.assert_no_next_page()
