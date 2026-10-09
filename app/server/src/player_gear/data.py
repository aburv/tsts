"""
Player Data
"""
from enum import Enum
from typing import Optional

from src.config import Relation
from src.data import DataModel, FilterMeta


class PlayerGearFilterType(Enum):
    """
    Player Gear Filter
    """
    SEARCH = FilterMeta(
        querying_fields=["p_jersey_name", "p_jersey_number"],
        filtering_fields=["t_player"]
    )
    ID = FilterMeta(
        querying_fields=["t_player"],
        filtering_fields=["p_jersey_name", "p_jersey_number", "p_jersey_size", "p_shoe_size"],
        record_count=1)


class PlayerGearData(DataModel):
    """
    Data Player
    """

    def __init__(self):
        super().__init__(Relation.T_PLAYER, has_id=False, is_a_record=False)

    def on_data(self, data: dict, filter_type: Optional[PlayerGearFilterType] = None):
        """
        Set up the data
        """
        self._filter_type = filter_type
        self.set_data(data, filter_type == "")

    def add_insert_fields(self):
        self.add_field('t_player', "player", str, is_optional=False)
        self.add_field('p_jersey_name', "jName", str, is_optional=False)
        self.add_field('p_jersey_number', "jNo", str, is_optional=False)
        self.add_field('p_jersey_size', "jSize", str, is_optional=False)
        self.add_field('p_shoe_size', "sSize", str, is_optional=False)

    def add_fields(self):
        self.add_field('t_player', "player", str)
        self.add_field('p_jersey_name', "jName", str)
        self.add_field('p_jersey_number', "jNo", str)
        self.add_field('p_jersey_size', "jSize", str)
        self.add_field('p_shoe_size', "sSize", str)

    def on_select(self, data: dict, filter_type: PlayerGearFilterType):
        """
        On Select operation
        """
        self._filter_type = filter_type
        self.set_data(data, is_new=False)

    def is_on_search(self) -> bool:
        """
        On Search operation
        """
        return self._filter_type == PlayerGearFilterType.SEARCH
