"""
Migrating script
"""
import json
import os

import psycopg2

from src.config import Config, Relation
from src.data import DataModel, OrderType
from src.db_duo import PostgresDbDuo
from src.logger import LoggerAPI
from src.option.data import OptionData, FormData
from src.responses import TableNotFoundException, DBConnectionException, DBExecutionException

RESOURCES_FOLDER = "resources"


def get_resources_path() -> str:
    """
    get resources path
    """
    current_path = os.path.dirname(os.path.abspath(""))

    return os.path.join(current_path, RESOURCES_FOLDER)


def get_ddl_files() -> list:
    """
    get all controller files
    """
    file_names = []
    for _, _, files in os.walk(get_resources_path()):
        for file in files:
            file_names.append(file)
    file_names.sort()
    return file_names


def get_json_from_file(file_path: str) -> dict:
    """
    Get Json from file
    """
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def get_version_from_name(file_name: str) -> str:
    """
    parse and get version
    :param file_name:
    :return:
    """
    return file_name.split("__")[0].replace("V", "")


class MigrateData(DataModel):
    """
    Data Migrate
    """

    def __init__(self):
        super().__init__(Relation.MIGRATION, has_id=False, is_a_record=False)

    def on_data(self, data: dict):
        """
        On Data
        """
        self.set_data(data, True)

    def add_insert_fields(self):
        self.add_field('version', "version", str, is_optional=False)

    def add_fields(self):
        return None

    def get_filtering_fields(self) -> list:
        return ["version"]

    def get_record_count(self) -> int | None:
        return 1

    def get_ordering_type(self) -> OrderType | None:
        return OrderType("date_time", True)


class Migrate: # pylint: disable=too-many-instance-attributes
    """
    Migrate class
    """

    def __init__(self) -> None:
        self.logger = LoggerAPI()
        self.param = Config.get_db_parameters()
        self._data = MigrateData()
        self.db = PostgresDbDuo(self._data)
        self._option_data = OptionData()
        self.option = PostgresDbDuo(self._option_data)
        self._form_data = FormData()
        self.form = PostgresDbDuo(self._form_data)
        self.init = PostgresDbDuo(DataModel(Relation.INIT))

    def run(self) -> None:
        """
        start function to run ddl files
        :return:
        :rtype:
        """
        path = get_resources_path()
        self.logger.info_entry('Migrating DB')
        system_db_version = self.get_version()
        self.logger.info_entry(f'Current Version: {system_db_version}')
        if system_db_version == "-1.00":
            self.create_schema(self.param["meta_schema"])
            self.create_schema(self.param["schema"])
        ddl_files = get_ddl_files()
        try:
            for ddl_file_name in ddl_files:
                version = get_version_from_name(ddl_file_name)
                file_name_path = str(os.path.join(path, ddl_file_name))
                if float(version) <= float(system_db_version):
                    self.logger.info_entry(
                        f'DDL command file already executed as fileV{version} {ddl_file_name} - '
                        f'systemDBVersion {system_db_version}'
                    )
                else:
                    if version.split(".")[1] == "00":
                        if version.split(".")[0] == "0":
                            self.logger.info_entry(
                                f'Executing Meta schema command file: {ddl_file_name}'
                            )
                            self.db.run_ddl_file(file_name_path)
                        else:
                            self.logger.info_entry(
                                f'Inserting Data from JSON file: {ddl_file_name}'
                            )
                            option_items = get_json_from_file(file_name_path)
                            self.add_option_items(option_items)
                    else:
                        self.logger.info_entry(
                            f'Executing DDL command file: {ddl_file_name}'
                        )
                        self.init.run_ddl_file(file_name_path)
                    self.update_version(version)
        except DBExecutionException as _:
            self.logger.error_entry('Migration stopped')
        except Exception as e:
            self.logger.error_entry(f'Migration stopped on {e}')
        self.logger.info_entry('Migration Done')

    def create_schema(self, schema: str) -> None:
        """
        Run ddl command directly
        """
        self.logger.info_entry(f'Creating Schema: {schema}')
        try:
            con = psycopg2.connect(
                host=self.param.get("host"),
                port=int(self.param.get("port")),
                database=self.param.get("db"),
                user=self.param.get("user"),
                password=self.param.get("pass")
            )
            con.autocommit = True
            client = con.cursor()
            client.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
            con.commit()
        except Exception as e:
            self.logger.error_entry(f'Create schema : {schema} {e}')

    def get_version(self) -> str:
        """
        get version
        :return:
        :rtype:
        """
        try:
            version_records = self.db.get_records()
            if len(version_records) == 1:
                return str(version_records[0]["version"])
            return "-1.00"
        except TableNotFoundException as _:
            return "-1.00"
        except DBExecutionException as _:
            return "-1.00"

    def update_version(self, version: str) -> None:
        """
        :return:
        :rtype:
        """
        try:
            self._data.on_data({"version": version})
            self.logger.info_entry(f'Updating migration version : {version}')
            self.db.insert_record("")
        except DBExecutionException as _:
            raise DBExecutionException('Update to version', version) from _

    def add_option_items(self, data: dict):
        """
        Inserting option into db
        """
        for form in data.keys():
            for form_field, values in data[form].items():
                self._form_data.on_data({'form': form, 'field': form_field})
                self.form.insert_record("")
                field_id = self._form_data.get("id")
                for value in values:
                    self._option_data.on_data({'fieldId': field_id, 'fValue': value})
                    self.option.insert_record("")


def run_migrate():
    """
    Run migration script
    """
    is_done = False  # pragma: no cover
    while not is_done:  # pragma: no cover
        try:  # pragma: no cover
            Migrate().run()  # pragma: no cover
            is_done = True  # pragma: no cover
        except DBConnectionException as _:  # pragma: no cover
            pass  # pragma: no cover
