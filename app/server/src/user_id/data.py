"""
User id Data
"""
from enum import Enum

from src.config import Relation
from src.data import DataModel, FilterMeta
from src.option_data import OptionData


class UserIDFilterType(Enum):
    """
    User id filter type
    """
    ID = FilterMeta(querying_fields=["val", "g_id", "is_verified"], filtering_fields=["t_user"], record_count=1)
    DEFAULT = FilterMeta(querying_fields=["t_user", "is_verified"], filtering_fields=["val", "type"], record_count=None)


class UserIDData(DataModel):
    """
    Data User id
    """
    TYPES = list(OptionData.get_id_types().keys())

    def __init__(self):
        super().__init__(Relation.UID, has_id=False, is_a_record=False)

    def on_data(self, data: dict):
        """
        Set up the data
        """
        self.set_data(data, True)

    def add_insert_fields(self):
        self.add_field('t_user', "user", str, is_optional=False)
        self.add_field('val', "value", str, is_optional=False)
        self.add_field('type', "type", str, is_optional=False, data_list=UserIDData.TYPES)
        self.add_field('g_id', "gId", str, is_optional=False)
        self.add_field('is_verified', "isVerified", bool, is_optional=False)

    def add_fields(self):
        self.add_field('t_user', "user", str)
        self.add_field('val', "value", str)
        self.add_field('g_id', "gId", str)
        self.add_field('is_verified', "isVerified", bool)

    def on_select(self, data: dict, f_type: UserIDFilterType = UserIDFilterType.DEFAULT):
        """
        Set up the data
        """
        self.set_data(data, False)
        self._filter_type = f_type
