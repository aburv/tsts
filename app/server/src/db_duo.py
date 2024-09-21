"""
 PostgresDB class
"""

import psycopg2

from src.config import Config, Relation
from src.responses import DBConnectionException, TableNotFoundException, DBExecutionException


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
            self.con.autocommit = True
            self.client = self.con.cursor()

        except Exception as e:
            raise DBConnectionException(str(db_parameters) + " : " + str(table.value.get_name())) from e
        self.table = table.value.get_name()

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
                f"table_name='{self.table}'",
            )
            val = self.client.fetchone()
            self.con.commit()
            return val[0] if val is not None else False
        except Exception as e:
            raise DBExecutionException('Is Table exist', f'{self.table} on {e}') from e

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
            raise TableNotFoundException(self.table)

        if len(fields) == 0:
            raise DBExecutionException('Retrieve', 'Query fields cannot be empty')

        field_str = ", ".join(fields)

        query = f'SELECT {field_str} FROM {self.table}'
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
            records = []
            if data is not None:
                for data_item in data:
                    record = {}
                    for index, field in enumerate(fields):
                        record[field] = data_item[index]
                    records.append(record)
            return records
        except Exception as e:
            raise DBExecutionException('Retrieve', f'{self.table} : {query} on {e}') from e

    def insert_record(self, data: dict) -> None:
        """
        Insert record into DB
        """
        fields = []
        values = []
        for field, value in data.items():
            fields.append(f"{field}")
            if isinstance(value, str):
                values.append(f"'{str(value)}'")
            else:
                values.append(str(value))
        statement = f"INSERT INTO {self.table} ({', '.join(fields)}) VALUES ({', '.join(values)})"
        try:
            self.client.execute(statement)
            self.con.commit()
        except Exception as e:
            raise DBExecutionException('Insert', f'{self.table} : {data} on {e}') from e
        if not self.client.rowcount == 1:
            raise DBExecutionException('Insert', f'{self.table} : {data} on no response')

    def update_record(self, r_id: str, data: dict) -> None:
        """
        Update record data by id into DB
        """
        data_list = []
        for field, value in data.items():
            if isinstance(value, str):
                value_temp = f"'{str(value)}'"
            else:
                value_temp = f"{str(value)}"
            data_list.append(f"'{field}'={value_temp}")

        statement = f"UPDATE {self.table} SET {' , '.join(data_list)} WHERE id = {r_id}"
        try:
            self.client.execute(statement)
            self.con.commit()
        except Exception as e:
            raise DBExecutionException('Update', f'{self.table} : {data} on {r_id} on {e}') from e
        if not self.client.rowcount == 1:
            raise DBExecutionException('Update', f'{self.table} : {data} on {r_id} on no response')
