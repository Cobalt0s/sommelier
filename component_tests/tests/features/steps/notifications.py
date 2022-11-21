from behave import when

from features import api


@when('I view subscriptions')
def get_subscriptions(context):
    api.get('/follows', [])


@when('I follow tag {tag_id}')
def follow_tag(context, tag_id):
    api.post('/follows/tags/{0}', [tag_id])


@when('I follow question {question_id}')
def follow_tag(context, question_id):
    api.post('/follows/questions/{0}', [question_id])


@when('I unfollow tag {tag_id}')
def unfollow_tag(context, tag_id):
    api.delete('/follows/tags/{0}', [tag_id])


@when('I unfollow question {question_id}')
def unfollow_tag(context, question_id):
    api.delete('/follows/questions/{0}', [question_id])
