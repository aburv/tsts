"""In-memory message producer for local development."""

from src.services.contracts import ProducerService
from src.services.local_event_store import events


class LocalProducerService(ProducerService):
    """Records published events in memory instead of calling the broker."""

    def __init__(self) -> None:
        self.events = events

    def add_event(self, topic: str, key: str, content: str) -> bool:
        self.events.setdefault(topic, {}).setdefault(key, []).append(content)
        return True