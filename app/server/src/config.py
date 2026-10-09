"""
Methods returning system config
"""
import enum
import os

from src.responses import DataValidationException
from src.secret_manager import SecretProvider, SecretProviderFactory, SecretStore


SECRET_KEYS = (
    "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST",
    "POSTGRES_PORT", "POSTGRES_SCHEMA_META", "POSTGRES_SCHEMA", "REDIS_USER",
    "REDIS_PASSWORD", "REDIS_HOST", "REDIS_PORT", "BROKER_HOST", "BROKER_PORT",
    "AUTH_HOST", "AUTH_PORT", "SEPARATOR", "WEB_CLIENT_KEY", "ANDROID_CLIENT_KEY",
    "IOS_CLIENT_KEY", "KEY",
)


class Config:
    """
    Config class to set all envs
    """

    _secret_store: SecretStore | None = None
    _secret_store_is_explicit = False

    @staticmethod
    def create_secret_provider() -> SecretProvider:
        """
        Create secret provider based on env
        """
        provider = SecretProviderFactory.create()
        return provider

    @classmethod
    def set_secret_store(cls, secret_store: SecretStore) -> None:
        cls._secret_store = secret_store
        cls._secret_store_is_explicit = True

    @classmethod
    def _get_configured_store(cls) -> SecretStore | None:
        secret_name = os.getenv("SECRET_NAME", "").strip()
        if not secret_name and not cls._secret_store_is_explicit:
            return None
        if cls._secret_store is None and secret_name:
            cls._secret_store = SecretStore(cls.create_secret_provider(), [secret_name])
        return cls._secret_store

    @classmethod
    def validate_secret_store(cls) -> None:
        if cls._secret_store is None:
            raise RuntimeError("Secret store has not been configured")
        missing = [key for key in SECRET_KEYS if not cls._secret_store.contains(key)]
        if missing:
            raise ValueError(f"Missing required secret keys: {', '.join(missing)}")

    @classmethod
    def _get_secret(cls, secret_name: str) -> str:
        secret_store = cls._get_configured_store()
        if secret_store is not None:
            return secret_store.get(secret_name)
        return os.environ[secret_name]

    @staticmethod
    def get_db_parameters() -> dict:
        """
        :return:
        :rtype:
        """
        return {
            "db": Config._get_secret("POSTGRES_DB"),
            "user": Config._get_secret("POSTGRES_USER"),
            "pass": Config._get_secret("POSTGRES_PASSWORD"),
            "host": Config._get_secret("POSTGRES_HOST"),
            "port": Config._get_secret("POSTGRES_PORT"),
            "meta_schema": Config._get_secret("POSTGRES_SCHEMA_META"),
            "schema": Config._get_secret("POSTGRES_SCHEMA")
        }

    @staticmethod
    def get_caching_parameters() -> dict:
        """
        :return:
        :rtype:
        """
        return {
            "user": Config._get_secret("REDIS_USER"),
            "pass": Config._get_secret("REDIS_PASSWORD"),
            "host": Config._get_secret("REDIS_HOST"),
            "port": Config._get_secret("REDIS_PORT"),
        }

    @staticmethod
    def get_broker_connection_string() -> str:
        """
        :return:
        :rtype:
        """
        return Config._get_secret("BROKER_HOST") + ":" + Config._get_secret("BROKER_PORT")

    @staticmethod
    def get_auth_connection_string() -> str:
        """
        :return:
        :rtype:
        """
        return Config._get_secret("AUTH_HOST") + ":" + Config._get_secret("AUTH_PORT")

    @staticmethod
    def get_separator() -> str:
        """
        :return:
        :rtype:
        """
        return Config._get_secret("SEPARATOR")

    @staticmethod
    def get_tokens(token: str) -> tuple[str, str]:
        """
        Get tokens from given token
        """
        try:
            tokens = token.split(Config.get_separator())
            return (tokens[0]), (tokens[1])
        except Exception as e:
            raise DataValidationException("Invalid Tokens ", f"{token} {e}") from e

    @staticmethod
    def get_api_keys() -> list:
        """
        :return:
        :rtype:
        """
        return [
            Config._get_secret("WEB_CLIENT_KEY"),
            Config._get_secret("ANDROID_CLIENT_KEY"),
            Config._get_secret("IOS_CLIENT_KEY"),
            Config._get_secret("KEY")
        ]


class Table:
    """
    Table
    """
    _name: str
    schemaType: bool

    def __init__(self, name: str, is_main: bool) -> None:
        self._name = name
        self.schema_type = is_main

    def get_name(self) -> str:
        """
        :return: table name
        :rtype: str
        """
        return self._name


class Join(Table):
    """
    Table join Table
    """

    def __init__(self, table1: Table, table2: Table, key1: str, key2: str) -> None:
        super().__init__("", True)
        self.table1 = table1
        self.table2 = table2
        self.key1 = key1
        self.key2 = key2

    def get_name(self) -> str:
        """
        :return: table name
        :rtype: str
        """
        return (f"{self.table1.get_name()} AS a "
                f"INNER JOIN "
                f"{self.table2.get_name()} AS b "
                f"ON "
                f"a.{self.key1} = b.{self.key2}")


class Relation(enum.Enum):
    """
    Relation defining the table
    """
    INIT = Table("", True)
    MIGRATION = Table("migration", False)
    AUDIT = Table("audit", False)
    AUDIT_FIELD = Table("audit_field", False)
    DEVICE = Table("device", True)
    IMAGE = Table("t_image", True)
    LOCATION = Table("t_location", True)
    USER = Table("t_user", True)
    UID = Table("user_identifier", True)
    ROLE = Table("t_role", True)
    LOGIN = Table("t_login", True)
    FORM_FIELD = Table("form_field", True)
    OPTION_DATA = Table("data_option", True)
    OPTION = Join(Table("form_field", True),
                  Table("data_option", True),
                  "id",
                  "field_id"
                  )
    PLAYER = Table("player", True)
    T_PLAYER = Table("player_gear", True)
    PLAYER_POSITION = Table("player_position", True)
