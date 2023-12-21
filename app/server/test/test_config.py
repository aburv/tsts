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
        "POSTGRES_PORT": 'port',
        "POSTGRES_SCHEMA_META": 'meta',
        "POSTGRES_SCHEMA": 'data'
    }, clear=True)
    def test_should_get_mongo_parameters(self):
        expected = {
            'db': 'DB',
            'host': 'host',
            'pass': 'pass',
            'port': 'port',
            'user': 'user',
            'meta_schema': 'meta',
            'schema': 'data',
        }
        actual = Config.get_db_parameters()
        self.assertEqual(expected, actual)

    @mock.patch.dict(os.environ, {
        "WEB_CLIENT_KEY": "test_web_key",
        "ANDROID_CLIENT_KEY": "test_android_key",
        "IOS_CLIENT_KEY": "test_ios_key",
        "DEV_KEY": "test_dev_key"}, clear=True)
    def test_should_get_api_key(self):
        actual = Config.get_api_keys()
        self.assertEqual(["test_web_key", "test_android_key", "test_ios_key", "test_dev_key"], actual)
