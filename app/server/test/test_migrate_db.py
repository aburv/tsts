import unittest
from unittest import mock
from unittest.mock import call, patch

from src.config import Relation
from src.db_duo import PostgresDbDuo, OrderType
from migrate_db import Migrate, get_version_from_name, get_ddl_files
from src.logger import LoggerAPI
from src.responses import TableNotFoundException, DBExecutionException


class MigrateTest(unittest.TestCase):

    @mock.patch('os.walk', return_value=[("", "", ['', ''])])
    def test_should_return_ddl_files_on_get_ddl_files(self, mock_os_walk):
        self.assertEqual(['', ''], get_ddl_files())

        mock_os_walk.assert_called_once_with("resources")

    def test_should_return_version_number_on_get_version_from_name(self):
        self.assertEqual("1.00", get_version_from_name("V1.00__desc"))

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    def test_should_create_object_on_init(self,
                                          mock_db,
                                          ):
        migrate = Migrate()

        mock_db.assert_has_calls([call(Relation.MIGRATION), call(Relation.INIT)])
        self.assertEqual(True, isinstance(migrate, Migrate))

    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(Migrate, 'get_version', return_value="-1.00")
    @mock.patch('migrate_db.get_ddl_files')
    def test_should_not_run_the_ddl_file_when_version_is_negative_1_00(self,
                                                                       mock_get_ddl_files,
                                                                       mock_get_version,
                                                                       mock_logger,
                                                                       mock_info
                                                                       ):
        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.logger = LoggerAPI()

        migrate.run()

        mock_info.assert_called_once_with('Migrating DB')
        mock_get_version.assert_called_once_with()
        assert not mock_get_ddl_files.called

    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
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
                                                                 mock_logger,
                                                                 mock_info
                                                                 ):
        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.init = mock_db
            migrate.db = mock_db
            migrate.logger = LoggerAPI()
            migrate.schema = "schema"
            migrate.meta_schema = "meta_schema"

        migrate.run()

        mock_info.assert_has_calls([call('Migrating DB')])
        mock_get_version.assert_called_once_with()
        mock_get_ddl_files.assert_called_once_with()
        mock_create_schema.assert_has_calls([call("meta_schema"), call("schema")])
        mock_get_version_from_name.assert_has_calls([call('V0.00')])
        mock_db.run_ddl_file.assert_has_calls([call('resources/V0.00')])
        mock_update_version.assert_has_calls([])

    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
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
                                      mock_logger,
                                      mock_info,
                                      ):
        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.init = mock_db
            migrate.logger = LoggerAPI()
            migrate.schema = "schema"
            migrate.meta_schema = "meta_schema"

        migrate.run()

        mock_info.assert_has_calls([call('Migrating DB')])
        mock_get_version.assert_called_once_with()
        mock_get_ddl_files.assert_called_once_with()
        mock_get_version_from_name.assert_has_calls([call('V1.11')])
        mock_db.run_ddl_file.assert_has_calls([call('resources/V1.11')])
        mock_update_version.assert_has_calls([call("1.11")])

    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
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
                                                                                         mock_logger,
                                                                                         mock_info
                                                                                         ):
        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.logger = LoggerAPI()
            migrate.init = mock_db
            migrate.schema = "schema"
            migrate.meta_schema = "meta_schema"

        migrate.run()

        mock_get_version.assert_called_once_with()
        mock_get_ddl_files.assert_called_once_with()
        mock_get_version_from_name.assert_has_calls([call('V1.11'), call('V1.22')])
        assert not mock_db.run_ddl_file.called
        assert not mock_update_version.called
        mock_info.assert_has_calls([
            call('Migrating DB'),
            call('DDL command file already executed as fileV1.09 systemVersion 1.10'),
            call('DDL command file already executed as fileV1.09 systemVersion 1.10')
        ])

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(Migrate, 'update_version')
    @mock.patch.object(Migrate, 'get_version', return_value="1.10")
    @mock.patch('migrate_db.get_ddl_files', return_value=['V1.11', 'V1.22'])
    @mock.patch('migrate_db.get_version_from_name', return_value="1.11")
    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    def test_should_stop_run_the_ddl_files_when_exception_on_update_version(self,
                                                                            mock_exception,
                                                                            mock_get_version_from_name,
                                                                            mock_get_ddl_files,
                                                                            mock_get_version,
                                                                            mock_update_version,
                                                                            mock_db,
                                                                            mock_logger,
                                                                            mock_info,
                                                                            mock_error
                                                                            ):
        mock_update_version.side_effect = DBExecutionException('op', 'msg')
        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.logger = LoggerAPI()
            migrate.init = mock_db
            migrate.schema = "schema"
            migrate.meta_schema = "meta_schema"

        migrate.run()

        mock_info.assert_has_calls([call('Migrating DB')])
        mock_get_version.assert_called_once_with()
        mock_get_ddl_files.assert_called_once_with()
        mock_get_version_from_name.assert_has_calls([call('V1.11')])
        mock_db.run_ddl_file.assert_has_calls([call('resources/V1.11')])
        mock_update_version.assert_has_calls([call("1.11")])
        mock_error.assert_has_calls([call('Migration stopped')])

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
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
                                                                     mock_logger,
                                                                     mock_info,
                                                                     mock_error
                                                                     ):
        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.init = mock_db
            migrate.logger = LoggerAPI()
            migrate.schema = "schema"
            migrate.meta_schema = "meta_schema"
            mock_db.run_ddl_file.side_effect = Exception("error")

        migrate.run()

        mock_info.assert_has_calls([call('Migrating DB')])
        mock_get_version.assert_called_once_with()
        mock_get_ddl_files.assert_called_once_with()
        mock_get_version_from_name.assert_has_calls([call('V1.11')])
        mock_db.run_ddl_file.assert_has_calls([call('resources/V1.11')])
        assert not mock_update_version.called
        mock_error.assert_has_calls([call('Migration stopped on error')])

    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch('psycopg2.connect')
    def test_should_establish_db_connection_on_create_schema(self,
                                                             mock_connect,
                                                             mock_logger,
                                                             mock_info
                                                             ):
        mock_con = mock_connect.return_value
        mock_cur = mock_con.cursor.return_value

        with patch.object(Migrate, '__init__', return_value=None) as _:
            migrate = Migrate()
            migrate.logger = LoggerAPI()
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
        mock_info.assert_called_with("Creating Schema: schema")

    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch('psycopg2.connect')
    def test_should_log_error_when_exception_on_execute_on_create_schema(self, mock_connect,
                                                                         mock_logger,
                                                                         mock_error,
                                                                         mock_info
                                                                         ):
        mock_con = mock_connect.return_value
        mock_cur = mock_con.cursor.return_value
        mock_cur.execute.side_effect = Exception("error")

        with patch.object(Migrate, '__init__', return_value=None) as _:
            migrate = Migrate()
            migrate.logger = LoggerAPI()
            migrate.param = {
                "db": "test_db",
                "user": "test_user",
                "pass": "test_pass",
                "host": "test_host",
                "port": 123,
            }

        migrate.create_schema("schema")

        mock_info.assert_called_once_with('Creating Schema: schema')
        mock_connect.assert_called_once_with(
            host='test_host',
            port=123,
            database='test_db',
            user='test_user',
            password='test_pass',
        )
        mock_cur.execute.assert_called_once_with('CREATE SCHEMA IF NOT EXISTS schema')
        mock_error.assert_called_once_with('Create schema : schema error')

    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch('psycopg2.connect', side_effect=Exception("error"))
    def test_should_log_error_on_exception_with_connection_on_create_schema(self, mock_connect,
                                                                            mock_logger,
                                                                            mock_error,
                                                                            mock_info
                                                                            ):
        mock_con = mock_connect.return_value
        mock_cur = mock_con.cursor.return_value

        with patch.object(Migrate, '__init__', return_value=None) as _:
            migrate = Migrate()
            migrate.logger = LoggerAPI()
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
        mock_error.assert_called_once_with('Create schema : schema error')
        mock_info.assert_called_once_with('Creating Schema: schema')

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(OrderType, '__init__', return_value=None)
    def test_should_return_system_version_on_get_version(self,
                                                         mock_order_type,
                                                         mock_db,
                                                         ):
        expected = "1.00"

        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.db = mock_db
            mock_db.get_records.return_value = expected

        actual = migrate.get_version()

        mock_order_type.assert_called_once_with('date_time', True)
        mock_db.get_records.assert_called_once()
        args = mock_db.get_records.call_args
        self.assertEqual((["version"],), args[0])
        self.assertEqual(OrderType, type(args[1]["order_type"]))
        self.assertEqual(1, args[1]["record_count"])
        self.assertEqual(expected, actual)

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(OrderType, '__init__', return_value=None)
    def test_should_return_0_00_on_empty_tuple_get_version_from_db(self,
                                                                   mock_order_type,
                                                                   mock_db,
                                                                   ):
        expected = "0.00"

        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.db = mock_db
            mock_db.get_records.return_value = ()

        actual = migrate.get_version()

        mock_order_type.assert_called_once_with('date_time', True)
        mock_db.get_records.assert_called_once()
        args = mock_db.get_records.call_args
        self.assertEqual((["version"],), args[0])
        self.assertEqual(OrderType, type(args[1]["order_type"]))
        self.assertEqual(1, args[1]["record_count"])
        self.assertEqual(expected, actual)

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(OrderType, '__init__', return_value=None)
    def test_should_return_0_00_on_table_not_found_exception_on_get_version(self,
                                                                            mock_order_type,
                                                                            mock_db,
                                                                            ):
        expected = "0.00"

        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.db = mock_db
            with mock.patch.object(TableNotFoundException, '__init__', return_value=None):
                mock_db.get_records.side_effect = TableNotFoundException("")

        actual = migrate.get_version()

        args = mock_db.get_records.call_args
        mock_db.get_records.assert_called_once()
        self.assertEqual((["version"],), args[0])
        self.assertEqual(OrderType, type(args[1]["order_type"]))
        mock_order_type.assert_called_once_with('date_time', True)
        self.assertEqual(1, args[1]["record_count"])
        self.assertEqual(expected, actual)

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(OrderType, '__init__', return_value=None)
    def test_should_return_negative_1_00_on_exception_on_get_version(self,
                                                                     mock_order_type,
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
        args = mock_db.get_records.call_args
        self.assertEqual((["version"],), args[0])
        self.assertEqual(OrderType, type(args[1]["order_type"]))
        mock_order_type.assert_called_once_with('date_time', True)
        self.assertEqual(1, args[1]["record_count"])

        mock_exception.assert_called_once_with('op', 'error')
        self.assertEqual(expected, actual)

    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    def test_should_call_insert_on_update_version(self,
                                                  mock_db,
                                                  mock_logger,
                                                  mock_info
                                                  ):
        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.logger = LoggerAPI()
            migrate.db = mock_db
            mock_db.insert_record.return_value = True

        migrate.update_version("version")

        mock_info.assert_called_once_with('updating migration version : version')
        mock_db.insert_record.assert_called_once_with({'version': 'version'})

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    def test_should_raise_exception_on_update_version(self,
                                                      mock_db,
                                                      mock_logger,
                                                      mock_info,
                                                      mock_exception
                                                      ):
        with mock.patch.object(Migrate, '__init__', return_value=None):
            migrate = Migrate()
            migrate.logger = LoggerAPI()
            migrate.db = mock_db
            with mock.patch.object(TableNotFoundException, '__init__', return_value=None):
                mock_db.insert_record.side_effect = DBExecutionException('op', 'message')

        with self.assertRaises(DBExecutionException):
            migrate.update_version("version")

        mock_info.assert_called_once_with('updating migration version : version')
        mock_db.insert_record.assert_called_once_with({'version': 'version'})
        mock_exception.assert_has_calls([call('op', 'message'), call('Update', 'version : version')])
