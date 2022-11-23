import os

from sommelier import ApiClient, EventManager

SVC_HOST = os.getenv("SVC_HOST")

api = ApiClient(SVC_HOST)

KAFKA_HOST = os.getenv("KAFKA_HOST")

event_manager = EventManager(KAFKA_HOST, wait_timeout=10.0)
