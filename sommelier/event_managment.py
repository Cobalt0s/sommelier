import copy
from typing import Optional

from sommelier.behave_wrapper.logging.format_str import StringFormatter
from sommelier.behave_wrapper.tables import Carpenter
from sommelier.ctx_manager import FlowListener
from sommelier.events import EventConsumer, EventProducer
from sommelier.utils import JsonRetriever


def events_equal(context_manager, expected_event, given_event, ignored_keys):
    a = JsonRetriever(context_manager, copy.deepcopy(expected_event))
    b = JsonRetriever(context_manager, copy.deepcopy(given_event))

    for i in range(len(ignored_keys)):
        key = ignored_keys[i]
        a.delete(key)
        b.delete(key)

    return a.equals(b)


def validate_events_for_topic(context_manager, event_registry, expected_events, topic, ignored_keys=None):
    if ignored_keys is None:
        ignored_keys = []
    # ignore tracing information that may come with event
    # effectively we are making comparison of every other field
    ignored_keys.append('trace')

    given_events = event_registry[topic]
    for expected_event in expected_events:
        match = False
        index_to_remove = None
        for i, given_event in given_events.items():
            if events_equal(context_manager, expected_event['payload'], given_event, ignored_keys):
                match = True
                index_to_remove = i
                save_event_attaching_test_name(context_manager, expected_event['name'], given_event)
                break

        if index_to_remove is not None:
            del given_events[index_to_remove]

        is_expected = expected_event['is_expected']
        error_message = 'Expected' if is_expected else 'Not expected but present'
        context_manager.set('requests_verb', 'CONSUME')
        context_manager.set('url', topic)
        context_manager.judge().expectation(
            is_expected == match,
            StringFormatter('%%! event %%pretty!', [
                error_message,
                expected_event['payload']
            ]),
            cross_out_ignored_fields(context_manager, given_events, ignored_keys)
        )


def cross_out_ignored_fields(context_manager, events, ignored_keys):
    result = []
    for e in events.values():
        j = JsonRetriever(context_manager, copy.deepcopy(e))
        for key in ignored_keys:
            val = j.get(key)
            j.delete(key)
            j.set(f"__ignored__.{key}", val)
        result.append(j.raw())
    return result


def save_event_attaching_test_name(context_manager, event_alias_name, event):
    if event_alias_name is not None:
        context_manager.set(f'named_events.{event_alias_name}', event)


class EventManager(FlowListener):

    def __init__(self, host, wait_timeout):
        super().__init__(definitions=[
            ['events', {}],
            ['named_events', {}],
            ['topics', {}],
        ], managers={
            'carpenter': Carpenter,
        })
        self.carpenter: Optional[Carpenter] = None
        self.event_consumer = EventConsumer(host)
        self.event_producer = EventProducer(host)
        self.wait_timeout = wait_timeout

    def _save_expected_event(self, topic_name, is_expected, payload, name=None):
        arr = []
        if topic_name in self.ctx_m().get('events'):
            arr = self.ctx_m().get(f'events.{topic_name}')
        else:
            self.ctx_m().set(f'events.{topic_name}', arr)
        arr.append({
            'is_expected': is_expected,
            'payload': payload,
            'name': name,
        })
        if topic_name in self.ctx_m().get('topics'):
            topic_counter = self.ctx_m().get(f'topics.{topic_name}')
            self.ctx_m().set(f'topics.{topic_name}', topic_counter + 1)
        else:
            self.ctx_m().set(f'topics.{topic_name}', 1)

    def save_expected_event_with_payload(self, topic_name, topic_type, author_id, is_expected):
        self._save_expected_event(topic_name, is_expected, {
            'authorId': author_id,
            'type': topic_type,
            'payload': self.carpenter.builder().double().dict(),
        })

    def save_expected_event(self, topic_name, is_expected, name=None):
        self._save_expected_event(topic_name, is_expected, self.carpenter.builder().double().dict(), name)

    def _collect_events(self, drain_timeout=None):
        event_registry = {}
        for topic, num_messages in self.ctx_m().get('topics').items():
            event_registry[topic] = (self.event_consumer.consume(topic, num_messages, drain_timeout))
        return event_registry

    def validate_expected_events(self, drain_timeout=None, ignored_keys=None):
        event_registry = self._collect_events(drain_timeout)

        for topic, expected_events in self.ctx_m().get('events').items():
            validate_events_for_topic(self.ctx_m(), event_registry, expected_events, topic, ignored_keys)
        self.ctx_m().set('events', {})

    def produce_event(self, topic):
        message = self.carpenter.builder().double().dict()
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
        self.ctx_m().judge().expectation(
            received_num_messages == num_messages,
            StringFormatter(
                "Expected to skip %%! while got %%! events %%pretty!", [
                    num_messages,
                    received_num_messages,
                    events,
                ]),
            api_enhancements=False
        )
