import json
import logging
import time

from confluent_kafka import Consumer

DRAIN_TIMEOUT = 5
POLL_TIMEOUT = 10


class EventConsumer:

    def __init__(self, host):
        self.host_url = host
        # Consumer configuration
        # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
        # Create logger for consumer (logs will be emitted when poll() is called)
        self.logger = logging.getLogger('consumer')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
        self.logger.addHandler(handler)

    def consume(self, topic, num_messages, drain_timeout=None):
        # Create Consumer instance
        # Hint: try debug='fetch' to generate some log messages
        c = Consumer({
            'bootstrap.servers': self.host_url,
            'group.id': 'hello',
            'auto.offset.reset': 'earliest'
        }, logger=self.logger)

        # Subscribe to topics
        c.subscribe([topic])
        messages = drain_messages_from_kafka(c, num_messages, topic, drain_timeout)
        c.close()

        return messages


def drain_messages_from_kafka(c, num_messages, topic, drain_timeout=None):
    messages = {}
    i = 0
    drain_timeout = DRAIN_TIMEOUT if drain_timeout is None else drain_timeout
    # Drain num_messages of messages from the topic
    timeout = time.time() + drain_timeout
    while i != num_messages:
        message, rtype = get_message_from_kafka(c)
        if rtype == "message":
            messages[i] = message
            i += 1
        if time.time() > timeout:
            print("timeout occurred")
            break
        if rtype == "error":
            print("kafka consumer error has occurred")
            break
        if rtype == "finished":
            print("Finished reading kafka topic ", topic)
            break
    return messages


def get_message_from_kafka(c):
    msg = c.poll(POLL_TIMEOUT)
    if msg is None:
        return None, "finished"
    else:
        if msg.error():
            print(msg.error())
            return None, "error"
        else:
            # Proper message
            # sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
            #                  (msg.topic(), msg.partition(), msg.offset(),
            #                   str(msg.key())))

            decoded_value = msg.value().decode("utf-8")
            if msg.key() is None:
                return None, "heartbeat"

            value = json.loads(decoded_value)
            return value, "message"
