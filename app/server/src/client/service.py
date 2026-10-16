"""Storage and validation for short-lived client installation sessions."""
import base64
import hashlib
import json
import secrets
import time

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature

from src.caching import Caching


class ClientSessionService:
    """Issue opaque client tokens backed by Redis."""

    _prefix = "client-session:"
    _installation_prefix = "client-installation:"
    _challenge_prefix = "client-challenge:"
    _ttl_seconds = 3600
    _challenge_ttl_seconds = 300
    _request_ttl_seconds = 300

    @classmethod
    def _hash(cls, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @classmethod
    def create(cls, installation_id: str, public_key: str, platform: str) -> tuple[str, int]:
        """
        Create a new client session
        """
        token = secrets.token_urlsafe(32)
        expires_at = int(time.time()) + cls._ttl_seconds
        record = {
            "installation_id": installation_id,
            "public_key": public_key,
            "platform": platform,
            "expires_at": expires_at,
        }
        cache = Caching.CACHE
        cache.set(f"{cls._installation_prefix}{installation_id}", json.dumps(record),
                  timeout=cls._ttl_seconds)
        cache.set(f"{cls._prefix}{cls._hash(token)}", json.dumps(record),
                  timeout=cls._ttl_seconds)
        return token, expires_at

    @classmethod
    def create_challenge(cls, installation_id: str, public_key: str, platform: str) -> str:
        """
        Create a new client challenge
        """
        challenge = secrets.token_urlsafe(32)
        record = json.dumps({
            "installation_id": installation_id,
            "public_key": public_key,
            "platform": platform,
        })
        Caching.CACHE.set(
            f"{cls._challenge_prefix}{cls._hash(challenge)}",
            record,
            timeout=cls._challenge_ttl_seconds,
        )
        return challenge

    @classmethod
    def create_from_challenge(
            cls, installation_id: str, platform: str, challenge: str, signature: str
    ) -> tuple[str, int]:
        """
        Create a new client challenge
        """
        from src.responses import SecurityException # pylint: disable=import-outside-toplevel

        value = Caching.CACHE.get(f"{cls._challenge_prefix}{cls._hash(challenge)}")
        if value is None:
            raise SecurityException("Challenge", "Expired or invalid challenge")
        try:
            record = json.loads(value)
            if (record["installation_id"] != installation_id
                    or record["platform"] != platform):
                raise SecurityException("Challenge", "Invalid installation")
            public_key_bytes = base64.b64decode(record["public_key"], validate=True)
            try:
                public_key = serialization.load_der_public_key(public_key_bytes)
            except ValueError:
                public_key = ec.EllipticCurvePublicKey.from_encoded_point(
                    ec.SECP256R1(), public_key_bytes
                )
            if not isinstance(public_key, ec.EllipticCurvePublicKey):
                raise ValueError("Public key is not an EC key")
            public_key.verify(
                base64.b64decode(signature, validate=True),
                challenge.encode("utf-8"),
                ec.ECDSA(hashes.SHA256()),
            )
        except (InvalidSignature, ValueError, TypeError, KeyError, base64.binascii.Error):
            raise SecurityException("Signature", "Invalid client signature") from None
        Caching.CACHE.delete(f"{cls._challenge_prefix}{cls._hash(challenge)}")
        return cls.create(installation_id, record["public_key"], record["platform"])

    @classmethod
    def validate(cls, token: str) -> bool:
        """
        Validate a token
        """
        try:
            value = Caching.CACHE.get(f"{cls._prefix}{cls._hash(token)}")
            if value is None:
                return False
            record = json.loads(value)
            return int(record["expires_at"]) > int(time.time())
        except (TypeError, ValueError, KeyError, json.JSONDecodeError):
            return False

    @classmethod
    def authenticate_request(
            cls, token: str, installation_id: str, platform: str, timestamp: str,
            request_id: str, signature: str, method: str, path: str, body: bytes
    ) -> bool:
        """
        Authenticate a request
        """
        try:
            timestamp_value = int(timestamp)
            now = int(time.time())
            if abs(now - timestamp_value) > cls._request_ttl_seconds:
                return False
            value = Caching.CACHE.get(f"{cls._prefix}{cls._hash(token)}")
            if value is None:
                return False
            record = json.loads(value)
            if (record["installation_id"] != installation_id
                    or record["platform"] != platform
                    or int(record["expires_at"]) <= now):
                return False
            public_key_bytes = base64.b64decode(record["public_key"], validate=True)
            try:
                public_key = serialization.load_der_public_key(public_key_bytes)
            except ValueError:
                public_key = ec.EllipticCurvePublicKey.from_encoded_point(
                    ec.SECP256R1(), public_key_bytes
                )
            if not isinstance(public_key, ec.EllipticCurvePublicKey):
                return False
            canonical = "\n".join((
                method.upper(), path, timestamp, request_id,
                hashlib.sha256(body).hexdigest(), platform, installation_id,
            )).encode("utf-8")
            public_key.verify(
                base64.b64decode(signature, validate=True),
                canonical,
                ec.ECDSA(hashes.SHA256()),
            )
            replay_key = f"client-request:{cls._hash(request_id)}"
            if hasattr(Caching.CACHE, "add"):
                return bool(Caching.CACHE.add(replay_key, "1", timeout=cls._request_ttl_seconds))
            if Caching.CACHE.get(replay_key) is not None:
                return False
            Caching.CACHE.set(replay_key, "1", timeout=cls._request_ttl_seconds)
            return True
        except (InvalidSignature, ValueError, TypeError, KeyError,
                json.JSONDecodeError, base64.binascii.Error):
            return False
