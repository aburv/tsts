import unittest
from unittest import mock
from unittest.mock import patch, call

import psycopg2

from src.config import Config, Relation, Table
from src.db_duo import PostgresDbDuo, OrderType, DBOperationException
from src.responses import DBConnectionException, DBExecutionException, TableNotFoundException, DataValidationException


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

        relation = Relation.INIT
        db = PostgresDbDuo(relation)

        # mock_table_name.assert_called_once_with()
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
        self.assertEqual(db.table, relation.value)

    @mock.patch.object(DBConnectionException, '__init__', return_value=None)
    @mock.patch.object(Config, 'get_db_parameters')
    @mock.patch.object(psycopg2, 'connect', side_effect=Exception('error'))
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
            "port": 123,
            "schema": "schema",
            "meta_schema": "meta_schema"
        }
        mock_get_db_parameters.return_value = parameters

        with self.assertRaises(DBConnectionException):
            PostgresDbDuo(Relation.INIT)

        mock_get_db_parameters.assert_called_once_with()
        mock_client_init.assert_called_once_with(
            host='test_host',
            port=123,
            database='test_db',
            user='test_user',
            password='test_pass',
            options='-c search_path=schema'
        )
        mock_exception.assert_called_once_with(str(parameters) + " : ")

    @mock.patch('builtins.open')
    def test_should_run_ddl_file(self, mock_open):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)
            db.schema = 'schema'

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
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)
            db.schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value

        with self.assertRaises(Exception):
            db.run_ddl_file("file_name")

        mock_exception.assert_called_once_with('Run DDL file', 'file_name on error')
        mock_open.assert_called_once_with('file_name', 'r')
        assert not db.con.commit.called

    def test_should_return_true_in_is_table_exist(self):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)
            db.schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            db.client.fetchone.return_value = (True,)

        actual = db.is_table_exist()

        mock_execute.assert_called_once_with(
            "SELECT * FROM information_schema.tables WHERE table_schema='schema' and table_name='table'"
        )
        db.con.commit.assert_called_once_with()
        self.assertEqual(True, actual)

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    def test_should_raise_db_execution_exception_on_exception_is_table_exist(self, mock_exception):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)
            db.schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            mock_execute.side_effect = Exception("error")

        with self.assertRaises(DBExecutionException):
            db.is_table_exist()

        mock_execute.assert_called_once_with(
            "SELECT * FROM information_schema.tables WHERE table_schema='schema' and table_name='table'"
        )
        mock_exception.assert_called_once_with('Is Table exist', 'table on error')
        assert not db.con.commit.called

    @mock.patch.object(TableNotFoundException, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_table_exist', return_value=False)
    def test_should_raise_table_not_found_exception_when_table_is_exist_is_false_get_records(self,
                                                                                             mock_is_table_exist,
                                                                                             mock_exception
                                                                                             ):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)
            db.schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value

        with self.assertRaises(TableNotFoundException):
            db.get_records([])

        mock_is_table_exist.assert_called_once_with()
        assert not db.con.commit.called
        assert not db.client.cursor.called
        assert not db.client.execute.called
        assert not db.client.fetchall.called
        mock_exception.assert_called_once_with("table")

    @mock.patch.object(PostgresDbDuo, 'is_table_exist', return_value=True)
    def test_should_return_list_result_when_query_fields_group_order_DESC_count_get_records_(self,
                                                                                             mock_is_table_exist):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)
            db.schema = 'schema'

        expected = [{'field_1': "value_1", 'field_2': "value_2"}]

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            db.client.fetchall.return_value = (('value_1', 'value_2',),)

        actual = db.get_records(
            ['field_1', 'field_2'],
            query_param={'field_2': 2, 'field_5': '2'},
            order_type=OrderType('type', True),
            group_by_field="field_3",
            record_count=4
        )

        mock_is_table_exist.assert_called_once_with()
        mock_execute.assert_called_once_with(
            "SELECT field_1, field_2 FROM table WHERE field_2=2 AND field_5='2' "
            "GROUP BY field_3 ORDER BY type DESC LIMIT 4"
        )
        db.con.commit.assert_called_once_with()
        self.assertEqual(expected, actual)

    @mock.patch.object(PostgresDbDuo, 'is_table_exist', return_value=True)
    def test_should_return_list_result_when_query_fields_group_order_ASC_count_get_records_(self,
                                                                                            mock_is_table_exist):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)
            db.schema = 'schema'

        expected = [{'field_1': 'value_1', 'field_2': 'value_2'}]

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            db.client.fetchall.return_value = (('value_1', 'value_2',),)

        actual = db.get_records(
            ['field_1', 'field_2'],
            query_param={'field_2': 2},
            order_type=OrderType('type', False),
            group_by_field="field_3",
            record_count=4
        )

        mock_is_table_exist.assert_called_once_with()
        mock_execute.assert_called_once_with(
            "SELECT field_1, field_2 FROM table WHERE field_2=2 GROUP BY field_3 ORDER BY type ASC LIMIT 4"
        )
        db.con.commit.assert_called_once_with()
        self.assertEqual(expected, actual)

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_table_exist', return_value=True)
    def test_should_raise_db_execution_exception_when_fields_empty_list_on_exception_get_records(self,
                                                                                                 mock_is_table_exist,
                                                                                                 mock_exception
                                                                                                 ):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)
            db.schema = 'schema'

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            db.client.fetchall.return_value = None

        with self.assertRaises(DBExecutionException):
            db.get_records([])

        mock_exception.assert_called_once_with('Retrieve', 'Query fields cannot be empty')
        mock_is_table_exist.assert_called_once_with()
        mock_execute.assert_not_called()
        db.con.commit.assert_not_called()

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'is_table_exist', return_value=True)
    def test_should_raise_db_execution_exception_on_exception_get_records(self,
                                                                          mock_is_table_exist,
                                                                          mock_exception
                                                                          ):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            mock_execute.side_effect = Exception("error")

        with self.assertRaises(DBExecutionException):
            db.get_records(
                ['field_1', 'field_2'],
                query_param={'field_2': 2},
                order_type=OrderType('type', True)
            )

        mock_exception.assert_called_once_with(
            'Retrieve', 'table : SELECT field_1, field_2 FROM table WHERE field_2=2 ORDER BY type DESC on error')
        mock_is_table_exist.assert_called_once_with()
        mock_execute.assert_called_once_with(
            "SELECT field_1, field_2 FROM table WHERE field_2=2 ORDER BY type DESC"
        )
        assert not db.con.commit.called

    @mock.patch.object(Table, 'get_name', return_value="table")
    @mock.patch.object(PostgresDbDuo, 'is_operation_success', return_value=True)
    @mock.patch.object(PostgresDbDuo, 'update_audit')
    def test_should_insert_record_with_main_table(self,
                                                  mock_audit_update,
                                                  mock_is_success,
                                                  mock_table_get_name):
        mock_is_success.side_effect = [True]

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", True)
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        db.insert_record({'field': 'value', 'field_2': 1, "id": "id"}, "my_id")

        mock_audit_update.assert_called_once_with('id', {'field': 'value', 'field_2': 1}, 'my_id')
        mock_is_success.assert_has_calls([
            call('INSERT 0 1'),
        ])
        mock_table_get_name.assert_called_once_with()
        mock_execute.assert_has_calls([
            call('BEGIN;'),
            call("INSERT INTO table (field, field_2, id) VALUES ('value', 1, 'id');"),
            call('END;')
        ])
        db.con.commit.assert_called_once_with()

    @mock.patch.object(Table, 'get_name', return_value="table")
    @mock.patch.object(PostgresDbDuo, 'is_operation_success', return_value=True)
    @mock.patch.object(PostgresDbDuo, 'update_audit')
    def test_should_insert_record_with_non_main_table(self,
                                                      mock_audit_update,
                                                      mock_is_success,
                                                      mock_table_get_name):
        mock_is_success.side_effect = [True]
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        db.insert_record({'field': 'value', 'field_2': 1, "id": "id"}, "my_id")

        assert not mock_audit_update.called
        mock_is_success.assert_has_calls([
            call('INSERT 0 1'),
        ])
        mock_table_get_name.assert_called_once_with()
        mock_execute.assert_has_calls([
            call('BEGIN;'),
            call("INSERT INTO table (field, field_2, id) VALUES ('value', 1, 'id');"),
            call('END;')
        ])
        db.con.commit.assert_called_once_with()

    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(Table, 'get_name', return_value="table")
    @mock.patch.object(PostgresDbDuo, 'is_operation_success', return_value=True)
    @mock.patch('uuid.uuid4', return_value='audit_id')
    def test_should_raise_validation_exception_in_insert_record_on_data_empty(self,
                                                                              mock_id,
                                                                              mock_is_success,
                                                                              mock_table_get_name,
                                                                              mock_exception
                                                                              ):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        with self.assertRaises(DataValidationException):
            db.insert_record({}, "my_id")

        assert not mock_id.called
        mock_is_success.assert_has_calls([])
        mock_table_get_name.assert_called_once_with()
        mock_execute.assert_has_calls([])
        assert not db.con.commit.called

        mock_exception.assert_called_once_with('Nothing to Insert Failure: ', 'table')

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(Table, 'get_name', return_value="table")
    @mock.patch.object(PostgresDbDuo, 'is_operation_success')
    @mock.patch('uuid.uuid4', return_value='audit_id')
    def test_should_raise_execution_exception_in_insert_record_on_exception(self,
                                                                            mock_id,
                                                                            mock_is_success,
                                                                            mock_table_get_name,
                                                                            mock_exception):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            mock_execute.side_effect = Exception("error")

        with self.assertRaises(DBExecutionException):
            db.insert_record({'field': 'value', 'field_2': 'value_2', "id": "id"}, "my_id")

        mock_table_get_name.assert_called_once_with()
        mock_is_success.assert_has_calls([])
        mock_execute.assert_has_calls([
            call('BEGIN;')
        ])
        mock_exception.assert_called_once_with(
            'Insert Failure: System error',
            "table {'field': 'value', 'field_2': 'value_2', 'id': 'id'} : error"
        )
        assert not mock_id.called
        assert not db.con.commit.called

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(Table, 'get_name', return_value="table")
    @mock.patch.object(PostgresDbDuo, 'is_operation_success')
    def test_should_raise_execution_exception_in_insert_record_on_no_execution_on_insert_statement(self,
                                                                                                   mock_is_success,
                                                                                                   mock_table_get_name,
                                                                                                   mock_exception):
        data = {'field': 'value', 'field_2': 'value_2', "id": "id"}

        mock_is_success.side_effect = [
            False
        ]
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        with self.assertRaises(DBExecutionException):
            db.insert_record(data, "my_id")

        mock_table_get_name.assert_called_once_with()
        mock_execute.assert_has_calls([
            call('BEGIN;'),
            call("INSERT INTO table (field, field_2, id) VALUES ('value', 'value_2', 'id');"),
        ])
        mock_exception.assert_called_once_with(
            'Insert Failure: System error',
            f"table {data} : Data not inserted"
        )
        mock_is_success.assert_has_calls([call('INSERT 0 1')])
        assert not db.con.commit.called

    @mock.patch.object(Table, 'get_name', return_value="table")
    @mock.patch.object(PostgresDbDuo, 'is_operation_success', return_value=True)
    @mock.patch.object(PostgresDbDuo, 'update_audit', return_value='audit_id')
    def test_should_update_record_with_main_table(self,
                                                  mock_audit_update,
                                                  mock_is_success,
                                                  mock_table_get_name):
        mock_is_success.side_effect = [True]

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", True)
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        db.update_record("record_id", {'field': 'value', 'field_2': 1}, "my_id")

        mock_table_get_name.assert_called_once_with()
        mock_is_success.assert_has_calls([
            call('UPDATE 0 1'),
        ])
        mock_audit_update.assert_called_once_with('record_id', {'field': 'value', 'field_2': 1}, 'my_id')
        mock_execute.assert_has_calls([
            call('BEGIN;'),
            call("UPDATE table SET 'field'='value', 'field_2'=1 WHERE id = record_id;"),
            call('END;')
        ])
        db.con.commit.assert_called_once_with()

    @mock.patch.object(Table, 'get_name', return_value="table")
    @mock.patch.object(PostgresDbDuo, 'is_operation_success', return_value=True)
    @mock.patch.object(PostgresDbDuo, 'update_audit')
    def test_should_update_record_with_non_main_table(self,
                                                      mock_audit_update,
                                                      mock_is_success,
                                                      mock_table_get_name):
        mock_is_success.side_effect = [True]

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        db.update_record("id", {'field': 'value', 'field_2': 1}, "my_id")

        assert not mock_audit_update.called
        mock_is_success.assert_has_calls([
            call('UPDATE 0 1'),
        ])
        mock_table_get_name.assert_called_once_with()
        mock_execute.assert_has_calls([
            call('BEGIN;'),
            call("UPDATE table SET 'field'='value', 'field_2'=1 WHERE id = id;"),
            call('END;')
        ])
        db.con.commit.assert_called_once_with()

    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(Table, 'get_name', return_value="table")
    @mock.patch.object(PostgresDbDuo, 'is_operation_success', return_value=True)
    @mock.patch.object(PostgresDbDuo, 'update_audit', return_value=True)
    def test_should_raise_validation_exception_in_update_record_on_data_empty(self,
                                                                              mock_audit_update,
                                                                              mock_is_success,
                                                                              mock_table_get_name,
                                                                              mock_exception
                                                                              ):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        with self.assertRaises(DataValidationException):
            db.update_record("id", {}, "my_id")

        assert not mock_audit_update.called
        mock_is_success.assert_has_calls([])
        mock_table_get_name.assert_called_once_with()
        mock_execute.assert_has_calls([])
        assert not db.con.commit.called

        mock_exception.assert_called_once_with('Nothing to Update Failure: ', 'table')

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(Table, 'get_name', return_value="table")
    @mock.patch.object(PostgresDbDuo, 'is_operation_success', return_value=True)
    @mock.patch.object(PostgresDbDuo, 'update_audit', return_value=True)
    def test_should_raise_execution_exception_in_update_record_on_exception(self,
                                                                            mock_audit_update,
                                                                            mock_is_success,
                                                                            mock_table_get_name,
                                                                            mock_exception):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute
            mock_execute.side_effect = Exception("error")

        with self.assertRaises(DBExecutionException):
            db.update_record("record_id", {'field': 'value', 'field_2': 'value_2'}, "my_id")

        mock_table_get_name.assert_called_once_with()
        mock_is_success.assert_has_calls([])
        mock_execute.assert_has_calls([
            call("BEGIN;")
        ])
        mock_exception.assert_called_once_with(
            'Update failure: System error',
            "table : {'field': 'value', 'field_2': 'value_2'} on record_id: error"
        )
        assert not mock_audit_update.called
        assert not db.con.commit.called

    @mock.patch.object(DBExecutionException, '__init__', return_value=None)
    @mock.patch.object(Table, 'get_name', return_value="table")
    @mock.patch.object(PostgresDbDuo, 'is_operation_success')
    def test_should_raise_execution_exception_in_update_record_on_no_execution_on_update_statement(self,
                                                                                                   mock_is_success,
                                                                                                   mock_table_get_name,
                                                                                                   mock_exception):
        mock_is_success.side_effect = [
            False,
        ]
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", False)
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        with self.assertRaises(DBExecutionException):
            db.update_record(
                "record_id",
                {'field': 'value', 'field_2': 'value_2'},
                "my_id"
            )

        mock_table_get_name.assert_called_once_with()
        mock_is_success.assert_has_calls([call('UPDATE 0 1')])
        mock_execute.assert_has_calls([
            call('BEGIN;'),
            call("UPDATE table SET 'field'='value', 'field_2'='value_2' WHERE id = record_id;"),
        ])

        mock_exception.assert_called_once_with(
            'Update failure: System error',
            "table : {'field': 'value', 'field_2': 'value_2'} on record_id: Data not updated"
        )

        assert not db.con.commit.called

    @mock.patch.object(Table, 'get_name', return_value="table")
    @mock.patch.object(PostgresDbDuo, 'is_operation_success')
    @mock.patch('uuid.uuid4', return_value='audit_id')
    def test_should_insert_audit_and_audit_fields_on_update_audit(
            self,
            mock_id,
            mock_is_success,
            mock_table_get_name,
    ):
        mock_is_success.side_effect = [
            True,
            True,
            True
        ]

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", True)
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        db.update_audit(
            "record_id",
            {'field': 'value', 'field_2': 'value_2'},
            "my_id"
        )

        mock_table_get_name.assert_called_once_with()
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
    @mock.patch.object(Table, 'get_name', return_value="table")
    @mock.patch.object(PostgresDbDuo, 'is_operation_success')
    @mock.patch('uuid.uuid4', return_value='audit_id')
    def test_should_raise_execution_exception_in_update_audit_on_no_execution_on_audit_statement(
            self,
            mock_id,
            mock_is_success,
            mock_table_get_name,
            mock_exception
    ):
        mock_is_success.side_effect = [
            False,
        ]

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", True)
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        with self.assertRaises(DBOperationException):
            db.update_audit(
                "record_id",
                {'field': 'value', 'field_2': 'value_2'},
                "my_id"
            )

        mock_table_get_name.assert_called_once_with()
        mock_is_success.assert_has_calls([call('INSERT 0 1')])
        mock_id.assert_called_once_with()
        mock_execute.assert_has_calls([
            call(
                "INSERT INTO table_1 (id, table_name, record_id, operation, op_user) "
                "VALUES ('audit_id', 'table', 'record_id', 'INSERT', 'my_id');"
            )
        ])

        mock_exception.assert_called_once_with(
            "Audit not inserted"
        )
        assert not db.con.commit.called

    @mock.patch.object(DBOperationException, '__init__', return_value=None)
    @mock.patch.object(Table, 'get_name', return_value="table")
    @mock.patch.object(PostgresDbDuo, 'is_operation_success')
    @mock.patch('uuid.uuid4', return_value='audit_id')
    def test_should_raise_execution_exception_in_update_audit_on_no_execution_on_audit_field_statement(
            self,
            mock_id,
            mock_is_success,
            mock_table_get_name,
            mock_exception
    ):
        mock_is_success.side_effect = [
            True,
            False
        ]

        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)
            db.table = Table("table", True)
            db.audit_table = "table_1"
            db.audit_field_table = "table_2"

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_execute = mock_connect.cursor.return_value.execute

        with self.assertRaises(DBOperationException):
            db.update_audit(
                "record_id",
                {'field': 'value', 'field_2': 'value_2'},
                "my_id"
            )

        mock_table_get_name.assert_called_once_with()
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
        assert not db.con.commit.called

    def test_should_true_if_status_message_matches_to_param_in_is_operation_success(self):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value
            mock_connect.cursor.return_value.statusmessage = "status"

        actual = db.is_operation_success(
            "status",
        )

        self.assertTrue(actual)

        # assert not db.con.commit.called

    def test_should_false_if_status_message_mismatches_to_param_in_is_operation_success(self):
        with patch.object(PostgresDbDuo, '__init__', return_value=None) as _:
            db = PostgresDbDuo(Relation.INIT)

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
            db = PostgresDbDuo(Relation.INIT)

        with mock.patch('psycopg2.connect') as mock_connect:
            db.con = mock_connect
            db.client = mock_connect.cursor.return_value

        db.close()

        db.client.close.assert_called_once_with()
