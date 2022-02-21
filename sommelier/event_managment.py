import copy

from sommelier.utils.json_helpers import JsonRetriever

from sommelier.logging import Judge, pretty

from sommelier.events import EventConsumer, EventProducer
from sommelier.utils import table_as_dict


def events_equal(context, expected_event, given_event, ignored_keys=None):
    a = JsonRetriever(context, copy.deepcopy(expected_event))
    b = JsonRetriever(context, copy.deepcopy(given_event))

    if ignored_keys is None:
        ignored_keys = []

    # ignore tracing information that may come with event
    # effectively we are making comparison of every other field
    ignored_keys.append('trace')

    for i in range(len(ignored_keys)):
        key = ignored_keys[i]
        a.delete(key)
        b.delete(key)

    a.sort()
    b.sort()

    return a.raw() == b.raw()


def validate_events_for_topic(context, event_registry, expected_events, topic, ignored_keys=None):
    given_events = event_registry[topic]
    for expected_event in expected_events:

        match = False
        index_to_remove = None
        for i, given_event in given_events.items():
            if events_equal(context, expected_event['payload'], given_event, ignored_keys):
                match = True
                index_to_remove = i
                save_event_attaching_test_name(context, given_event)
                break

        if index_to_remove is not None:
            del given_events[index_to_remove]

        is_expected = expected_event['is_expected']
        error_message = 'Expected' if is_expected else 'Not expected but present'
        context.requests_verb = "CONSUME"
        context.url = topic
        Judge(context).expectation(
            is_expected == match,
            f"{error_message} event '{pretty(context, expected_event['payload'])}'",
            given_events
        )


def save_event_attaching_test_name(context, expected_event):
    event_alias_name = expected_event['name']
    if event_alias_name is not None:
        context.named_events[event_alias_name] = expected_event['payload']


class EventManager:

    def __init__(self, host, wait_timeout):
        self.context = None
        self.event_consumer = EventConsumer(host)
        self.event_producer = EventProducer(host)
        self.wait_timeout = wait_timeout

    def set_context(self, context):
        self.context = context

    def reset(self):
        self.context.events = {}
        self.context.named_events = {}
        self.context.topics = {}

    def _save_expected_event(self, topic_name, is_expected, payload, name=None):
        arr = []
        if topic_name in self.context.events:
            arr = self.context.events[topic_name]
        else:
            self.context.events[topic_name] = arr
        arr.append({
            'is_expected': is_expected,
            'payload': payload,
            'name': name,
        })
        if topic_name in self.context.topics:
            self.context.topics[topic_name] += 1
        else:
            self.context.topics[topic_name] = 1

    def save_expected_event_with_payload(self, topic_name, topic_type, author_id, is_expected):
        self._save_expected_event(topic_name, is_expected, {
            'authorId': author_id,
            'type': topic_type,
            'payload': table_as_dict(self.context),
        })

    def save_expected_event(self, topic_name, is_expected, name=None):
        self._save_expected_event(topic_name, is_expected, table_as_dict(self.context), name)

    def _collect_events(self, drain_timeout=None):
        event_registry = {}
        for topic, num_messages in self.context.topics.items():
            event_registry[topic] = (self.event_consumer.consume(topic, num_messages, drain_timeout))
        return event_registry

    def validate_expected_events(self, drain_timeout=None, ignored_keys=None):
        event_registry = self._collect_events(drain_timeout)

        for topic, expected_events in self.context.events.items():
            validate_events_for_topic(self.context, event_registry, expected_events, topic, ignored_keys)
        self.context.events = {}

    def produce_event(self, topic):
        message = table_as_dict(self.context)
        self.event_producer.send_message(topic, message)

    def drain_events(self, topic):
        self.event_consumer.consume(topic, -1)

    def must_be_empty(self, topic):
        messages = self.event_consumer.consume(topic, -1, drain_timeout=1)
        empty = len(messages) == 0
        if not empty:
            self.drain_events(topic)

    def skip_events(self, topic, num_messages):
        num_messages = int(num_messages)
        events = self.event_consumer.consume(topic, num_messages, None)
        received_num_messages = len(events)
        Judge(self.context).expectation(
            received_num_messages == num_messages,
            f"Expected to skip {num_messages} while got {received_num_messages} events '{pretty(self.context, events)}'",
            api_enhancements=False
        )
