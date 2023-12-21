"""
 PostgresDB class
"""
from typing import Any

import psycopg2

from src.config import Config
from src.responses import DBConnectionException, SchemaNotFoundException


class OrderType:
    is_desc: bool
    field: str

    def __init__(self, field: str, is_desc: bool):
        self.is_desc = is_desc
        self.field = field


class PostgresDbDuo:
    """
    db api to the services
    """

    def __init__(self, table_name: str) -> None:
        db_parameters = Config.get_db_parameters()
        try:
            self.con = psycopg2.connect(host=db_parameters.get("host"),
                                        port=int(db_parameters.get("port")),
                                        database=db_parameters.get("db"),
                                        user=db_parameters.get("user"),
                                        password=db_parameters.get("pass"))
            self.con.autocommit = True
            self.client = self.con.cursor()

        except Exception as e:
            print(str(e))
            raise DBConnectionException(str(db_parameters))
        self.table = table_name
        self.schema = db_parameters.get("schema")

    def run_ddl(self, file_path) -> None:
        self.client.execute(open(file_path, "r").read())
        self.con.commit()
        if not self.client.rownumber > 0:
            print("Not able to complete the ddl command")

    def is_table_exist(self) -> bool:
        try:
            self.client.execute(
                'SELECT * FROM information_schema.tables WHERE table_name=%s and table_schema=%s',
                (self.table, self.schema))
            val = self.client.fetchone()
            return val[0] if val is not None else False
        except Exception as e:
            print("Not able to execute listing tables : " + str(e))
            return False

    def get_records(self,
                    query_param: dict | None,
                    fields: list,
                    order_type: OrderType | None
                    ) -> tuple[Any, ...]:

        if not self.is_table_exist():
            raise SchemaNotFoundException(self.table)

        query = 'SELECT %s FROM %s'
        if query_param is not None:
            query += ' WHERE '
            query_list = []
            for (field, value) in query_param.items():
                query_list.append(field + '=' + value)
            query += " AND ".join(query_list)
        if order_type is not None:
            query += ' ORDER BY %s ' + 'DESC' if order_type.is_desc else 'ASC'

        field_str = ", ".join(fields) if len(fields) != 0 else '*'

        try:
            self.client.execute(query, (field_str, self.schema + "." + self.table, order_type.field,), )
            data = self.client.fetchone()
            self.con.commit()
            return data[0]
        except Exception as e:
            print("" + str(e))

    def insert_record(self, data: dict):
        fields = []
        values = []
        for field, value in data.items():
            fields.append(field)
            values.append(value)

        try:
            self.client.execute('INSERT INTO %s (%s) values (%s)',
                                (self.schema + "." + self.table, ", ".join(fields), ", ".join(values),))
            self.con.commit()
        except Exception as e:
            print("" + str(e))
            return
        if not self.client.rowcount == 1:
            print("not inserted")
