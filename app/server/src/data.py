"""
Data file
"""
import uuid

from src.responses import DataValidationException


class Data:
    """
    Data
    """

    @staticmethod
    def get_platforms() -> list:
        """
        :return: platforms
        :rtype: list
        """
        return ["App", "browsers"]

    @staticmethod
    def get_device_types() -> list:
        """
        :return: Device types
        :rtype: list
        """
        return ["Desktop", "Phone", "Tab"]


class DataModel:
    """
    Data Model
    """
    _data: dict
    _fields: dict

    def __init__(self, data):
        self._data = data
        self._fields = {}

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

    def get_insert_payload(self) -> dict:
        """
        :return: payload
        :rtype: dict
        """
        self._fields.update({
            'id': str(uuid.uuid4()),
            'is_active': True
        })
        return self._fields

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
