import os
import unittest
from unittest import mock

from src.config import Config, Table, Relation
from src.responses import DataValidationException


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
    def test_should_return_db_creds_on_get_mongo_parameters(self):
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
        "REDIS_PASSWORD": 'pass',
        "REDIS_HOST": 'host',
        "REDIS_PORT": 'port',
    }, clear=True)
    def test_should_return_redis_db_creds_on_get_caching_parameters(self):
        expected = {
            'host': 'host',
            'pass': 'pass',
            'port': 'port',
        }
        actual = Config.get_caching_parameters()
        self.assertEqual(expected, actual)

    @mock.patch.dict(os.environ, {
        "BROKER_HOST": 'host',
        "BROKER_PORT": 'port',
    }, clear=True)
    def test_should_return_broker_server_connection_string_on_get_broker_connection_string(self):
        expected = "host:port"
        actual = Config.get_broker_connection_string()
        self.assertEqual(expected, actual)

    @mock.patch.dict(os.environ, {
        "AUTH_HOST": "host",
        "AUTH_PORT": "port"}, clear=True)
    def test_should_return_auth_connection_string(self):
        actual = Config.get_auth_connection_string()
        self.assertEqual("host:port", actual)

    @mock.patch.dict(os.environ, {
        "SEPARATOR": "separator_str"}, clear=True)
    def test_should_return_separator_string(self):
        actual = Config.get_separator()
        self.assertEqual("separator_str", actual)

    @mock.patch.object(Config, "get_separator", return_value="separator_str")
    def test_should_return_tokens_on_get_tokens(self, mock_get_separator):
        actual = Config.get_tokens("token1separator_strtoken2")

        mock_get_separator.assert_called_once_with()
        self.assertEqual(('token1', 'token2'), actual)

    @mock.patch.object(DataValidationException, "__init__", return_value=None)
    @mock.patch.object(Config, "get_separator", return_value="separator_str")
    def test_should_raise_data_validation_exception_when_no_separator_on_get_tokens(self,
                                                                                    mock_get_separator,
                                                                                    mock_exception):
        with self.assertRaises(DataValidationException):
            actual = Config.get_tokens("token1token2")

        mock_exception.assert_called_once_with('Invalid Tokens ', 'token1token2 list index out of range')
        mock_get_separator.assert_called_once_with()

    @mock.patch.dict(os.environ, {
        "WEB_CLIENT_KEY": "test_web_key",
        "ANDROID_CLIENT_KEY": "test_android_key",
        "IOS_CLIENT_KEY": "test_ios_key",
        "KEY": "test_dev_key"}, clear=True)
    def test_should_get_api_key(self):
        actual = Config.get_api_keys()
        self.assertEqual(["test_web_key", "test_android_key", "test_ios_key", "test_dev_key"], actual)


class TableTest(unittest.TestCase):
    def test_should_return_table_name_on_get_name(self):
        expected = "tableName"
        table = Table(expected, False)
        actual = table.get_name()
        self.assertEqual(expected, actual)
        self.assertEqual(False, table.schema_type)


class RelationTest(unittest.TestCase):
    def test_should_check_relation_enum_objects(self):
        self.assertTrue(isinstance(Relation.INIT, Relation))
        self.assertEqual(Relation.INIT.value.get_name(), '')
        self.assertTrue(isinstance(Relation.MIGRATION, Relation))
        self.assertEqual(Relation.MIGRATION.value.get_name(), 'migration')
        self.assertTrue(isinstance(Relation.AUDIT, Relation))
        self.assertEqual(Relation.AUDIT.value.get_name(), 'audit')
        self.assertTrue(isinstance(Relation.AUDIT_FIELD, Relation))
        self.assertEqual(Relation.AUDIT_FIELD.value.get_name(), 'audit_field')
        self.assertTrue(isinstance(Relation.DEVICE, Relation))
        self.assertEqual(Relation.DEVICE.value.get_name(), 'device')
        self.assertTrue(isinstance(Relation.IMAGE, Relation))
        self.assertEqual(Relation.IMAGE.value.get_name(), 't_image')
        self.assertTrue(isinstance(Relation.LOCATION, Relation))
        self.assertEqual(Relation.LOCATION.value.get_name(), 't_location')
        self.assertTrue(isinstance(Relation.USER, Relation))
        self.assertEqual(Relation.USER.value.get_name(), 't_user')
        self.assertTrue(isinstance(Relation.UID, Relation))
        self.assertEqual(Relation.UID.value.get_name(), 'user_identifier')
        self.assertTrue(isinstance(Relation.ROLE, Relation))
        self.assertEqual(Relation.ROLE.value.get_name(), 't_role')
