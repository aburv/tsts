import os
import unittest
from unittest import mock

from src.config import Config, Table, Relation


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
