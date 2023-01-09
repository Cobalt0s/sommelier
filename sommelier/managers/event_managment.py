import copy
from typing import Optional


from sommelier.adapters.events import EventConsumer, EventProducer
from sommelier.behave_wrapper import FlowListener
from sommelier.behave_wrapper.logging import StringFormatter, Judge
from sommelier.behave_wrapper.responses.response_holder import ResponseJsonHolder
from sommelier.behave_wrapper.tables import Carpenter
from sommelier.utils import JsonRetriever, require_var


class EventManager(FlowListener):

    def __init__(self, kafka_host, ignored_keys=None, show_ignored=True):
        super().__init__(definitions=[
            ['events', {}],
            ['named_events', {}],
            ['topics', {}],
        ], managers={
            'carpenter': Carpenter,
            'judge': Judge,
            'response_holder': ResponseJsonHolder,
        })
        self.carpenter: Optional[Carpenter] = None
        self.judge: Optional[Judge] = None
        self.response_holder: Optional[ResponseJsonHolder] = None
        require_var(kafka_host, "kafka_host")
        self.event_consumer = EventConsumer(kafka_host)
        self.event_producer = EventProducer(kafka_host)
        if ignored_keys is None:
            # ignore tracing information that may come with event
            ignored_keys = ['trace']
        self.ignored_keys = ignored_keys
        self.show_ignored = show_ignored

    ##########################################################
    # managing data that this class is responsible for
    def get_event(self, alias):
        return self.ctx_m().get(f'named_events.{alias}', strict=False)

    def save_event(self, alias, event):
        if alias is not None:
            self.ctx_m().set(f'named_events.{alias}', event)

    def pop_events(self):
        all_event_definitions = self.ctx_m().get('events').items()
        self.ctx_m().set('events', {})
        return all_event_definitions

    def topic_events(self, topic_name):
        self.ctx_m().declare(f'events.{topic_name}', [])
        return self.ctx_m().get(f'events.{topic_name}')

    def get_topic_event_num(self):
        return self.ctx_m().get('topics').items()

    def increment_topic_event_num(self, topic_name):
        self.ctx_m().declare(f'topics.{topic_name}', 0)
        old_value = self.ctx_m().get(f'topics.{topic_name}')
        new_value = old_value + 1
        self.ctx_m().set(f'topics.{topic_name}', new_value)

    ##########################################################
    # record Gherkin defined events to check later against events received from Kafka
    def _save_expected_event(self, topic_name, must_be_present, payload, alias=None):
        arr = self.topic_events(topic_name)
        arr.append({
            'must_be_present': must_be_present,
            'payload': payload,
            'alias': alias,
        })
        self.increment_topic_event_num(topic_name)

    def save_expected_event_with_payload(self, topic_name, topic_type, author_id, must_be_present):
        self._save_expected_event(topic_name, must_be_present, {
            'authorId': author_id,
            'type': topic_type,
            'payload': self.carpenter.builder().double().dict(),
        })

    def save_expected_event(self, topic_name, must_be_present, alias=None):
        self._save_expected_event(topic_name, must_be_present, self.carpenter.builder().double().dict(), alias)

    ##########################################################
    # sending messages to server via Kafka
    def produce_event(self, topic, key=None):
        message = self.carpenter.builder().double().dict()
        self.event_producer.send_message(topic, message, key=key)

    ##########################################################
    # skipping, draining events from Kafka topics
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
        self.judge.expectation(
            received_num_messages == num_messages,
            StringFormatter(
                "Expected to skip %%! while got %%! events %%pretty!", [
                    num_messages,
                    received_num_messages,
                    events,
                ]),
            api_enhancements=False
        )

    ##########################################################
    # trigger validation against defined expectations
    def validate_expected_events(self, drain_timeout=None, ignored_keys=None):
        # collect events from Kafka
        server_events = {}
        for topic, num_messages in self.get_topic_event_num():
            server_events[topic] = (self.event_consumer.consume(topic, num_messages, drain_timeout))
        # check with predefined expectations if results match
        for topic, expected_events in self.pop_events():
            self.validate_events_for_topic(topic, server_events[topic], expected_events, ignored_keys)
        # ensure there are no extra events that came from server, Tester must mention all
        no_events = True
        for topic, events in server_events.items():
            if bool(events):
                no_events = False
                break
        self.judge.expectation(
            no_events,
            StringFormatter('Not all events where mentioned in test %%pretty!', [
                server_events
            ])
        )

    def validate_events_for_topic(self, topic, given_events, expected_events, ignored_keys=None):
        # combine default ignored keys by this manager with provided ones
        if ignored_keys is None:
            ignored_keys = []
        ignored_keys.extend(self.ignored_keys)

        # effectively we are making comparison of every other field
        for expected_event in expected_events:
            # search for event among those provided by the server
            index_to_remove = None
            for i, given_event in given_events.items():
                if self.events_equal(expected_event['payload'], given_event, ignored_keys):
                    index_to_remove = i
                    break
            # if found, remove and add to named category if Tester wants to reference the payload later
            if index_to_remove is not None:
                self.save_event(expected_event['alias'], given_events[index_to_remove])
                del given_events[index_to_remove]
            # now check missing/present status in Kafka topic satisfies the expectation of Tester
            must_be_present = expected_event['must_be_present']
            found = index_to_remove is not None
            self.response_holder.with_description("Consume", topic)
            self.judge.expectation(
                must_be_present == found,
                StringFormatter('%%! event %%pretty!', [
                    'Expected' if must_be_present else 'Not expected but present',
                    expected_event['payload']
                ]),
                self.cross_out_ignored_fields(given_events, ignored_keys)
            )

    def cross_out_ignored_fields(self, events, ignored_keys):
        # by default we group, prefix all the ignored fields under united category
        # this makes it easier to see the actual data and parts we are interested for the test
        result = []
        for e in events.values():
            j = JsonRetriever(self.ctx_m(), copy.deepcopy(e))
            for key in ignored_keys:
                val = j.get(key)
                j.delete(key)
                if self.show_ignored:
                    j.set(f"__ignored__.{key}", val)
            result.append(j.raw())
        return result

    def events_equal(self, expected_event, given_event, ignored_keys):
        a = JsonRetriever(self.ctx_m(), copy.deepcopy(expected_event))
        b = JsonRetriever(self.ctx_m(), copy.deepcopy(given_event))

        for i in range(len(ignored_keys)):
            key = ignored_keys[i]
            a.delete(key)
            b.delete(key)

        return a.equals(b)

