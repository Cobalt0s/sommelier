from behave import then, when, given

from features import event_manager

from sommelier.utils.string_manipulations import StringUtils


@then('Event on topic {topic_name} is expected to be emitted')
def event_production_is_expected(context, topic_name):
    event_manager.save_expected_event(topic_name, is_expected=True)


@then('Event on topic {topic_name} is expected to be emitted, alias as {alias_name}')
def event_production_is_expected_with_alias(context, topic_name, alias_name):
    event_manager.save_expected_event(topic_name, is_expected=True, name=alias_name)


@then('Event {topic_type} on topic {topic_name} is expected to be emitted for author {author_id}')
def event_production_is_expected_with_payload(context, topic_type, topic_name, author_id):
    event_manager.save_expected_event_with_payload(topic_name, topic_type, author_id, is_expected=True)


@then('Event on topic {topic_name} is not emitted')
def event_production_is_not_expected(context, topic_name):
    event_manager.save_expected_event(topic_name, is_expected=False)


@then('Assert events arrived')
def event_production_is_expected(context):
    event_manager.validate_expected_events()


@then('Assert events arrived ignoring {ignored}')
def event_production_is_expected_with_timeout_ignoring(context, ignored):
    ignored_keys = StringUtils.comma_separated_to_list(ignored)
    event_manager.validate_expected_events(ignored_keys=ignored_keys)


@then('Assert events arrived with timeout {timeout}')
def event_production_is_expected_with_timeout(context, timeout):
    event_manager.validate_expected_events(drain_timeout=timeout)


@then('Assert events arrived while ignoring {ignored} with timeout {timeout}')
def event_production_is_expected_with_timeout_ignoring(context, ignored, timeout):
    ignored_keys = StringUtils.comma_separated_to_list(ignored)
    event_manager.validate_expected_events(drain_timeout=timeout, ignored_keys=ignored_keys)


@when('Sending event to {topic} topic')
def send_event(context, topic):
    event_manager.produce_event(topic)


@given('Topic {topic} is drained')
def drain_topic(context, topic):
    event_manager.drain_events(topic)


@then('Topic {topic} must be empty')
def topic_must_be_empty(context, topic):
    event_manager.must_be_empty(topic)


@when('Skip {num_events} events in topic {topic}')
def skip_events_in_topic(context, num_events, topic):
    event_manager.skip_events(topic, num_events)
