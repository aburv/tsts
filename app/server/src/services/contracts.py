"""Contracts implemented by local and cloud service adapters."""

from abc import ABC, abstractmethod


class AuthService(ABC):
    """Authentication operations used by the application."""

    @abstractmethod
    def login(self, user_id: str) -> tuple[str, str]:
        raise NotImplementedError

    @abstractmethod
    def validate_token(self, id_token: str, token: str, resource: str,
                       record_id: str, permission: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def refresh_token(self, id_token: str, access_token: str) -> tuple[str, str]:
        raise NotImplementedError


class ProducerService(ABC):
    """Message publishing operations used by the application."""

    @abstractmethod
    def add_event(self, topic: str, key: str, content: str) -> bool:
        raise NotImplementedError

class ConsumerService(ABC):
    """Message publishing operations used by the application."""

    @abstractmethod
    def listen_event(self, topic: str, key: str) -> str | None:
        raise NotImplementedError