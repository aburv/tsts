"""
Methods returning system config
"""
import enum
import os


class Config:
    """
    Config class to set all envs
    """

    @staticmethod
    def get_db_parameters() -> dict:
        """
        :return:
        :rtype:
        """
        return {
            "db": os.environ.get("POSTGRES_DB"),
            "user": os.environ.get("POSTGRES_USER"),
            "pass": os.environ.get("POSTGRES_PASSWORD"),
            "host": os.environ.get("POSTGRES_HOST"),
            "port": os.environ.get("POSTGRES_PORT"),
            "meta_schema": os.environ.get("POSTGRES_SCHEMA_META"),
            "schema": os.environ.get("POSTGRES_SCHEMA")
        }

    @staticmethod
    def get_api_keys() -> list:
        """
        :return:
        :rtype:
        """
        return [
            os.environ.get("WEB_CLIENT_KEY"),
            os.environ.get("ANDROID_CLIENT_KEY"),
            os.environ.get("IOS_CLIENT_KEY"),
            os.environ.get("KEY")
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


class Relation(enum.Enum):
    """
    Relation defining the table
    """
    INIT = Table("", True)
    MIGRATION = Table("migration", False)
    AUDIT = Table("audit", False)
    AUDIT_FIELD = Table("audit_field", False)
    DEVICE = Table("device", True)
