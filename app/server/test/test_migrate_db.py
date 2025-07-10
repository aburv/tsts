import unittest
from unittest import mock
from unittest.mock import call, patch

from migrate_db import Migrate, get_version_from_name, get_ddl_files, MigrateData
from src.config import Relation, Config
from src.data import DataModel, OrderType
from src.db_duo import PostgresDbDuo
from src.logger import LoggerAPI
from src.responses import TableNotFoundException, DBExecutionException


class MigrateDataTest(unittest.TestCase):
    @mock.patch.object(DataModel, '__init__', return_value=None)
    def test_should_init_migrate_data(self, mock_data_model):
        MigrateData()

        mock_data_model.assert_called_once_with(Relation.MIGRATION, has_id=False, is_a_record=False)

    @mock.patch.object(DataModel, 'add_field', return_value=None)
    def test_should_add_fields_on_add_insert_fields(self, mock_add_field):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            migrate_data = MigrateData()

        migrate_data.add_insert_fields()

        mock_add_field.assert_has_calls([
            call('version', 'version', str, is_optional=False),
        ])

    @mock.patch.object(DataModel, 'add_field', return_value=None)
    def test_should_return_none_on_add_update_fields(self, mock_add_field):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            migrate_data = MigrateData()

        actual = migrate_data.add_fields()

        self.assertIsNone(actual)
        assert not mock_add_field.called

    def test_should_return_filter_fields_on_get_filtering_fields(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            migrate_data = MigrateData()

        actual = migrate_data.get_filtering_fields()

        self.assertEqual(['version'], actual)

    @mock.patch.object(OrderType, '__init__', return_value=None)
    def test_should_return_order_type_on_get_ordering_type(self, mock_order_type):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            migrate_data = MigrateData()

        actual = migrate_data.get_ordering_type()

        mock_order_type.assert_called_once_with('date_time', True)
        self.assertIsInstance(actual, OrderType)

    def test_should_return_one_on_get_record_count(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            migrate_data = MigrateData()

        actual = migrate_data.get_record_count()

        self.assertEqual(1, actual)

    @mock.patch.object(DataModel, 'set_data', return_value=None)
    def test_should_add_fields_on_data(self, mock_set_data):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            migrate_data = MigrateData()

        migrate_data.on_data({"version": "version"})

        mock_set_data.assert_called_once_with({"version": "version"}, True)


class MigrateTest(unittest.TestCase):

    @mock.patch('os.walk', return_value=[("", "", ['', ''])])
    def test_should_return_ddl_files_on_get_ddl_files(self, mock_os_walk):
        self.assertEqual(['', ''], get_ddl_files())

        mock_os_walk.assert_called_once_with("resources")

    def test_should_return_version_number_on_get_version_from_name(self):
        self.assertEqual("1.00", get_version_from_name("V1.00__desc"))

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(MigrateData, '__init__', return_value=None)
    @mock.patch.object(DataModel, '__init__', return_value=None)
    @mock.patch.object(Config, 'get_db_parameters')
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    def test_should_create_object_on_init(self,
                                          mock_db,
                                          mock_parameter,
                                          mock_model,
                                          mock_data,
                                          mock_log
                                          ):
        mock_parameter.return_value = {'meta_schema': 'meta_schema', 'schema': 'schema'}
        migrate = Migrate()

        mock_log.assert_called_once_with()
        self.assertIsInstance(migrate.logger, LoggerAPI)
        mock_parameter.assert_called_once_with()
        self.assertEqual(migrate.schema, 'schema')
        self.assertEqual(migrate.meta_schema, 'meta_schema')
        mock_data.assert_called_once_with()
        self.assertIsInstance(migrate._data, MigrateData)
        self.assertIsInstance(migrate.db, PostgresDbDuo)
        mock_model.assert_called_once_with(Relation.INIT)
        self.assertIsInstance(migrate.init, PostgresDbDuo)
        calls = mock_db.call_args_list
        self.assertIsInstance(calls[0][0][0], MigrateData)
        self.assertIsInstance(calls[1][0][0], DataModel)
        self.assertIsInstance(migrate, Migrate)

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(Migrate, 'get_version', return_value="-1.00")
    @mock.patch('migrate_db.get_ddl_files')
    def test_should_not_run_the_ddl_file_when_version_is_negative_1_00(self,
                                                                       mock_get_ddl_files,
                                                                       mock_get_version,
                                                                       mock_log,
                                                                       ):
        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.logger = mock_log

        migrate.run()

        mock_log.info_entry.assert_called_once_with('Migrating DB')
        mock_get_version.assert_called_once_with()
        assert not mock_get_ddl_files.called

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(Migrate, 'create_schema')
    @mock.patch.object(Migrate, 'update_version', return_value=True)
    @mock.patch.object(Migrate, 'get_version', return_value="0.00")
    @mock.patch('migrate_db.get_ddl_files', return_value=['V0.00'])
    @mock.patch('migrate_db.get_version_from_name', return_value="0.00")
    def test_should_run_the_ddl_files_on_init_with_create_schema(self,
                                                                 mock_get_version_from_name,
                                                                 mock_get_ddl_files,
                                                                 mock_get_version,
                                                                 mock_update_version,
                                                                 mock_create_schema,
                                                                 mock_db,
                                                                 mock_log,
                                                                 ):
        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.init = mock_db
            migrate.db = mock_db
            migrate.logger = mock_log
            migrate.schema = "schema"
            migrate.meta_schema = "meta_schema"

        migrate.run()

        mock_log.info_entry.assert_has_calls([call('Migrating DB')])
        mock_get_version.assert_called_once_with()
        mock_get_ddl_files.assert_called_once_with()
        mock_create_schema.assert_has_calls([call("meta_schema"), call("schema")])
        mock_get_version_from_name.assert_has_calls([call('V0.00')])
        mock_db.run_ddl_file.assert_has_calls([call('resources/V0.00')])
        mock_update_version.assert_has_calls([])

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(Migrate, 'update_version', return_value=True)
    @mock.patch.object(Migrate, 'get_version', return_value="1.10")
    @mock.patch('migrate_db.get_ddl_files', return_value=['V1.11'])
    @mock.patch('migrate_db.get_version_from_name', return_value="1.11")
    def test_should_run_the_ddl_files(self,
                                      mock_get_version_from_name,
                                      mock_get_ddl_files,
                                      mock_get_version,
                                      mock_update_version,
                                      mock_db,
                                      mock_log,
                                      ):
        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.init = mock_db
            migrate.logger = mock_log
            migrate.schema = "schema"
            migrate.meta_schema = "meta_schema"

        migrate.run()

        mock_log.info_entry.assert_has_calls([call('Migrating DB')])
        mock_get_version.assert_called_once_with()
        mock_get_ddl_files.assert_called_once_with()
        mock_get_version_from_name.assert_has_calls([call('V1.11')])
        mock_db.run_ddl_file.assert_has_calls([call('resources/V1.11')])
        mock_update_version.assert_has_calls([call("1.11")])

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(Migrate, 'update_version', return_value=True)
    @mock.patch.object(Migrate, 'get_version', return_value="1.10")
    @mock.patch('migrate_db.get_ddl_files', return_value=['V1.11', 'V1.22'])
    @mock.patch('migrate_db.get_version_from_name', return_value="1.09")
    def test_should_not_run_the_ddl_files_on_system_version_is_greater_than_file_version(self,
                                                                                         mock_get_version_from_name,
                                                                                         mock_get_ddl_files,
                                                                                         mock_get_version,
                                                                                         mock_update_version,
                                                                                         mock_db,
                                                                                         mock_log,
                                                                                         ):
        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.logger = mock_log
            migrate.init = mock_db
            migrate.schema = "schema"
            migrate.meta_schema = "meta_schema"

        migrate.run()

        mock_get_version.assert_called_once_with()
        mock_get_ddl_files.assert_called_once_with()
        mock_get_version_from_name.assert_has_calls([call('V1.11'), call('V1.22')])
        assert not mock_db.run_ddl_file.called
        assert not mock_update_version.called
        mock_log.info_entry.assert_has_calls([
            call('Migrating DB'),
            call('Executing DDL command file: resources/V1.11'),
            call('DDL command file already executed as fileV1.09 systemVersion 1.10'),
            call('Executing DDL command file: resources/V1.22'),
            call('DDL command file already executed as fileV1.09 systemVersion 1.10')
        ])

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(Migrate, 'update_version')
    @mock.patch.object(Migrate, 'get_version', return_value="1.10")
    @mock.patch('migrate_db.get_ddl_files', return_value=['V1.11', 'V1.22'])
    @mock.patch('migrate_db.get_version_from_name', return_value="1.11")
    def test_should_stop_run_the_ddl_files_when_exception_on_update_version(self,
                                                                            mock_get_version_from_name,
                                                                            mock_get_ddl_files,
                                                                            mock_get_version,
                                                                            mock_update_version,
                                                                            mock_db,
                                                                            mock_log,
                                                                            ):
        with mock.patch.object(DBExecutionException, '__init__', return_value=None) as _:
            mock_update_version.side_effect = DBExecutionException('op', 'msg')
        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.logger = mock_log
            migrate.init = mock_db
            migrate.schema = "schema"
            migrate.meta_schema = "meta_schema"

        migrate.run()

        mock_log.info_entry.assert_has_calls([call('Migrating DB')])
        mock_get_version.assert_called_once_with()
        mock_get_ddl_files.assert_called_once_with()
        mock_get_version_from_name.assert_has_calls([call('V1.11')])
        mock_db.run_ddl_file.assert_has_calls([call('resources/V1.11')])
        mock_update_version.assert_has_calls([call("1.11")])
        mock_log.error_entry.assert_has_calls([call('Migration stopped')])

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(Migrate, 'update_version', return_value=True)
    @mock.patch.object(Migrate, 'get_version', return_value="1.10")
    @mock.patch('migrate_db.get_ddl_files', return_value=['V1.11', 'V1.22'])
    @mock.patch('migrate_db.get_version_from_name', return_value="1.11")
    def test_should_stop_run_the_ddl_files_when_exception_on_run_ddl(self,
                                                                     mock_get_version_from_name,
                                                                     mock_get_ddl_files,
                                                                     mock_get_version,
                                                                     mock_update_version,
                                                                     mock_db,
                                                                     mock_log,
                                                                     ):
        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.init = mock_db
            migrate.logger = mock_log
            migrate.schema = "schema"
            migrate.meta_schema = "meta_schema"
            mock_db.run_ddl_file.side_effect = Exception("error")

        migrate.run()

        mock_log.info_entry.assert_has_calls([call('Migrating DB')])
        mock_get_version.assert_called_once_with()
        mock_get_ddl_files.assert_called_once_with()
        mock_get_version_from_name.assert_has_calls([call('V1.11')])
        mock_db.run_ddl_file.assert_has_calls([call('resources/V1.11')])
        assert not mock_update_version.called
        mock_log.error_entry.assert_has_calls([call('Migration stopped on error')])

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch('psycopg2.connect')
    def test_should_establish_db_connection_on_create_schema(self,
                                                             mock_connect,
                                                             mock_log,
                                                             ):
        mock_con = mock_connect.return_value
        mock_cur = mock_con.cursor.return_value

        with patch.object(Migrate, '__init__', return_value=None) as _:
            migrate = Migrate()
            migrate.logger = mock_log
            migrate.param = {
                "db": "test_db",
                "user": "test_user",
                "pass": "test_pass",
                "host": "test_host",
                "port": 123,
            }

        migrate.create_schema("schema")

        mock_connect.assert_called_once_with(
            host='test_host',
            port=123,
            database='test_db',
            user='test_user',
            password='test_pass',
        )

        mock_cur.execute.assert_called_with("CREATE SCHEMA IF NOT EXISTS schema")
        mock_log.info_entry.assert_called_with("Creating Schema: schema")

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch('psycopg2.connect')
    def test_should_log_error_when_exception_on_execute_on_create_schema(self, mock_connect,
                                                                         mock_log,
                                                                         ):
        mock_con = mock_connect.return_value
        mock_cur = mock_con.cursor.return_value
        mock_cur.execute.side_effect = Exception("error")

        with patch.object(Migrate, '__init__', return_value=None) as _:
            migrate = Migrate()
            migrate.logger = mock_log
            migrate.param = {
                "db": "test_db",
                "user": "test_user",
                "pass": "test_pass",
                "host": "test_host",
                "port": 123,
            }

        migrate.create_schema("schema")

        mock_log.info_entry.assert_called_once_with('Creating Schema: schema')
        mock_connect.assert_called_once_with(
            host='test_host',
            port=123,
            database='test_db',
            user='test_user',
            password='test_pass',
        )
        mock_cur.execute.assert_called_once_with('CREATE SCHEMA IF NOT EXISTS schema')
        mock_log.error_entry.assert_called_once_with('Create schema : schema error')

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch('psycopg2.connect', side_effect=Exception("error"))
    def test_should_log_error_on_exception_with_connection_on_create_schema(self, mock_connect,
                                                                            mock_log,
                                                                            ):
        mock_con = mock_connect.return_value
        mock_cur = mock_con.cursor.return_value

        with patch.object(Migrate, '__init__', return_value=None) as _:
            migrate = Migrate()
            migrate.logger = mock_log
            migrate.param = {
                "db": "test_db",
                "user": "test_user",
                "pass": "test_pass",
                "host": "test_host",
                "port": 123,
            }

        migrate.create_schema("schema")

        mock_connect.assert_called_once_with(
            host='test_host',
            port=123,
            database='test_db',
            user='test_user',
            password='test_pass',
        )
        assert not mock_cur.execute.called
        mock_log.error_entry.assert_called_once_with('Create schema : schema error')
        mock_log.info_entry.assert_called_once_with('Creating Schema: schema')

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    def test_should_return_system_version_on_get_version(self,
                                                         mock_db,
                                                         ):
        expected = "1.00"

        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.db = mock_db
            mock_db.get_records.return_value = [{"version": expected}]

        actual = migrate.get_version()

        mock_db.get_records.assert_called_once_with()

        self.assertEqual(expected, actual)

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    def test_should_return_0_00_on_empty_tuple_get_version_from_db(self,
                                                                   mock_db,
                                                                   ):
        expected = "0.00"

        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.db = mock_db
            mock_db.get_records.return_value = ()

        actual = migrate.get_version()

        mock_db.get_records.assert_called_once_with()

        self.assertEqual(expected, actual)

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    def test_should_return_0_00_on_table_not_found_exception_on_get_version(self,
                                                                            mock_db,
                                                                            ):
        expected = "0.00"

        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.db = mock_db
            with mock.patch.object(TableNotFoundException, '__init__', return_value=None):
                mock_db.get_records.side_effect = TableNotFoundException("")

        actual = migrate.get_version()

        mock_db.get_records.assert_called_once_with()
        self.assertEqual(expected, actual)

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    def test_should_return_negative_1_00_on_exception_on_get_version(self,
                                                                     mock_db,
                                                                     mock_exception
                                                                     ):
        expected = "-1.00"

        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.db = mock_db
            mock_db.get_records.side_effect = DBExecutionException('op', 'error')

        actual = migrate.get_version()

        mock_db.get_records.assert_called_once()
        mock_exception.assert_called_once_with('op', 'error')
        self.assertEqual(expected, actual)

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(MigrateData, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    def test_should_call_insert_on_update_version(self,
                                                  mock_db,
                                                  mock_data,
                                                  mock_log,
                                                  ):
        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.logger = mock_log
            migrate.db = mock_db
            migrate._data = mock_data

        migrate.update_version("version")

        mock_log.info_entry.assert_called_once_with('Updating migration version : version')
        mock_data.on_data.assert_called_once_with({'version': 'version'})
        mock_db.insert_record.assert_called_once()
        args, _ = mock_db.insert_record.call_args
        self.assertEqual(args[0], '')

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'insert_record', return_value=True)
    @mock.patch.object(MigrateData, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    def test_should_raise_exception_on_update_version(self,
                                                      mock_db,
                                                      mock_data,
                                                      mock_insert,
                                                      mock_log,
                                                      mock_exception
                                                      ):
        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.logger = mock_log
            mock_db.insert_record = mock_insert
            migrate._data = mock_data
            migrate.db = mock_db
            with mock.patch.object(TableNotFoundException, '__init__', return_value=None):
                mock_db.insert_record.side_effect = DBExecutionException('op', 'message')

        with self.assertRaises(DBExecutionException):
            migrate.update_version("version")

        mock_log.info_entry.assert_called_once_with('Updating migration version : version')
        mock_insert.assert_called_once()
        args, _ = mock_insert.call_args
        self.assertEqual(args[0], '')

        mock_exception.assert_has_calls([call('op', 'message'), call('Update to version', 'version')])
