from core.events import EventConsumer, EventProducer
from core.utils import table_as_dict


def events_equal(expected_event, given_event):
    return expected_event['payload'] == given_event


def validate_events_for_topic(event_registry, expected_events, topic):
    given_events = event_registry[topic]
    for expected_event in expected_events:

        match = False
        index_to_remove = None
        for i, given_event in given_events.items():
            if events_equal(expected_event, given_event):
                match = True
                index_to_remove = i
                break

        if index_to_remove is not None:
            del given_events[index_to_remove]

        is_expected = expected_event['is_expected']
        error_message = 'Expected' if is_expected else 'Not expected but present'
        assert is_expected == match, f"{error_message} event '{expected_event['payload']}'\nBut given{given_events}"


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
        self.context.topics = {}

    def _save_expected_event(self, topic_name, is_expected, payload):
        arr = []
        if topic_name in self.context.events:
            arr = self.context.events[topic_name]
        else:
            self.context.events[topic_name] = arr
        arr.append({
            'is_expected': is_expected,
            'payload': payload,
        })
        if is_expected:
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

    def save_expected_event(self, topic_name, is_expected):
        self._save_expected_event(topic_name, is_expected, table_as_dict(self.context))

    def _collect_events(self):
        event_registry = {}
        for topic, num_messages in self.context.topics.items():
            event_registry[topic] = (self.event_consumer.consume(topic, num_messages))
        return event_registry

    def validate_expected_events(self):
        event_registry = self._collect_events()
        
        for topic, expected_events in self.context.events.items():
            validate_events_for_topic(event_registry, expected_events, topic)
        self.context.events = {}

    def produce_event(self, topic):
        message = table_as_dict(self.context)
        self.event_producer.send_message(topic, message)
