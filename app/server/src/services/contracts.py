"""
Contracts implemented by local and cloud service adapters.
"""

from abc import ABC, abstractmethod


class AuthService(ABC):
    """
    Authentication operations used by the application.
    """

    @abstractmethod
    def login(self, user_id: str) -> tuple[str, str]:
        """
        Login operations used by the application.
        """
        raise NotImplementedError

    @abstractmethod
    def validate_token(self, id_token: str, token: str, resource: str,
                       record_id: str, permission: str) -> str:
        """
        Validate the token is valid.
        """
        raise NotImplementedError

    @abstractmethod
    def refresh_token(self, id_token: str, access_token: str) -> tuple[str, str]:
        """
        Refresh the access token.
        """
        raise NotImplementedError


class ProducerService(ABC):
    """Message publishing operations used by the application."""

    @abstractmethod
    def add_event(self, topic: str, key: str, content: str) -> bool:
        """
        Add an event to the queue.
        """
        raise NotImplementedError

class ConsumerService(ABC):
    """Message publishing operations used by the application."""

    @abstractmethod
    def listen_event(self, topic: str, key: str) -> str | None:
        """
        Listen an event for the queue.
        """
        raise NotImplementedError
