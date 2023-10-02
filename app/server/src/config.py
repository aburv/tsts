"""
Methods returning system config
"""
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
            "port": os.environ.get("POSTGRES_PORT")
        }

    @staticmethod
    def get_api_key() -> str:
        """
        :return:
        :rtype:
        """
        return os.environ.get("API_KEY")
