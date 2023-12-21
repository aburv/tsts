import unittest
from unittest import mock
from unittest.mock import patch, PropertyMock

import psycopg2

from src.config import Config
from src.db_duo import PostgresDbDuo, OrderType
from src.responses import DBConnectionException, SchemaNotFoundException


class Con:
    autocommit: bool

    def cursor(self):
        return "Cursor Object"


class OrderTypeTest(unittest.TestCase):

    def test_should_instantiate_order_type(self):
        order_type = OrderType("field", True)

        self.assertEqual(order_type.field, "field")
        self.assertEqual(order_type.is_desc, True)


class DbDuoTest(unittest.TestCase):

    @mock.patch.object(Config, 'get_db_parameters')
    @mock.patch.object(psycopg2, 'connect')
    def test_should_establish_db_connection_on_init(self,
                                                    mock_client_init,
                                                    mock_get_db_parameters
                                                    ):
        client = Con()
        mock_client_init.return_value = client
        mock_get_db_parameters.return_value = {
            "db": "test_db",
            "user": "test_user",
            "pass": "test_pass",
            "host": "test_host",
            "port": 123
        }

        db = PostgresDbDuo("tableName")

        mock_get_db_parameters.assert_called_once_with()
        mock_client_init.assert_called_once_with(
            host='test_host',
            port=123,
            database='test_db',
            user='test_user',
            password='test_pass'
        )
        self.assertEqual(True, isinstance(db, PostgresDbDuo))
        self.assertEqual(db.con, client)
        self.assertEqual(True, db.con.autocommit)
        self.assertEqual(db.client, client.cursor())
        self.assertEqual(db.table, "tableName")

    @mock.patch.object(DBConnectionException, '__init__', return_value=None)
    @mock.patch.object(Config, 'get_db_parameters')
    @mock.patch.object(psycopg2, 'connect', side_effect=Exception())
    def test_should_raise_db_connection_exception_on_init(self,
                                                          mock_client_init,
                                                          mock_get_db_parameters,
                                                          mock_exception
                                                          ):
        parameters = {
            "db": "test_db",
            "user": "test_user",
            "pass": "test_pass",
            "host": "test_host",
            "port": 123
        }
        mock_get_db_parameters.return_value = parameters

        with self.assertRaises(DBConnectionException):
            PostgresDbDuo("tableName")

        mock_get_db_parameters.assert_called_once_with()
        mock_client_init.assert_called_once_with(
            host='test_host',
            port=123,
            database='test_db',
            user='test_user',
            password='test_pass'
        )
        mock_exception.assert_called_once_with(str(parameters))

    @mock.patch('builtins.open')
    def test_should_run_ddl(self, mock_open):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo("table")
            db.table = 'table'
            db.schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            mock_connect.cursor.return_value.rownumber = 1

        db.run_ddl("file_name")

        mock_open.assert_called_once_with('file_name', 'r')
        mock_execute.assert_called_once_with(mock_open().read())

    @mock.patch('builtins.open')
    @mock.patch('builtins.print')
    def test_should_run_ddl_fails(self, mock_print, mock_open):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo("table")
            db.table = 'table'
            db.schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            mock_connect.cursor.return_value.rownumber = 0

        db.run_ddl("file_name")

        mock_open.assert_called_once_with('file_name', 'r')
        mock_execute.assert_called_once_with(mock_open().read())
        mock_print.assert_called_once_with('Not able to complete the ddl command')

    def test_should_return_true_in_is_table_exist(self):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo("table")
            db.table = 'table'
            db.schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            db.client.fetchone.return_value = (True,)

        actual = db.is_table_exist()

        mock_execute.assert_called_once_with(
            'SELECT * FROM information_schema.tables WHERE table_name=%s and table_schema=%s',
            ('table', 'schema',)
        )

        self.assertEqual(True, actual)

    def test_should_return_false_in_is_table_exist(self):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo("table")
            db.table = 'table'
            db.schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            db.client.fetchone.return_value = (False,)

        actual = db.is_table_exist()

        mock_execute.assert_called_once_with(
            'SELECT * FROM information_schema.tables WHERE table_name=%s and table_schema=%s',
            ('table', 'schema',)
        )

        self.assertEqual(False, actual)

    @mock.patch('builtins.print')
    def test_should_return_false_in_is_table_exist_on_exception(self, mock_print):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo("table")
            db.table = 'table'
            db.schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            mock_execute.side_effect = Exception("error")

        actual = db.is_table_exist()

        mock_execute.assert_called_once_with(
            'SELECT * FROM information_schema.tables WHERE table_name=%s and table_schema=%s',
            ('table', 'schema',)
        )
        mock_print.assert_called_once_with('Not able to execute listing tables : error')
        self.assertEqual(False, actual)

    @mock.patch.object(PostgresDbDuo, 'is_table_exist', return_value=True)
    def test_should_return_tuple_result_get_records_with_all_fields_no_query(self,
                                                                             mock_is_table_exist
                                                                             ):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo('table')
            db.table = 'table'
            db.schema = 'schema'

        expected = "value"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            db.client.fetchone.return_value = (expected,)

        actual = db.get_records(
            None,
            [],
            OrderType('type', True)
        )

        mock_is_table_exist.assert_called_once_with()
        mock_execute.assert_called_once_with(
            'SELECT %s FROM %s ORDER BY %s DESC',
            ('*', 'schema.table', 'type',)
        )
        self.assertEqual(expected, actual)

    @mock.patch.object(PostgresDbDuo, 'is_table_exist', return_value=True)
    def test_should_return_tuple_result_get_records_with_query_and_specific_fields(self,
                                                                                   mock_is_table_exist):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo('table')
            db.table = 'table'
            db.schema = 'schema'

        expected = "value"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            db.client.fetchone.return_value = (expected,)

        actual = db.get_records(
            {'field_2': '2'},
            ['field_1', 'field_2'],
            OrderType('type', True)
        )

        mock_is_table_exist.assert_called_once_with()
        mock_execute.assert_called_once_with(
            'SELECT %s FROM %s WHERE field_2=2 ORDER BY %s DESC',
            ('field_1, field_2', 'schema.table', 'type',)
        )
        self.assertEqual(expected, actual)

    @mock.patch.object(SchemaNotFoundException, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_table_exist', return_value=False)
    def test_should_raise_schema_not_found_exception_get_records(self,
                                                                 mock_is_table_exist,
                                                                 mock_exception
                                                                 ):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo('table')
            db.table = 'table'
            db.schema = 'schema'

        with self.assertRaises(SchemaNotFoundException):
            db.get_records(
                None,
                [],
                OrderType('type', True)
            )

        mock_is_table_exist.assert_called_once_with()
        mock_exception.assert_called_once_with("table")

    @mock.patch.object(PostgresDbDuo, 'is_table_exist', return_value=True)
    @mock.patch('builtins.print')
    def test_should_print_exception_get_records_on_exception(self,
                                                             mock_print,
                                                             mock_is_table_exist
                                                             ):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo('table')
            db.table = 'table'
            db.schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            mock_execute.side_effect = Exception("error")

        db.get_records(
            {'field_2': '2'},
            ['field_1', 'field_2'],
            OrderType('type', True)
        )

        mock_print.assert_called_once_with('error')
        mock_is_table_exist.assert_called_once_with()
        mock_execute.assert_called_once_with(
            'SELECT %s FROM %s WHERE field_2=2 ORDER BY %s DESC',
            ('field_1, field_2', 'schema.table', 'type',)
        )

    def test_should_insert_record(self):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo("table")
            db.table = 'table'
            db.schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            mock_connect.cursor.return_value.rowcount = 1

        db.insert_record({'field': 'value', 'field_2': 'value_2'})

        mock_execute.assert_called_once_with(
            'INSERT INTO %s (%s) values (%s)',
            ('schema.table', 'field, field_2', 'value, value_2',)
        )

    @mock.patch('builtins.print')
    def test_should_print_error_in_insert_record_on_exception(self, mock_print):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo("table")
            db.table = 'table'
            db.schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            mock_execute.side_effect = Exception("error")

        db.insert_record({'field': 'value', 'field_2': 'value_2'})

        mock_execute.assert_called_once_with(
            'INSERT INTO %s (%s) values (%s)',
            ('schema.table', 'field, field_2', 'value, value_2',)
        )
        mock_print.assert_called_once_with('error')

    @mock.patch('builtins.print')
    def test_should_print_error_in_insert_record_on_failure(self, mock_print):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo("table")
            db.table = 'table'
            db.schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            mock_connect.cursor.return_value.rowcount = 0

        db.insert_record({'field': 'value', 'field_2': 'value_2'})

        mock_execute.assert_called_once_with(
            'INSERT INTO %s (%s) values (%s)',
            ('schema.table', 'field, field_2', 'value, value_2',)
        )

        mock_print.assert_called_once_with('not inserted')
