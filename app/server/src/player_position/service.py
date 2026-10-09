"""
Player Service
"""
from src.db_duo import PostgresDbDuo
from src.player_position.data import PlayerPositionData, PlayerPositionFilterType


class PlayerPositionServices:
    """
    Service Player
    """

    def __init__(self):
        self._data = PlayerPositionData()
        self._db = PostgresDbDuo(self._data)

    def create_position(self, player_id: str, position_id: str, u_id: str) -> None:
        """
        Map player to position
        """
        self._data.on_data({"player": player_id, "position": position_id, "percent": 0})
        self._db.insert_record(u_id, player_id)

    def get_positions(self, player_id: str) -> list:
        """
        get position player
        """
        self._data.on_select({"player": player_id})
        records = self._db.get_records()
        positions = []
        for record in records:
            positions.append(record["p_position"])
        return positions

    def update_position_delta(self, player_id: str, position_id: str, delta: float, u_id: str) -> None:
        """
        Map player to position
        """
        self._data.on_data({"player": player_id, "position": position_id, "percent": delta},
                           PlayerPositionFilterType.POSITION)
        self._db.update_record(u_id, player_id)
