from behave import then, when, given

from features import event_manager


@then('Event on topic {topic_name} is expected to be emitted')
def event_production_is_expected(context, topic_name):
    event_manager.save_expected_event(topic_name, is_expected=True)


@then('Event {topic_type} on topic {topic_name} is expected to be emitted for author {author_id}')
def event_production_is_expected_with_payload(context, topic_type, topic_name, author_id):
    event_manager.save_expected_event_with_payload(topic_name, topic_type, author_id, is_expected=True)


@then('Event on topic {topic_name} is not emitted')
def event_production_is_not_expected(context, topic_name):
    event_manager.save_expected_event(topic_name, is_expected=False)


@then('Assert events arrived')
def event_production_is_expected(context):
    event_manager.validate_expected_events()


@then('Assert events arrived with timeout {timeout}')
def event_production_is_expected_with_timeout(context, timeout):
    event_manager.validate_expected_events(timeout)


@when('Sending event to {topic} topic')
def send_event(context, topic):
    event_manager.produce_event(topic)


@given('Topic {topic} is drained')
def drain_topic(context, topic):
    event_manager.drain_events(topic)


@when('Skip {num_events} events in topic {topic}')
def skip_events_in_topic(context, num_events, topic):
    event_manager.skip_events(topic, num_events)
