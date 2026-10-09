"""In-memory message consumer for local development."""

from src.services.contracts import ConsumerService
from src.services.local_event_store import events


class LocalConsumerService(ConsumerService):
    """Records published events in memory instead of calling the broker."""

    def __init__(self) -> None:
        self.events = events

    def listen_event(self, topic: str, key: str) -> str | None:
        messages = self.events.get(topic, {}).get(key, [])
        return messages[-1] if messages else None