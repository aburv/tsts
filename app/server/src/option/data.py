"""
Form Option Data
"""
from enum import Enum

from src.config import Relation
from src.data import DataModel, FilterMeta


class FormType(Enum):
    """
    Form types
    """
    PLAYER = "player"


class FormData(DataModel):
    """
    Data Form
    """

    def __init__(self):
        super().__init__(Relation.FORM_FIELD)

    def on_data(self, data: dict):
        """
        On Data
        """
        self.set_data(data, True)

    def add_insert_fields(self):
        self.add_field('form', "form", str, is_optional=False)
        self.add_field('field', "field", str, is_optional=False)

    def add_fields(self):
        return None


class FormOptionDataFilterType(Enum):
    """
    Option Data Filter Type
    """
    DEFAULT = FilterMeta(
        querying_fields=["a.form", "a.is_active", "b.is_active"],
        filtering_fields=["a.field", "b.id", "b.f_value"],
        grouping_fields=['a.field']
    )


class FormOptionData(DataModel):
    """
    Data Form Option
    """

    def __init__(self, form: FormType):
        super().__init__(Relation.OPTION)
        self._filter_type = FormOptionDataFilterType.DEFAULT
        self.set_data({"is_active": 'true', 'form': [form.value, 'general']}, False)

    def add_fields(self):
        self.add_field('b.is_active', "is_active", bool)
        self.add_field('a.is_active', "is_active", bool)
        self.add_field('a.form', "form", list)

    def add_insert_fields(self):
        return None


class OptionDataFilterType(Enum):
    """
    Option Data Filter
    """
    DEFAULT = FilterMeta(
        querying_fields=["id", "is_active"],
        filtering_fields=["id", "f_value"]
    )
    ID = FilterMeta(
        querying_fields=["id", "is_active"],
        filtering_fields=["id", "f_value"]
    )


class OptionData(DataModel):
    """
    Data Option
    """

    def __init__(self):
        super().__init__(Relation.OPTION_DATA)

    def on_data(self, data: dict):
        """
        On Data
        """
        self.set_data(data, True)

    def on_select(self, data: dict, filter_type: OptionDataFilterType = OptionDataFilterType.DEFAULT):
        """
        On Data
        """
        self._filter_type = filter_type
        self.set_data(data, False)

    def add_insert_fields(self):
        self.add_field('field_id', "fieldId", str, is_optional=False)
        self.add_field('f_value', "fValue", str, is_optional=False)

    def add_fields(self):
        self.add_field('id', "valueId", list)
        self.add_field('f_value', "fValue", str)
