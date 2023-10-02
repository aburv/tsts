import unittest
from typing import Any
from unittest import mock
from unittest.mock import call, Mock, patch

from src.db_duo import PostgresDbDuo, OrderType
from src.migrate_db import Migrate, get_version_from_name, get_ddl_files
from src.responses import SchemaNotFoundException, DBConnectionException


class MigrateTest(unittest.TestCase):

    @mock.patch('os.walk', return_value=[("", "", ['', ''])])
    def test_should_return_path_files(self, mock_os_walk):
        self.assertEqual(['', ''], get_ddl_files())

        mock_os_walk.assert_called_once_with("../resources")

    def test_should_return_version_number(self):
        self.assertEqual(1.00, get_version_from_name("V1.00__desc"))

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    def test_should_init_migrate(self,
                                 mock_db
                                 ):
        migrate = Migrate()

        mock_db.assert_called_once_with('migrate')
        self.assertEqual(True, isinstance(migrate, Migrate))

    @mock.patch.object(DBConnectionException, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__')
    @mock.patch('builtins.print')
    def test_should_print_on_db_connection_exception_init_migrate(self,
                                                                  mock_print,
                                                                  mock_db,
                                                                  mock_exception,
                                                                  ):
        mock_db.side_effect = DBConnectionException("error")

        migrate = Migrate()

        mock_db.assert_called_once_with('migrate')
        mock_print.assert_called_once_with('Unable to connect: error')
        self.assertEqual(True, isinstance(migrate, Migrate))

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'run_ddl', return_value=None)
    @mock.patch.object(Migrate, 'update_version', return_value=True)
    @mock.patch.object(Migrate, 'get_version', return_value=1.10)
    @mock.patch('src.migrate_db.get_ddl_files', return_value=['V1.11', 'V1.22'])
    @mock.patch('src.migrate_db.get_version_from_name', return_value=1.11)
    @mock.patch('builtins.print')
    def test_should_run_the_ddl_files(self,
                                      mock_print,
                                      mock_get_version_from_name,
                                      mock_get_ddl_files,
                                      mock_get_version,
                                      mock_update_version,
                                      mock_run_ddl,
                                      mock_db
                                      ):
        migrate = Migrate()

        migrate.run()

        mock_print.assert_has_calls([call('Migrating DB ')])
        mock_get_ddl_files.assert_called_once_with()
        mock_get_version.assert_called_once_with()
        mock_run_ddl.assert_has_calls([call('../resources/V1.11'), call('../resources/V1.22')])
        mock_update_version.assert_has_calls([call(1.11), call(1.11)])
        mock_get_version_from_name.assert_has_calls([call('V1.11'), call('V1.22')])

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'run_ddl', return_value=None)
    @mock.patch.object(Migrate, 'update_version', return_value=False)
    @mock.patch.object(Migrate, 'get_version', return_value=1.10)
    @mock.patch('src.migrate_db.get_ddl_files', return_value=['V1.11', 'V1.22'])
    @mock.patch('src.migrate_db.get_version_from_name', return_value=1.11)
    @mock.patch('builtins.print')
    def test_should_stop_run_the_ddl_files_with_failed_update(self,
                                                              mock_print,
                                                              mock_get_version_from_name,
                                                              mock_get_ddl_files,
                                                              mock_get_version,
                                                              mock_update_version,
                                                              mock_run_ddl,
                                                              mock_db
                                                              ):
        migrate = Migrate()

        migrate.run()

        mock_print.assert_has_calls([call('Migrating DB ')])
        mock_get_ddl_files.assert_called_once_with()
        mock_get_version.assert_called_once_with()
        mock_run_ddl.assert_has_calls([call('../resources/V1.11')])
        mock_update_version.assert_has_calls([call(1.11)])
        mock_get_version_from_name.assert_has_calls([call('V1.11')])

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'run_ddl', side_effect=Exception("error"))
    @mock.patch.object(Migrate, 'update_version', return_value=False)
    @mock.patch.object(Migrate, 'get_version', return_value=1.10)
    @mock.patch('src.migrate_db.get_ddl_files', return_value=['V1.11', 'V1.22'])
    @mock.patch('src.migrate_db.get_version_from_name', return_value=1.11)
    @mock.patch('builtins.print')
    def test_should_run_the_ddl_files_on_exception(self,
                                                   mock_print,
                                                   mock_get_version_from_name,
                                                   mock_get_ddl_files,
                                                   mock_get_version,
                                                   mock_update_version,
                                                   mock_run_ddl,
                                                   mock_db
                                                   ):
        migrate = Migrate()

        migrate.run()

        mock_print.assert_has_calls([call('Migrating DB '), call('Unable to perform: error')])
        mock_get_ddl_files.assert_called_once_with()
        mock_get_version.assert_called_once_with()
        mock_run_ddl.assert_has_calls([call('../resources/V1.11')])
        mock_update_version.assert_has_calls([])
        mock_get_version_from_name.assert_has_calls([call('V1.11')])

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'get_records')
    @mock.patch.object(OrderType, '__init__', return_value=None)
    def test_should_get_version_from_db(self,
                                        mock_order_type,
                                        mock_get_records,
                                        mock_db,
                                        ):
        mock_get_records.return_value = ("1.00",)
        migrate = Migrate()
        expected = 1.00

        actual = migrate.get_version()

        mock_order_type.assert_called_once_with('date_time', True)
        mock_get_records.assert_called_once()
        args = mock_get_records.call_args.args
        self.assertEqual(None, args[0])
        self.assertEqual(["version"], args[1])
        self.assertEqual(OrderType, type(args[2]))
        self.assertEqual(expected, actual)

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'get_records', side_effect=Exception("error"))
    @mock.patch.object(OrderType, '__init__', return_value=None)
    @mock.patch('builtins.print')
    def test_should__return_100_0_on_exception_inn_get_version(self,
                                                               mock_print,
                                                               mock_order_type,
                                                               mock_get_records,
                                                               mock_db,
                                                               ):
        migrate = Migrate()
        expected = 100.00

        actual = migrate.get_version()

        mock_order_type.assert_called_once_with('date_time', True)
        mock_get_records.assert_called_once()
        mock_print.assert_called_once_with('Not able to execute get latest version: error')
        args = mock_get_records.call_args.args
        self.assertEqual(None, args[0])
        self.assertEqual(["version"], args[1])
        self.assertEqual(OrderType, type(args[2]))
        self.assertEqual(expected, actual)

    @mock.patch.object(SchemaNotFoundException, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'get_records')
    @mock.patch.object(OrderType, '__init__', return_value=None)
    def test_should_return_0_0_schema_not_found_exception_in_get_version(self,
                                                                         mock_order_type,
                                                                         mock_get_records,
                                                                         mock_db,
                                                                         mock_exception
                                                                         ):
        mock_get_records.side_effect = SchemaNotFoundException("")
        migrate = Migrate()
        expected = 0.00

        actual = migrate.get_version()

        mock_order_type.assert_called_once_with('date_time', True)
        mock_get_records.assert_called_once()
        args = mock_get_records.call_args.args
        self.assertEqual(None, args[0])
        self.assertEqual(["version"], args[1])
        self.assertEqual(OrderType, type(args[2]))
        self.assertEqual(expected, actual)

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'insert_record', return_value=True)
    def test_should_update_version(self,
                                   mock_insert_record,
                                   mock_db,
                                   ):
        migrate = Migrate()
        expected = True

        actual = migrate.update_version("version")

        mock_insert_record.assert_called_once_with({'version': 'version'})
        self.assertEqual(expected, actual)
