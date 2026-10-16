"""
Player Data
"""
from enum import Enum

from src.config import Relation
from src.data import DataModel, FilterMeta


class PlayerPositionFilterType(Enum):
    """
    Player Position Filter
    """
    POSITION = FilterMeta(
        querying_fields=["t_player", "p_position"],
        filtering_fields=["delta"]
    )
    DEFAULT = FilterMeta(
        querying_fields=["t_player"],
        filtering_fields=["p_position"]
    )


class PlayerPositionData(DataModel):
    """
    Data Player
    """

    def __init__(self):
        super().__init__(Relation.PLAYER_POSITION, has_id=False, is_a_record=False)

    def on_data(self, data: dict, filter_type: PlayerPositionFilterType = PlayerPositionFilterType.DEFAULT):
        """
        Set up the data
        """
        self._filter_type = filter_type
        self.set_data(data, filter_type == "")

    def add_insert_fields(self):
        self.add_field('t_player', "player", str, is_optional=False)
        self.add_field('p_position', "position", str, is_optional=False)
        self.add_field('delta', "percent", float, is_optional=False)

    def add_fields(self):
        self.add_field('t_player', "player", str)
        self.add_field('p_position', "position", str)
        self.add_field('delta', "percent", float)

    def on_select(self, data, filter_type: PlayerPositionFilterType = PlayerPositionFilterType.DEFAULT):
        """
        on Select operation
        """
        self._filter_type = filter_type
        self.set_data(data, is_new=False)
