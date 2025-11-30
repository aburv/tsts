"""
Player Data
"""
from enum import Enum
from typing import Optional

from src.config import Relation
from src.data import DataModel, FilterMeta


class PlayerFilterType(Enum):
    """
    Player Filter Type
    """
    SEARCH = FilterMeta(
        querying_fields=["p_call_name"],
        filtering_fields=["id"]
    )
    ID = FilterMeta(
        querying_fields=["id", "is_active"],
        filtering_fields=[
            "p_call_name",
            "p_blood_group",
            "p_birth",
            "p_weight",
            "p_height",
            "p_location",
            "p_gender"
        ],
        record_count=1)
    DEFAULT = FilterMeta(
        querying_fields=[],
        filtering_fields=["p_call_name", "p_blood_group", "p_birth", "p_weight", "p_height", "p_location", "p_gender"])


class PlayerData(DataModel):
    """
    Data Player
    """

    def __init__(self):
        super().__init__(Relation.PLAYER)

    def on_data(self, data: dict, filter_type: Optional[PlayerFilterType] = None):
        """
        Set up the data
        """
        self._filter_type = filter_type
        self.set_data(data, filter_type is None)

    def add_insert_fields(self):
        self.add_field('p_call_name', "callName", str, is_optional=False)
        self.add_field('p_blood_group', "bloodGroup", str, is_optional=False)
        self.add_field('p_gender', "gender", str, is_optional=False)
        self.add_field('p_birth', "birthDate", str, is_optional=False, validate_type="date")
        self.add_field('p_weight', "weight", float, is_optional=False)
        self.add_field('p_height', "height", float, is_optional=False)
        self.add_field('p_location', "locationId", str)

    def add_fields(self):
        self.add_field('id', "id", str)
        self.add_field('p_call_name', "callName", str)
        self.add_field('p_blood_group', "bloodGroup", str)
        self.add_field('p_gender', "gender", str)
        self.add_field('p_birth', "birthDate", str)
        self.add_field('p_weight', "weight", float)
        self.add_field('p_height', "height", float)
        self.add_field('p_location', "locationId", str)
        self.add_field('is_active', "is_active", bool)

    def on_select(self, data: dict, filter_type: PlayerFilterType = PlayerFilterType.DEFAULT):
        """
        on Select operation
        """
        self._filter_type = filter_type
        self.set_data(data, is_new=False)

    def is_on_search(self) -> bool:
        """
        on Search operation
        """
        return self._filter_type == PlayerFilterType.SEARCH
