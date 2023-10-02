"""
Migrating script
"""
import os

from src.db_duo import PostgresDbDuo, OrderType
from src.responses import SchemaNotFoundException, DBConnectionException

project_path = "../resources"


def get_ddl_files():
    """
    get all controller files
    """
    file_names = []
    for root, _, files in os.walk(project_path):
        for file in files:
            file_names.append(file)
    file_names.sort()
    return file_names


def get_version_from_name(file_name: str) -> float:
    """
    parse and get version
    :param file_name:
    :return:
    """
    return float(file_name.split("__")[0].replace("V", "")).__round__(2)


class Migrate:
    """
    Migrate class
    """

    def __init__(self):
        try:
            self.db = PostgresDbDuo("migrate")
        except DBConnectionException as e:
            print('Unable to connect: ' + str(e))

    def run(self):
        """
        start function to run ddl files
        :return:
        :rtype:
        """
        print("Migrating DB ")
        ddl_files = get_ddl_files()
        system_db_version = self.get_version()
        try:
            for ddl_file_name in ddl_files:
                version = get_version_from_name(ddl_file_name)
                if version > system_db_version:
                    file_name_path = str(os.path.join(project_path, ddl_file_name))
                    self.db.run_ddl(file_name_path)
                    if not self.update_version(version):
                        print(f"Not able to update version: ${version}")
                        break
        except Exception as e:
            print('Unable to perform: ' + str(e))

    def get_version(self) -> float:
        """
        get version
        :return:
        :rtype:
        """
        try:
            order_type = OrderType("date_time", True)
            version = self.db.get_records(
                None,
                ["version"],
                order_type
            )
            return float(version[0])
        except SchemaNotFoundException as _:
            return 0.00
        except Exception as e:
            print("Not able to execute get latest version: " + str(e))
            return 100.0

    def update_version(self, version) -> bool:
        """
        :return:
        :rtype:
        """
        return self.db.insert_record({"version": version})
