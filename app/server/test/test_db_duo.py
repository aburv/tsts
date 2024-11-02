import unittest
from unittest import mock
from unittest.mock import patch, call

import psycopg2

from src.config import Config, Relation, Table
from src.data import DataModel, OrderType
from src.db_duo import PostgresDbDuo, DBOperationException
from src.logger import LoggerAPI
from src.responses import DBConnectionException, DBExecutionException, TableNotFoundException, DataValidationException


class DbDuoTest(unittest.TestCase):

    @mock.patch.object(Config, 'get_db_parameters')
    @mock.patch.object(Table, '__init__', return_value=None)
    @mock.patch.object(psycopg2, 'connect')
    def test_should_establish_db_connection_on_init(self,
                                                    mock_client_init,
                                                    mock_table,
                                                    mock_get_db_parameters
                                                    ):
        mock_con = mock_client_init.return_value

        mock_get_db_parameters.return_value = {
            "db": "test_db",
            "user": "test_user",
            "pass": "test_pass",
            "host": "test_host",
            "port": 123,
            "schema": "schema",
            "meta_schema": "meta_schema"
        }

        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = True
            model.table = mock_table

        db = PostgresDbDuo(model)

        mock_get_db_parameters.assert_called_once_with()
        mock_client_init.assert_called_once_with(
            host='test_host',
            port=123,
            database='test_db',
            user='test_user',
            password='test_pass',
            options='-c search_path=schema'
        )
        self.assertEqual(True, isinstance(db, PostgresDbDuo))
        self.assertEqual(db.con, mock_client_init.return_value)
        self.assertEqual(True, db.con.autocommit)
        self.assertEqual(db.client, mock_con.cursor.return_value)
        self.assertEqual(db._data, model)
        self.assertEqual(db._schema, "schema")

    @mock.patch.object(DBConnectionException, '__init__', return_value=None)
    @mock.patch.object(Table, '__init__', return_value=None)
    @mock.patch.object(Config, 'get_db_parameters')
    @mock.patch.object(psycopg2, 'connect', side_effect=Exception('error'))
    @mock.patch.object(DataModel, 'get_table_name')
    def test_should_raise_db_connection_exception_on_init(self,
                                                          mock_table_name,
                                                          mock_client_init,
                                                          mock_get_db_parameters,
                                                          mock_table,
                                                          mock_exception
                                                          ):
        parameters = {
            "db": "test_db",
            "user": "test_user",
            "pass": "test_pass",
            "host": "test_host",
            "port": 123,
            "schema": "schema",
            "meta_schema": "meta_schema"
        }
        mock_get_db_parameters.return_value = parameters
        mock_table_name.return_value = "table"
        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = True
            model.table = mock_table

        with self.assertRaises(DBConnectionException):
            PostgresDbDuo(model)

        mock_get_db_parameters.assert_called_once_with()
        mock_client_init.assert_called_once_with(
            host='test_host',
            port=123,
            database='test_db',
            user='test_user',
            password='test_pass',
            options='-c search_path=schema'
        )
        mock_exception.assert_called_once_with(str(parameters) + " : table")

    @mock.patch('builtins.open')
    def test_should_run_ddl_file(self, mock_open):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT.value)
            db._schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        db.run_ddl_file("file_name")

        mock_open.assert_called_once_with('file_name', 'r')
        mock_execute.assert_called_once_with(mock_open().read())
        db.con.commit.assert_called_once_with()

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch('builtins.open', side_effect=Exception('error'))
    def test_should_raise_db_execution_exception_on_exception_run_ddl_file(self,
                                                                           mock_open,
                                                                           mock_exception
                                                                           ):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value

        with self.assertRaises(Exception):
            db.run_ddl_file("file_name")

        mock_exception.assert_called_once_with('Run DDL file', 'file_name on error')
        mock_open.assert_called_once_with('file_name', 'r')
        assert not db.con.commit.called

    @mock.patch.object(Table, '__init__', return_value=None)
    @mock.patch.object(DataModel, 'get_table_name')
    def test_should_return_true_in_is_table_exist(self, mock_table_name, mock_table):
        mock_table_name.return_value = "table"
        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            model.table = mock_table

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model
            db._schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            db.client.fetchone.return_value = (True,)

        actual = db.is_table_exist()

        db.client.fetchone.assert_called_once_with()
        mock_execute.assert_called_once_with(
            "SELECT * FROM information_schema.tables WHERE table_schema='schema' and table_name='table'"
        )
        db.con.commit.assert_called_once_with()
        self.assertEqual(True, actual)

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(Table, '__init__', return_value=None)
    @mock.patch.object(DataModel, 'get_table_name')
    def test_should_raise_db_execution_exception_on_exception_is_table_exist(self,
                                                                             mock_table_name,
                                                                             mock_table,
                                                                             mock_exception):
        mock_table_name.return_value = "table"
        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = False
            model.table = mock_table

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model
            db._schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            mock_execute.side_effect = Exception("error")

        with self.assertRaises(DBExecutionException):
            db.is_table_exist()

        assert not db.client.fetchone.called
        mock_execute.assert_called_once_with(
            "SELECT * FROM information_schema.tables WHERE table_schema='schema' and table_name='table'"
        )
        mock_exception.assert_called_once_with('Is Table exist', 'table on error')
        assert not db.con.commit.called

    @mock.patch.object(TableNotFoundException, '__init__', return_value=None)
    @mock.patch.object(Table, '__init__', return_value=None)
    @mock.patch.object(DataModel, 'frame_records')
    @mock.patch.object(DataModel, 'get_table_name')
    @mock.patch.object(PostgresDbDuo, 'get_select_statement', return_value="")
    @mock.patch.object(PostgresDbDuo, 'is_table_exist', return_value=False)
    def test_should_raise_table_not_found_exception_when_table_is_exist_is_false_get_records(self,
                                                                                             mock_is_table_exist,
                                                                                             mock_select_statement,
                                                                                             mock_table_name,
                                                                                             mock_frame_records,
                                                                                             mock_table,
                                                                                             mock_exception
                                                                                             ):
        mock_table_name.return_value = "table"
        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = False
            model.table = mock_table

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model
            db._schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value

        with self.assertRaises(TableNotFoundException):
            db.get_records()

        mock_is_table_exist.assert_called_once_with()
        assert not mock_select_statement.called
        assert not db.client.fetchall.called
        assert not db.con.commit.called
        assert not mock_frame_records.called

        mock_exception.assert_called_once_with("table")

    @mock.patch.object(Table, '__init__', return_value=True)
    @mock.patch.object(DataModel, 'frame_records')
    @mock.patch.object(DataModel, 'get_table_name')
    @mock.patch.object(PostgresDbDuo, 'get_select_statement',
                       return_value=("SELECT field1 FROM table WHERE field=%", ("value",)))
    @mock.patch.object(PostgresDbDuo, 'is_table_exist', return_value=True)
    def test_should_return_list_result_on_get_records(self,
                                                      mock_is_table_exist,
                                                      mock_select_statement,
                                                      mock_table_name,
                                                      mock_frame_records,
                                                      mock_table):
        mock_table_name.return_value = "table"

        expected = [{'field_1': "value_1", 'field_2': "value_2"}]
        mock_frame_records.return_value = expected

        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = False
            model.table = mock_table

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model
            db._schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            db.client.fetchall.return_value = (('value_1', 'value_2',),)

        actual = db.get_records()

        mock_is_table_exist.assert_called_once_with()
        mock_select_statement.assert_called_once_with()
        db.client.fetchall.assert_called_once_with()
        db.con.commit.assert_called_once_with()
        db.client.execute.assert_called_once_with('SELECT field1 FROM table WHERE field=%', ('value',))
        mock_frame_records.assert_called_once_with((('value_1', 'value_2'),))

        self.assertEqual(expected, actual)

    @mock.patch.object(DataModel, 'get_querying_fields_and_value',
                       return_value={'field_1': "value_1", 'field_2': "value_2"})
    @mock.patch.object(DataModel, 'get_table_name', return_value="table")
    def test_should_return_update_statement_data_on_get_update_statement(self,
                                                                         mock_table_name,
                                                                         mock_get_querying_fields_and_value):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            model._fields = {'field_1': "value_1", 'field_2': "value_1", "field": "value"}

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model

        actual = db.get_update_statement()
        mock_table_name.assert_called_once_with()
        mock_get_querying_fields_and_value.assert_called_once_with()
        self.assertEqual(
            ('UPDATE table SET field=%s WHERE field_1=%s AND field_2=%s', ('value_1', 'value_2')),
            actual
        )

    @mock.patch.object(DataModel, 'get_record_count', return_value=1)
    @mock.patch.object(DataModel, 'get_grouping_field', return_value="field_4")
    @mock.patch.object(DataModel, 'get_ordering_type', return_value=OrderType("field_4", True))
    @mock.patch.object(DataModel, 'get_querying_fields_and_value',
                       return_value={'field_1': "value_1", 'field_2': "value_2"})
    @mock.patch.object(DataModel, 'get_filtering_fields', return_value=['field_5', 'field_4'])
    @mock.patch.object(DataModel, 'get_table_name', return_value="table")
    @mock.patch.object(Table, '__init__', return_value=None)
    def test_should_return_framed_select_statement(self,
                                                   mock_table,
                                                   mock_table_name,
                                                   mock_get_filtering_fields,
                                                   mock_get_querying_fields_and_value,
                                                   mock_get_ordering_type,
                                                   mock_get_grouping_field,
                                                   mock_get_record_count
                                                   ):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = False
            model.table = mock_table
            model._fields = {'field_1': "value_1", 'field_2': "value_1"}

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model

        actual = db.get_select_statement()

        mock_get_filtering_fields.assert_called_once_with()
        mock_get_querying_fields_and_value.assert_called_once_with()
        mock_get_ordering_type.assert_called_once_with()
        mock_get_grouping_field.assert_called_once_with()
        mock_get_record_count.assert_called_once_with()
        mock_table_name.assert_called_once_with()
        self.assertEqual(
            ('SELECT field_5, field_4 FROM table WHERE field_1= %s AND field_2= %s '
             'GROUP BY field_4 ORDER BY field_4 DESC LIMIT 1',
             ('value_1', 'value_2')),
            actual
        )

    @mock.patch.object(DataModel, 'get_record_count', return_value=1)
    @mock.patch.object(DataModel, 'get_grouping_field', return_value=None)
    @mock.patch.object(DataModel, 'get_ordering_type', return_value=['field_1', 'field_2'])
    @mock.patch.object(DataModel, 'get_querying_fields_and_value', return_value=['field_1', 'field_2'])
    @mock.patch.object(DataModel, 'get_filtering_fields', return_value=[])
    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(Table, '__init__', return_value=None)
    def test_should_raise_db_execution_exception_on_get_select_statement(self,
                                                                         mock_table,
                                                                         mock_exception,
                                                                         mock_get_filtering_fields,
                                                                         mock_get_querying_fields_and_value,
                                                                         mock_get_ordering_type,
                                                                         mock_get_grouping_field,
                                                                         mock_get_record_count
                                                                         ):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = False
            model.table = mock_table

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model

        with self.assertRaises(DBExecutionException) as _:
            db.get_select_statement()

        mock_get_filtering_fields.assert_called_once_with()
        assert not mock_get_querying_fields_and_value.called
        assert not mock_get_ordering_type.called
        assert not mock_get_grouping_field.called
        assert not mock_get_record_count.called

        mock_exception.assert_called_once_with('Retrieve', 'Query fields cannot be empty')

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(Table, '__init__', return_value=None)
    @mock.patch.object(DataModel, 'frame_records')
    @mock.patch.object(DataModel, 'get_querying_fields_and_value')
    @mock.patch.object(DataModel, 'get_table_name')
    @mock.patch.object(PostgresDbDuo, 'get_select_statement',
                       return_value=("SELECT field1 FROM table WHERE field=%s", ('values',)))
    @mock.patch.object(PostgresDbDuo, 'is_table_exist', return_value=True)
    def test_should_raise_db_execution_exception_on_exception_get_records(self,
                                                                          mock_is_table_exist,
                                                                          mock_select_statement,
                                                                          mock_table_name,
                                                                          mock_get_querying_fields_and_value,
                                                                          mock_frame_records,
                                                                          mock_table,
                                                                          mock_exception
                                                                          ):
        mock_table_name.return_value = "table"
        mock_get_querying_fields_and_value.return_value = {'field_2': 2}
        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            model.table = mock_table

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            db.client.execute.side_effect = Exception("error")

        with self.assertRaises(DBExecutionException):
            db.get_records()

        mock_is_table_exist.assert_called_once_with()
        mock_select_statement.assert_called_once_with()
        db.client.execute.assert_called_once_with('SELECT field1 FROM table WHERE field=%s', ('values',))
        assert not db.con.commit.called
        assert not db.client.fetchall.called
        assert not mock_frame_records.called

        mock_exception.assert_called_once_with(
            'Retrieve', "table : {'field_2': 2} on error"
        )

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_operation_success')
    @mock.patch.object(PostgresDbDuo, 'update_audit')
    @mock.patch.object(Table, '__init__', return_value=None)
    @mock.patch.object(DataModel, 'get', return_value='id')
    @mock.patch.object(DataModel, 'get_fields', return_value=["field"])
    @mock.patch.object(DataModel, 'get_values', return_value=["value"])
    @mock.patch.object(DataModel, 'get_table_name', return_value="table")
    @mock.patch.object(DataModel, 'get_audit_payload', return_value={'field': 'value', 'field_2': 1})
    @mock.patch.object(DataModel, 'is_empty', return_value=False)
    def test_should_insert_record_with_main_table(self,
                                                  mock_is_empty,
                                                  mock_get_audit_payload,
                                                  mock_table_name,
                                                  mock_get_values,
                                                  mock_get_fields,
                                                  mock_get,
                                                  mock_table,
                                                  mock_audit_update,
                                                  mock_is_success,
                                                  mock_log):
        mock_is_success.side_effect = [True]

        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = True
            model.table = mock_table

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model
            db.logger = mock_log
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        db.insert_record("my_id")

        mock_is_empty.assert_called_once_with()
        mock_get_fields.assert_called_once_with()
        mock_get_values.assert_called_once_with()
        mock_get.assert_called_once_with("id")
        mock_audit_update.assert_called_once_with('table', 'id', {'field': 'value', 'field_2': 1}, 'my_id')
        mock_is_success.assert_has_calls([
            call('INSERT 0 1'),
        ])
        mock_get_audit_payload.assert_called_once_with()
        mock_table_name.assert_called_once_with()
        mock_log.info_entry.assert_has_calls([call('Inserting Data'), call('Updating Audits')])
        mock_execute.assert_has_calls([
            call('BEGIN;'),
            call('INSERT INTO table (field) VALUES (%s);', ('value',)),
            call('END;')
        ])
        db.con.commit.assert_called_once_with()
        assert not db.con.rollback.called

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(Table, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_operation_success')
    @mock.patch.object(PostgresDbDuo, 'update_audit')
    @mock.patch.object(DataModel, 'get', return_value='id')
    @mock.patch.object(DataModel, 'get_fields', return_value=["field"])
    @mock.patch.object(DataModel, 'get_values', return_value=["value"])
    @mock.patch.object(DataModel, 'get_table_name', return_value="table")
    @mock.patch.object(DataModel, 'get_audit_payload', return_value={'field': 'value', 'field_2': 1})
    @mock.patch.object(DataModel, 'is_empty', return_value=False)
    def test_should_insert_record_with_non_main_table(self,
                                                      mock_is_empty,
                                                      mock_get_audit_payload,
                                                      mock_table_name,
                                                      mock_get_values,
                                                      mock_get_fields,
                                                      mock_get,
                                                      mock_audit_update,
                                                      mock_is_success,
                                                      mock_table,
                                                      mock_log):
        mock_is_success.side_effect = [True]

        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = False
            model.table = mock_table

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model
            db.logger = mock_log
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        db.insert_record("my_id")

        mock_is_empty.assert_called_once_with()
        assert not mock_get.called
        assert not mock_audit_update.called
        mock_get_values.assert_called_once_with()
        mock_get_fields.assert_called_once_with()
        mock_is_success.assert_has_calls([
            call('INSERT 0 1'),
        ])
        assert not mock_get_audit_payload.called
        mock_table_name.assert_called_once_with()
        mock_log.info_entry.assert_called_once_with("Inserting Data")
        mock_execute.assert_has_calls([
            call('BEGIN;'),
            call('INSERT INTO table (field) VALUES (%s);', ('value',)),
            call('END;')
        ])
        db.con.commit.assert_called_once_with()
        assert not db.con.rollback.called

    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(Table, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_operation_success', return_value=True)
    @mock.patch.object(DataModel, 'get', return_value='id')
    @mock.patch.object(DataModel, 'get_values')
    @mock.patch.object(DataModel, 'get_fields')
    @mock.patch.object(DataModel, 'is_empty', return_value=True)
    @mock.patch.object(DataModel, 'get_table_name')
    def test_should_raise_validation_exception_in_insert_record_on_data_empty(self,
                                                                              mock_table_name,
                                                                              mock_is_empty,
                                                                              mock_get_fields,
                                                                              mock_get_value,
                                                                              mock_get,
                                                                              mock_is_success,
                                                                              mock_table,
                                                                              mock_log,
                                                                              mock_exception
                                                                              ):
        mock_table_name.return_value = 'table'

        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = False
            model.table = mock_table

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        with self.assertRaises(DataValidationException):
            db.insert_record("my_id")

        mock_is_empty.assert_called_once_with()
        assert not mock_get.called
        assert not mock_get_fields.called
        assert not mock_get_value.called
        mock_is_success.assert_has_calls([])
        mock_table_name.assert_called_once_with()
        mock_execute.assert_has_calls([])
        assert not mock_log.info_entry.called
        assert not db.con.commit.called
        assert not db.con.rollback.called

        mock_exception.assert_called_once_with('Nothing to Insert Failure: ', 'table')

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(Table, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_operation_success')
    @mock.patch.object(DataModel, 'get', return_value='id')
    @mock.patch.object(DataModel, 'get_audit_payload', return_value={'field': 'value', 'field_2': 1})
    @mock.patch.object(DataModel, 'get_fields', return_value=["field"])
    @mock.patch.object(DataModel, 'get_values', return_value=["value"])
    @mock.patch.object(DataModel, 'is_empty', return_value=False)
    @mock.patch.object(DataModel, 'get_table_name')
    def test_should_raise_execution_exception_in_insert_record_on_exception(self,
                                                                            mock_table_name,
                                                                            mock_is_empty,
                                                                            mock_get_values,
                                                                            mock_get_fields,
                                                                            mock_get_audit_payload,
                                                                            mock_get,
                                                                            mock_is_success,
                                                                            mock_table,
                                                                            mock_log,
                                                                            mock_exception):
        data = {'field': 'value', 'field_2': 'value_2', 'id': 'id'}
        mock_table_name.return_value = 'table'
        mock_get_audit_payload.return_value = data

        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = False
            model.table = mock_table

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model
            db.logger = mock_log
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            db.client.execute.side_effect = Exception("error")

        with self.assertRaises(DBExecutionException):
            db.insert_record("my_id")

        mock_table_name.assert_called_once_with()
        mock_is_empty.assert_called_once_with()
        assert not mock_get_fields.called
        mock_get_values.assert_called_once_with()
        mock_get_audit_payload.assert_called_once_with()
        assert not mock_get.called
        mock_is_success.assert_has_calls([])
        db.client.execute.assert_has_calls([
            call('BEGIN;')
        ])
        mock_exception.assert_called_once_with(
            'Insert Failure: System error',
            f"table {data} : error"
        )
        assert not mock_log.info_entry.called
        assert not db.con.commit.called
        db.con.rollback.assert_called_once_with()

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(Table, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_operation_success')
    @mock.patch.object(DataModel, 'get', return_value='id')
    @mock.patch.object(DataModel, 'get_audit_payload')
    @mock.patch.object(DataModel, 'get_fields', return_value=["field"])
    @mock.patch.object(DataModel, 'get_values', return_value=["value"])
    @mock.patch.object(DataModel, 'is_empty', return_value=False)
    @mock.patch.object(DataModel, 'get_table_name')
    def test_should_raise_execution_exception_in_insert_record_on_no_execution_on_insert_record(
            self,
            mock_table_name,
            mock_is_empty,
            mock_get_values,
            mock_get_fields,
            mock_get_audit_payload,
            mock_get,
            mock_is_success,
            mock_table,
            mock_log,
            mock_exception
    ):
        data = {'field': 'value', 'field_2': 'value_2', "id": "id"}
        mock_get_audit_payload.return_value = data
        mock_is_success.side_effect = [False]
        mock_table_name.return_value = 'table'

        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = False
            model.table = mock_table

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model
            db.logger = mock_log
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        with self.assertRaises(DBExecutionException):
            with self.assertRaises(DBOperationException):
                db.insert_record("my_id")

        mock_is_empty.assert_called_once_with()
        assert not mock_get.called
        mock_table_name.assert_called_once_with()
        mock_execute.assert_has_calls([
            call('BEGIN;'),
        ])
        mock_exception.assert_called_once_with(
            'Insert Failure: System error',
            f"table {data} : Data not inserted"
        )
        mock_get_values.assert_called_once_with()
        mock_get_fields.assert_called_once_with()
        mock_is_success.assert_has_calls([call('INSERT 0 1')])
        mock_get_audit_payload.assert_called_once_with()
        mock_log.info_entry.assert_called_once_with('Inserting Data')
        db.con.rollback.assert_called_once_with()
        assert not db.con.commit.called

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(Table, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_operation_success', return_value=True)
    @mock.patch.object(PostgresDbDuo, 'update_audit', return_value='audit_id')
    @mock.patch.object(PostgresDbDuo, 'get_update_statement',
                       return_value=('UPDATE table SET field1=value1 WHERE field2=%', ("value2",)))
    @mock.patch.object(DataModel, 'get_table_name', return_value="table")
    @mock.patch.object(DataModel, 'get_audit_payload', return_value={'field': 'value', 'field_2': 1})
    @mock.patch.object(DataModel, 'is_empty', return_value=False)
    def test_should_update_record_with_main_table(self,
                                                  mock_is_empty,
                                                  mock_audit_payload,
                                                  mock_table_name,
                                                  mock_update_statement,
                                                  mock_audit_update,
                                                  mock_is_success,
                                                  mock_table,
                                                  mock_log):
        mock_table_name.return_value = 'table'

        mock_is_success.side_effect = [True]

        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = True
            model.table = mock_table

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model
            db.logger = mock_log
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        db.update_record("record_id", "my_id")

        mock_is_empty.assert_called_once_with()
        mock_update_statement.assert_called_once_with()
        mock_table_name.assert_called_once_with()
        mock_audit_payload.assert_called_once_with()
        mock_is_success.assert_has_calls([
            call('UPDATE 0 1'),
        ])
        mock_audit_update.assert_called_once_with('table', 'record_id', {'field': 'value', 'field_2': 1}, 'my_id')
        mock_execute.assert_has_calls([
            call('BEGIN;'),
            call('UPDATE table SET field1=value1 WHERE field2=%', ('value2',)),
            call('END;')
        ])
        mock_log.info_entry.assert_has_calls([call('Updating Record'), call("Updating Audits")])
        db.con.commit.assert_called_once_with()
        assert not db.con.rollback.called

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(Table, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_operation_success', return_value=True)
    @mock.patch.object(PostgresDbDuo, 'update_audit')
    @mock.patch.object(PostgresDbDuo, 'get_update_statement',
                       return_value=('UPDATE table SET field1=value1 WHERE field2=%', ("value2",)))
    @mock.patch.object(DataModel, 'get_table_name', return_value="table")
    @mock.patch.object(DataModel, 'is_empty', return_value=False)
    def test_should_update_record_with_non_main_table(self,
                                                      mock_is_empty,
                                                      mock_table_name,
                                                      mock_update_statement,
                                                      mock_audit_update,
                                                      mock_is_success,
                                                      mock_table,
                                                      mock_log):
        mock_is_success.side_effect = [True]

        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = False
            model.table = mock_table

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model
            db.logger = mock_log
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        db.update_record("record_id", "my_id")

        mock_is_empty.assert_called_once_with()
        mock_update_statement.assert_called_once_with()
        assert not mock_audit_update.called
        mock_is_success.assert_has_calls([
            call('UPDATE 0 1'),
        ])
        mock_table_name.assert_called_once_with()
        mock_execute.assert_has_calls([
            call('BEGIN;'),
            call('UPDATE table SET field1=value1 WHERE field2=%', ('value2',)),
            call('END;')
        ])
        mock_log.info_entry.assert_has_calls([call('Updating Record')])
        db.con.commit.assert_called_once_with()
        assert not db.con.rollback.called

    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(Table, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_operation_success', return_value=True)
    @mock.patch.object(PostgresDbDuo, 'update_audit', return_value=True)
    @mock.patch.object(PostgresDbDuo, 'get_update_statement')
    @mock.patch.object(DataModel, 'is_empty', return_value=True)
    @mock.patch.object(DataModel, 'get_table_name')
    def test_should_raise_validation_exception_in_update_record_on_data_empty(self,
                                                                              mock_table_name,
                                                                              mock_is_empty,
                                                                              mock_update_statement,
                                                                              mock_audit_update,
                                                                              mock_is_success,
                                                                              mock_table,
                                                                              mock_log,
                                                                              mock_exception
                                                                              ):
        mock_table_name.return_value = "table"

        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = False
            model.table = mock_table

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db.logger = mock_log
            db._data = model

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        with self.assertRaises(DataValidationException):
            db.update_record("record_id", "my_id")

        mock_table_name.assert_called_once_with()
        mock_is_empty.assert_called_once_with()
        assert not mock_update_statement.called
        assert not mock_audit_update.called
        assert not mock_is_success.called
        assert not mock_execute.called
        assert not db.con.commit.called
        assert not db.con.rollback.called
        assert not mock_log.info_entry.called
        mock_exception.assert_called_once_with('Nothing to Update Failure: ', 'table')

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(Table, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_operation_success', return_value=True)
    @mock.patch.object(PostgresDbDuo, 'update_audit', return_value=True)
    @mock.patch.object(PostgresDbDuo, 'get_update_statement', return_value=("UPDATE ", ("value",)))
    @mock.patch.object(DataModel, 'get_audit_payload', return_value={'field': 'value', 'field_2': 'value_2'})
    @mock.patch.object(DataModel, 'is_empty', return_value=False)
    @mock.patch.object(DataModel, 'get_table_name')
    def test_should_raise_execution_exception_in_update_record_on_exception(self,
                                                                            mock_table_name,
                                                                            mock_is_empty,
                                                                            mock_get_audit_payload,
                                                                            mock_audit_update,
                                                                            mock_update_statement,
                                                                            mock_is_success,
                                                                            mock_table,
                                                                            mock_log,
                                                                            mock_exception):
        mock_table_name.return_value = "table"
        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = False
            model.table = mock_table

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model
            db.logger = mock_log
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            mock_execute.side_effect = Exception("error")

        with self.assertRaises(DBExecutionException):
            with self.assertRaises(DataValidationException):
                db.update_record("record_id", "my_id")

        mock_table_name.assert_called_once_with()
        mock_is_empty.assert_called_once_with()
        assert not mock_update_statement.called
        mock_get_audit_payload.assert_called_once_with()
        mock_is_success.assert_has_calls([])
        mock_execute.assert_has_calls([
            call("BEGIN;")
        ])
        mock_exception.assert_called_once_with(
            'Update failure: System error',
            "table : {'field': 'value', 'field_2': 'value_2'} on record_id: error"
        )
        assert not mock_log.info_entry.called
        assert not mock_audit_update.called
        db.con.rollback.assert_called_once_with()
        assert not db.con.commit.called

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(Table, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_operation_success')
    @mock.patch.object(PostgresDbDuo, 'get_update_statement',
                       return_value=("UPDATE table set field1=value1 WHERE field2=%s", ("value3",)))
    @mock.patch.object(DataModel, 'get_audit_payload', return_value={'field': 'value', 'field_2': 'value_2'})
    @mock.patch.object(DataModel, 'get_table_name')
    @mock.patch.object(DataModel, 'is_empty', return_value=False)
    def test_should_raise_execution_exception_in_update_record_on_no_execution_on_update_record(
            self,
            mock_is_empty,
            mock_table_name,
            mock_audit_payload,
            mock_get_update_statement,
            mock_is_success,
            mock_table,
            mock_log,
            mock_exception):
        mock_table_name.return_value = "table"

        mock_is_success.side_effect = [False]

        with mock.patch.object(DataModel, '__init__', return_value=None):
            model = DataModel(Relation.INIT)
            mock_table.schema_type = False
            model.table = mock_table

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(model)
            db._data = model
            db.logger = mock_log
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        with self.assertRaises(DBExecutionException):
            with self.assertRaises(DBOperationException):
                db.update_record("record_id", "my_id")

        mock_table_name.assert_called_once_with()
        mock_is_empty.assert_called_once_with()
        mock_get_update_statement.assert_called_once_with()
        mock_is_success.assert_has_calls([
            call('UPDATE 0 1'),
        ])
        mock_execute.assert_has_calls([
            call('BEGIN;'),
            call("UPDATE table set field1=value1 WHERE field2=%s", ("value3",))
        ])

        mock_audit_payload.assert_called_once_with()
        mock_log.info_entry.assert_has_calls([call("Updating Record")])
        mock_exception.assert_called_once_with(
            'Update failure: System error',
            "table : {'field': 'value', 'field_2': 'value_2'} on record_id: Data not updated"
        )

        assert not db.con.commit.called
        db.con.rollback.assert_called_once_with()

    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_operation_success')
    @mock.patch('uuid.uuid4', return_value='audit_id')
    def test_should_insert_audit_and_audit_fields_on_update_audit(
            self,
            mock_id,
            mock_is_success,
            mock_log
    ):
        mock_is_success.side_effect = [
            True,
            True,
            True
        ]

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT.value)
            db.logger = mock_log
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        db.update_audit(
            "table",
            "record_id",
            {'field': 'value', 'field_2': 'value_2'},
            "my_id"
        )

        mock_log.info_entry.assert_called_once_with('Inserting Audit record')
        mock_is_success.assert_has_calls([
            call('INSERT 0 1'),
            call('INSERT 0 1'),
            call('INSERT 0 1')
        ])
        mock_id.assert_called_once_with()
        mock_execute.assert_has_calls([
            call(
                "INSERT INTO table_1 (id, table_name, record_id, operation, op_user) "
                "VALUES ('audit_id', 'table', 'record_id', 'INSERT', 'my_id');"
            ),
            call(
                "INSERT INTO table_2 (audit_id, field_name, new_value) "
                "VALUES ('audit_id', 'field', 'value');"
            ),
            call(
                "INSERT INTO table_2 (audit_id, field_name, new_value) "
                "VALUES ('audit_id', 'field_2', 'value_2');"
            )
        ])

    @mock.patch.object(DBOperationException, '__init__', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_operation_success')
    @mock.patch('uuid.uuid4', return_value='audit_id')
    def test_should_raise_execution_exception_in_update_audit_on_no_execution_on_audit_statement(
            self,
            mock_id,
            mock_is_success,
            mock_log,
            mock_exception
    ):
        mock_is_success.side_effect = [
            False,
        ]

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT.value)
            db.logger = mock_log
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        with self.assertRaises(DBOperationException):
            db.update_audit(
                "table",
                "record_id",
                {'field': 'value', 'field_2': 'value_2'},
                "my_id"
            )

        mock_is_success.assert_has_calls([call('INSERT 0 1')])
        mock_id.assert_called_once_with()
        mock_execute.assert_has_calls([
            call(
                "INSERT INTO table_1 (id, table_name, record_id, operation, op_user) "
                "VALUES ('audit_id', 'table', 'record_id', 'INSERT', 'my_id');"
            )
        ])
        mock_exception.assert_called_once_with("Audit not inserted")
        mock_log.info_entry.assert_has_calls([call('Inserting Audit record')])

    @mock.patch.object(DBOperationException, '__init__', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_operation_success')
    @mock.patch('uuid.uuid4', return_value='audit_id')
    def test_should_raise_execution_exception_in_update_audit_on_no_execution_on_audit_field_statement(
            self,
            mock_id,
            mock_is_success,
            mock_log,
            mock_exception
    ):
        mock_is_success.side_effect = [
            True,
            False
        ]

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT.value)
            db.logger = mock_log
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        with self.assertRaises(DBOperationException):
            db.update_audit(
                "table",
                "record_id",
                {'field': 'value', 'field_2': 'value_2'},
                "my_id"
            )

        mock_is_success.assert_has_calls([
            call('INSERT 0 1'),
            call('INSERT 0 1')
        ])
        mock_id.assert_called_once_with()
        mock_execute.assert_has_calls([
            call(
                "INSERT INTO table_1 (id, table_name, record_id, operation, op_user) "
                "VALUES ('audit_id', 'table', 'record_id', 'INSERT', 'my_id');"
            ),
            call(
                "INSERT INTO table_2 (audit_id, field_name, new_value) "
                "VALUES ('audit_id', 'field', 'value');"
            )
        ])
        mock_exception.assert_called_once_with('Audit field not inserted')
        mock_log.info_entry.assert_has_calls([call('Inserting Audit record')])

    def test_should_true_if_status_message_matches_to_param_in_is_operation_success(self):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT.value)

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_connect.cursor.return_value.statusmessage = "status"

        actual = db.is_operation_success("status")

        self.assertTrue(actual)

    def test_should_false_if_status_message_mismatches_to_param_in_is_operation_success(self):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT.value)

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_connect.cursor.return_value.statusmessage = "status 2"

        actual = db.is_operation_success(
            "status",
        )

        self.assertFalse(actual)

    def test_should_call_close_api_in_close(self):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT.value)

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value

        db.close()

        db.client.close.assert_called_once_with()
