"""
 PostgresDB class
"""
import uuid

import psycopg2

from src.config import Config, Relation
from src.responses import DBConnectionException, TableNotFoundException, DBExecutionException, DataValidationException


class OrderType:
    """
    Order type
    """
    is_desc: bool
    field: str

    def __init__(self, field: str, is_desc: bool):
        self.is_desc = is_desc
        self.field = field


class PostgresDbDuo:
    """
    db api to the services
    """

    def __init__(self, table: Relation) -> None:
        db_parameters = Config.get_db_parameters()
        try:
            self.schema = db_parameters.get("schema") if table.value.schema_type \
                else db_parameters.get("meta_schema")
            self.con = psycopg2.connect(
                host=db_parameters.get("host"),
                port=int(db_parameters.get("port")),
                database=db_parameters.get("db"),
                user=db_parameters.get("user"),
                password=db_parameters.get("pass"),
                options=f'-c search_path={self.schema}'
            )
            self.audit_table = db_parameters.get("meta_schema") + ".audit"
            self.audit_field_table = db_parameters.get("meta_schema") + ".audit_field"
            self.con.autocommit = True
            self.client = self.con.cursor()

        except Exception as e:
            raise DBConnectionException(str(db_parameters) + " : " + str(table.value.get_name())) from e
        self.table = table.value

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
                f"table_schema='{self.schema}' and "
                f"table_name='{self.table.get_name()}'",
            )
            val = self.client.fetchone()
            self.con.commit()
            return val[0] if val is not None else False
        except Exception as e:
            raise DBExecutionException('Is Table exist', f'{self.table.get_name()} on {e}') from e

    def get_records(self,
                    fields: list,
                    query_param: dict | None = None,
                    order_type: OrderType | None = None,
                    group_by_field: str | None = None,
                    record_count: int | None = None
                    ) -> list:
        """
        Get records by filter on condition and
        fields with limiting count
        """
        if not self.is_table_exist():
            raise TableNotFoundException(self.table.get_name())

        if len(fields) == 0:
            raise DBExecutionException('Retrieve', 'Query fields cannot be empty')

        query = f'SELECT {", ".join(fields)} FROM {self.table.get_name()}'
        if query_param is not None:
            query += " WHERE "
            query_list = []
            for (field, value) in query_param.items():
                if isinstance(value, str):
                    query_list.append(field + "='" + value + "'")
                else:
                    query_list.append(field + "=" + str(value))
            query += " AND ".join(query_list)
        if group_by_field is not None:
            query += f" GROUP BY {group_by_field}"
        if order_type is not None:
            query += f" ORDER BY {order_type.field} " + ("DESC" if order_type.is_desc else "ASC")
        if record_count is not None:
            query += f" LIMIT {record_count}"
        try:
            self.client.execute(query)
            data = self.client.fetchall()
            self.con.commit()
            return self.frame_records(data, fields)
        except Exception as e:
            raise DBExecutionException('Retrieve', f'{self.table.get_name()} : {query} on {e}') from e

    @staticmethod
    def frame_records(data, fields):
        """
        Framing the records
        """
        records = []
        if data is not None:
            for data_item in data:
                record = {}
                for index, field in enumerate(fields):
                    record[field] = data_item[index]
                records.append(record)
        return records

    def insert_record(self, data: dict, my_id: str) -> None:
        """
        Insert record into DB
        """
        table_name = self.table.get_name()
        if len(data.items()) > 0:
            fields = []
            values = []

            for field, value in data.items():
                fields.append(f"{field}")
                if isinstance(value, str):
                    values.append(f"'{str(value)}'")
                else:
                    values.append(str(value))
            try:
                self.client.execute("BEGIN;")
                statement = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(values)});"
                self.client.execute(statement)
                if not self.is_operation_success("INSERT 0 1"):
                    raise DBOperationException('Data not inserted')
                if self.table.schema_type:
                    self.update_audit(
                        data['id'],
                        {key: val for key, val in data.items() if key != 'id'},
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
                    f'{table_name} {data} : {e}') from e
        else:
            raise DataValidationException(
                'Nothing to Insert Failure: ',
                f'{table_name}'
            )

    def update_record(self, r_id: str, data: dict, my_id: str) -> None:
        """
        Update record data by id into DB
        """
        table_name = self.table.get_name()

        if len(data.items()) > 0:
            data_list = []
            for field, value in data.items():
                if isinstance(value, str):
                    value_temp = f"'{str(value)}'"
                else:
                    value_temp = f"{str(value)}"
                data_list.append(f"'{field}'={value_temp}")
            try:
                self.client.execute("BEGIN;")
                statement = f"UPDATE {table_name} SET {', '.join(data_list)} WHERE id = {r_id};"
                self.client.execute(statement)
                if not self.is_operation_success("UPDATE 0 1"):
                    raise DBOperationException('Data not updated')
                if self.table.schema_type:
                    self.update_audit(r_id, data, my_id)
                self.client.execute("END;")
                self.con.commit()
            except Exception as e:
                if self.con:
                    self.con.rollback()
                raise DBExecutionException(
                    'Update failure: ' + ('Syntax' if (isinstance(e, SyntaxError)) else 'System') + ' error',
                    f'{table_name} : {data} on {r_id}: {e}'
                ) from e
        else:
            raise DataValidationException(
                'Nothing to Update Failure: ',
                f'{table_name}')

    def update_audit(self, r_id, data, my_id):
        """
        update audit and audit field tables
        :return:
        :rtype:
        """
        audit_id = uuid.uuid4()
        table_name = self.table.get_name()
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

    def is_operation_success(self, status):
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
