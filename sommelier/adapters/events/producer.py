import json

from confluent_kafka import Producer


# Optional per-message delivery callback (triggered by poll() or flush())
# when a message has been successfully delivered or permanently
# failed delivery (after retries).
def delivery_callback(err, msg):
    if err:
        raise Exception('%% Message failed delivery: %s\n' % err)


class EventProducer:

    def __init__(self, host):
        # Create Producer instance
        self.producer = Producer(**{
            'bootstrap.servers': host
        })

    def send_message(self, topic, message):
        try:
            self.producer.produce(topic, key="key-from-test", value=json.dumps(message).encode('ascii'), callback=delivery_callback)

        except BufferError:
            raise Exception(
                '%% Local producer queue is full (%d messages awaiting delivery): try again\n' % len(self.producer)
            )

        # Serve delivery callback queue.
        # NOTE: Since produce() is an asynchronous API this poll() call
        #       will most likely not serve the delivery callback for the
        #       last produce()d message.
        self.producer.poll(0)
        # Wait until all messages have been delivered
        self.producer.flush()
