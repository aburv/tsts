import unittest

from src.services.local_consumer_service import LocalConsumerService
from src.services.local_event_store import events
from src.services.local_producer_service import LocalProducerService


class LocalEventServicesTest(unittest.TestCase):

    def setUp(self) -> None:
        events.clear()

    def test_should_share_events_and_return_latest_matching_message(self):
        producer = LocalProducerService()
        consumer = LocalConsumerService()

        producer.add_event("topic", "key", "first")
        producer.add_event("topic", "key", "latest")

        self.assertIs(producer.events, consumer.events)
        self.assertEqual(consumer.listen_event("topic", "key"), "latest")

    def test_should_keep_events_when_services_are_recreated(self):
        LocalProducerService().add_event("topic", "key", "content")

        recreated_consumer = LocalConsumerService()

        self.assertEqual(recreated_consumer.listen_event("topic", "key"), "content")

    def test_should_return_none_when_event_does_not_exist(self):
        self.assertIsNone(LocalConsumerService().listen_event("topic", "key"))