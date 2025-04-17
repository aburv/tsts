"""
Data file
"""
import uuid

from src.config import Relation, Table
from src.responses import DataValidationException


class OrderType:
    """
    Order type
    """
    is_desc: bool
    field: str

    def __init__(self, field: str, is_desc: bool):
        self.is_desc = is_desc
        self.field = field


class DataModel:
    """
    Data Model
    """
    table: Table
    _data: dict
    _fields: dict
    _has_id: bool
    _is_a_record: bool

    _filter_type: str

    def __init__(self, relation: Relation, has_id: bool = True, is_a_record: bool = True):
        self.table = relation.value
        self._fields = {}
        self._has_id = has_id
        self._is_a_record = is_a_record

    def get(self, field_name):
        """
        get value by key
        :return: field value
        :rtype:
        """
        try:
            return self._fields[field_name]
        except KeyError as e:
            raise DataValidationException("Unable to find", field_name) from e

    def set_data(self, data: dict, is_new: bool):
        """
        Set data
        """
        self._data = data
        if is_new:
            if self._has_id:
                self._fields.update({
                    'id': str(uuid.uuid4()),
                })
            if self._is_a_record:
                self._fields.update({
                    'is_active': True
                })
            self.add_insert_fields()
        else:
            self.add_fields()

    def add_insert_fields(self):
        """
        Add Update fields
        """
        raise NotImplementedError()

    def add_fields(self):
        """
        Add Update fields
        """
        raise NotImplementedError()

    def get_querying_fields(self) -> list:
        """
        Subset of Fields to be querying from db
        """
        return []

    def get_querying_fields_and_value(self) -> dict | None:
        """
        =Fields and its value to be querying from db
        """
        query_fields = self.get_querying_fields()
        if not query_fields:
            return None
        return {key: val for key, val in self._fields.items() if key in query_fields}

    def get_filtering_fields(self) -> list:
        """
        Subset of Fields to be retrieved from db
        """
        return []

    def get_grouping_field(self) -> dict | None:
        """
        Subset of Fields to get group by
        """
        return None

    def get_ordering_type(self) -> OrderType | None:
        """
        Subset of Fields to get group by
        """
        return None

    def get_table_name(self):
        """
        Table name
        """
        return self.table.get_name()

    def get_record_count(self) -> int | None:
        """
        No of records to retrieve
        """
        return None

    def frame_records(self, data: tuple):
        """
        Framing the records
        """
        fields = self.get_filtering_fields()
        records = []
        if data is not None:
            for data_item in data:
                record = {}
                for index, field in enumerate(fields):
                    record[field] = data_item[index]
                records.append(record)
        return records

    def add_field(
            self,
            name: str,
            key: str,
            f_type: type,
            is_optional: bool = True,
            data_list: list | None = None
    ):
        """
        add the field to data
        """
        try:
            value = self._data[key]
            if isinstance(value, f_type):
                if (data_list is not None and value in data_list) or (
                        data_list is None and value != ""):
                    self._fields.update({name: value})
                    return
            raise DataValidationException("Improper data values", f" {self._data} {name} {value}")
        except KeyError as e:
            if not is_optional:
                raise DataValidationException("Necessary field not present", f"{self._data} {name}") from e

    def is_empty(self) -> bool:
        """
        checks for emptiness
        :return:
        :rtype: bool
        """
        return len(self._fields.items()) == 0

    def get_audit_payload(self) -> dict:
        """
        Get Audit payload
        """
        return {key: val for key, val in self._fields.items() if key != 'id'}

    def get_values(self) -> list:
        """
        Fields keys
        """
        return list(self._fields.values())

    def get_fields(self) -> list:
        """
        Fields keys
        """
        return list(self._fields.keys())
