"""Secret providers used by the server configuration."""
import json
import os
from abc import ABC, abstractmethod
from typing import TypeAlias


SecretValues: TypeAlias = dict[str, str]


class SecretProvider(ABC):
    """Interface for retrieving structured credentials from a secret store."""

    @abstractmethod
    def get_secret(self, secret_name: str) -> SecretValues:
        """Return the secret payload decoded as a JSON object."""


class EnvironmentSecretProvider(SecretProvider):
    """Environment variable implementation for local and simple deployments."""

    def get_secret(self, secret_name: str) -> SecretValues:
        value = os.getenv(secret_name)
        if value is None:
            raise ValueError(f"Environment variable '{secret_name}' is not set")
        return {secret_name: value}


def _decode_secret(payload: str | bytes, secret_name: str) -> SecretValues:
    try:
        secret = json.loads(payload)
    except (TypeError, json.JSONDecodeError) as error:
        raise ValueError(f"Secret '{secret_name}' must contain valid JSON") from error

    if not isinstance(secret, dict):
        raise ValueError(f"Secret '{secret_name}' must contain a JSON object")
    if any(not isinstance(key, str) or not isinstance(value, str)
           for key, value in secret.items()):
        raise ValueError(f"Secret '{secret_name}' must contain string keys and values")
    return secret


class SecretProviderFactory:
    """Build the configured provider without coupling callers to a cloud SDK."""

    @staticmethod
    def create() -> SecretProvider:
        provider = os.getenv("SECRET_PROVIDER", "").strip().lower()
        if provider == "env":
            return EnvironmentSecretProvider()
        raise ValueError("SECRET_PROVIDER must be set to 'env', 'aws', or 'gcp'")

class SecretStore:
    def __init__(self, provider: SecretProvider, secret_names: list[str]):
        self._secrets: SecretValues = {}
        for secret_name in secret_names:
            if not secret_name:
                continue
            secret = provider.get_secret(secret_name)
            self._secrets.update(secret)

    def get(self, secret_name: str) -> str:
        return self._secrets[secret_name]

    def contains(self, secret_name: str) -> bool:
        return secret_name in self._secrets