"""
User Data
"""
from enum import Enum
from typing import Union

from src.config import Relation
from src.data import DataModel, FilterMeta


class UserFilterType(Enum):
    """
    User Filter Type
    """
    ID = FilterMeta(
        querying_fields=["id", "is_active"],
        filtering_fields=["u_name", "dp"],
        record_count=1
    )
    DEFAULT = FilterMeta(
        querying_fields=[],
        filtering_fields=[]
    )
    PLAYERS = FilterMeta(
        querying_fields=["player", "is_active"],
        filtering_fields=["player", "u_name", "dp"],
    )
    PLAYER_DP = FilterMeta(
        querying_fields=["player", "is_active"],
        filtering_fields=["dp"],
    )
    PLAYER_ID = FilterMeta(
        querying_fields=["id", "is_active"],
        filtering_fields=["player"],
        record_count=1
    )


class UserData(DataModel):
    """
    Data User
    """

    def __init__(self):
        super().__init__(Relation.USER)
        self.filter_type = UserFilterType.DEFAULT

    def on_data(self, data: dict, is_inserting: bool):
        """
        Set up the data
        """
        if not is_inserting:
            self._filter_type = UserFilterType.ID
        self.set_data(data, is_inserting)

    def on_select(self, data: dict, filter_type: UserFilterType):
        """
        Set up the data
        """
        self.set_data(data, False)
        self._filter_type = filter_type

    def add_insert_fields(self):
        self.add_field('u_name', "name", str, is_optional=False)
        self.add_field('dp', "dp", str)

    def add_fields(self):
        self.add_field('id', "id", str)
        self.add_field('u_name', "name", str)
        self.add_field('dp', "dp", str)
        self.add_field('player', "player", Union[str, list])
