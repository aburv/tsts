import os
import unittest
from unittest import mock

from src.config import Config


class ConfigTest(unittest.TestCase):

    @mock.patch.dict(os.environ, {
        "POSTGRES_DB": 'DB',
        "POSTGRES_USER": 'user',
        "POSTGRES_PASSWORD": 'pass',
        "POSTGRES_HOST": 'host',
        "POSTGRES_PORT": 'port'
    }, clear=True)
    def test_should_get_mongo_parameters(self):
        actual = Config.get_db_parameters()
        self.assertEqual({'db': 'DB', 'host': 'host', 'pass': 'pass', 'port': 'port', 'user': 'user'}, actual)

    @mock.patch.dict(os.environ, {"API_KEY": "test_api_key"}, clear=True)
    def test_should_get_api_key(self):
        actual = Config.get_api_key()
        self.assertEqual("test_api_key", actual)
