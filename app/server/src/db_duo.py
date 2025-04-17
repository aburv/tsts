"""
 PostgresDB class
"""
import uuid

import psycopg2

from src.config import Config
from src.data import DataModel
from src.logger import LoggerAPI
from src.responses import DBConnectionException, TableNotFoundException, DBExecutionException, DataValidationException


class PostgresDbDuo:
    """
    db api to the services
    """

    def __init__(self, data: DataModel) -> None:
        db_parameters = Config.get_db_parameters()
        try:
            self._schema = db_parameters.get("schema") if data.table.schema_type \
                else db_parameters.get("meta_schema")
            self.con = psycopg2.connect(
                host=db_parameters.get("host"),
                port=int(db_parameters.get("port")),
                database=db_parameters.get("db"),
                user=db_parameters.get("user"),
                password=db_parameters.get("pass"),
                options=f'-c search_path={self._schema}'
            )
            self.logger = LoggerAPI()
            self.audit_table = db_parameters.get("meta_schema") + ".audit"
            self.audit_field_table = db_parameters.get("meta_schema") + ".audit_field"
            self.con.autocommit = True
            self.client = self.con.cursor()

        except Exception as e:
            raise DBConnectionException(str(db_parameters) + " : " + str(data.get_table_name())) from e
        self._data = data

    def run_ddl_file(self, file_path: str) -> None:
        """
        Run DDL command from file
        """
        try:
            self.client.execute(open(file_path, "r").read())
            self.con.commit()
        except Exception as e:
            raise DBExecutionException('Run DDL file', f'{file_path} on {e}') from e

    def is_table_exist(self) -> bool:
        """
        check table presence
        """
        try:
            self.client.execute(
                f"SELECT * FROM information_schema.tables WHERE "
                f"table_schema='{self._schema}' and "
                f"table_name='{self._data.get_table_name()}'",
            )
            val = self.client.fetchone()
            self.con.commit()
            return val[0] if val is not None else False
        except Exception as e:
            raise DBExecutionException('Is Table exist', f'{self._data.get_table_name()} on {e}') from e

    def get_record_field_value(self) -> str | None:
        """
        Get record value
        """
        records = self.get_records()
        if len(records) > 0:
            field = self._data.get_filtering_fields()[0]
            return records[0][field]
        return None

    def get_records(self) -> list:
        """
        Get records by filter on condition and
        fields with limiting count
        """
        if not self.is_table_exist():
            raise TableNotFoundException(self._data.get_table_name())

        try:
            query, query_values = self.get_select_statement()
            self.client.execute(query, tuple(query_values))
            data = self.client.fetchall()
            self.con.commit()
            return self._data.frame_records(data)
        except Exception as e:
            raise DBExecutionException(
                'Retrieve',
                f'{self._data.get_table_name()} : {self._data.get_querying_fields_and_value()} on {e}'
            ) from e

    def get_select_statement(self):
        """
        Select Statement
        """
        fields = self._data.get_filtering_fields()
        if not fields:
            raise DBExecutionException('Retrieve', 'Query fields cannot be empty')
        query_param: dict = self._data.get_querying_fields_and_value()
        order_type = self._data.get_ordering_type()
        group_by_field = self._data.get_grouping_field()
        record_count = self._data.get_record_count()
        query = f'SELECT {", ".join(fields)} FROM {self._data.get_table_name()}'
        values = []
        if query_param is not None:
            values = query_param.values()
            query += " WHERE "
            query_list = []
            for (field, _) in query_param.items():
                query_list.append(field + "= %s")
            query += " AND ".join(query_list)
        if group_by_field is not None:
            query += f" GROUP BY {group_by_field}"
        if order_type is not None:
            query += f" ORDER BY {order_type.field} " + ("DESC" if order_type.is_desc else "ASC")
        if record_count is not None:
            query += f" LIMIT {record_count}"
        return query, tuple(values)

    def insert_record(self, my_id: str, r_id: str | None = None) -> None:
        """
        Insert record into DB
        """
        table_name = self._data.get_table_name()
        if self._data.is_empty():
            raise DataValidationException(
                'Nothing to Insert Failure: ',
                f'{table_name}'
            )
        values = self._data.get_values()
        try:
            self.client.execute("BEGIN;")
            self.logger.info_entry('Inserting Data')
            statement = (f"INSERT INTO {table_name} ({', '.join(self._data.get_fields())}) "
                         f"VALUES ({', '.join(['%s'] * len(values))});")
            self.client.execute(statement, tuple(values))
            if not self.is_operation_success("INSERT 0 1"):
                raise DBOperationException('Data not inserted')
            if self._data.table.schema_type:
                if r_id is None:
                    r_id = self._data.get('id')
                self.logger.info_entry('Updating Audits')
                self.update_audit(
                    table_name,
                    r_id,
                    self._data.get_audit_payload(),
                    my_id
                )
            self.client.execute("END;")
            self.con.commit()
        except Exception as e:
            if self.con:
                self.con.rollback()
            raise DBExecutionException(
                'Insert Failure: ' + (
                    'Syntax' if (isinstance(e, SyntaxError)) else 'System') + ' error',
                f'{table_name} {self._data.get_audit_payload()} : {e}') from e

    def update_record(self, my_id: str, r_id: str | None = None) -> None:
        """
        Update record data by id into DB
        """
        table_name = self._data.get_table_name()
        if self._data.is_empty():
            raise DataValidationException(
                'Nothing to Update Failure: ',
                f'{table_name}')
        try:
            self.client.execute("BEGIN;")
            self.logger.info_entry('Updating Record')
            statement, query_values = self.get_update_statement()

            self.client.execute(statement, query_values)

            if not self.is_operation_success("UPDATE 1"):
                raise DBOperationException('Data not updated')
            if self._data.table.schema_type:
                self.logger.info_entry('Updating Audits')
                self.update_audit(table_name, r_id, self._data.get_audit_payload(), my_id)
            self.client.execute("END;")
            self.con.commit()
        except Exception as e:
            if self.con is not None:
                self.con.rollback()
            raise DBExecutionException(
                'Update failure: ' + ('Syntax' if (isinstance(e, SyntaxError)) else 'System') + ' error',
                f'{table_name} : {self._data.get_audit_payload()} on {r_id}: {e}'
            ) from e

    def get_update_statement(self) -> (str, tuple):
        """
        Update Statement
        """
        query_param: dict = self._data.get_querying_fields_and_value()
        updating_fields = self._data.get_filtering_fields()
        query = ""
        if query_param is not None:
            query += " WHERE "
            query_list = []
            for (field, value) in query_param.items():
                query_list.append(field + "=%s")
            query += " AND ".join(query_list)
            query_fields = query_param.keys()

            updating_fields = {
                key: val
                for key, val in self._data._fields.items()
                if key not in query_fields
            }
        data_list = []
        values = []
        for field, value in updating_fields.items():
            values.append(str(value))
            data_list.append(f"{field}=%s")
        statement = f"UPDATE {self._data.get_table_name()} SET {', '.join(data_list)}" + query
        return statement, tuple(values + list(query_param.values()))

    def update_audit(self, table_name: str, r_id: str, data: dict, my_id: str):
        """
        update audit and audit field tables
        :return:
        :rtype:
        """
        self.logger.info_entry('Inserting Audit record')
        audit_id = uuid.uuid4()
        audit_statement = (
            f"INSERT INTO {self.audit_table} "
            f"(id, table_name, record_id, operation, op_user) "
            f"VALUES ('{audit_id}', '{table_name}', '{r_id}', 'INSERT', '{my_id}');"
        )
        self.client.execute(audit_statement)
        if not self.is_operation_success("INSERT 0 1"):
            raise DBOperationException('Audit not inserted')
        audit_field_statement_prefix = (
            f"INSERT INTO {self.audit_field_table} "
            f"(audit_id, field_name, new_value) VALUES "
        )
        for field, value in data.items():
            self.client.execute(audit_field_statement_prefix + f"('{audit_id}', '{field}', '{value}');")
            if not self.is_operation_success("INSERT 0 1"):
                raise DBOperationException('Audit field not inserted')

    def is_operation_success(self, status: str):
        """
        :return:
        :rtype:
        """
        return self.client.statusmessage == status

    def close(self):
        """
        :return:
        :rtype:
        """
        self.client.close()


class DBOperationException(Exception):
    """
    Custom DB Operation failure Exception
    """

    def __init__(self, message: str):
        super().__init__(message)
