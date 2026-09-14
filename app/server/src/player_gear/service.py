"""
Player Service
"""
from src.db_duo import PostgresDbDuo
from src.player_gear.data import PlayerGearData, PlayerGearFilterType
from src.responses import RecordNotFoundException


class PlayerGearServices:
    """
    Service Player
    """

    def __init__(self):
        self._data = PlayerGearData()
        self._db = PostgresDbDuo(self._data)

    def create(self, player_id: str, data: dict, u_id: str) -> None:
        """
        Create and return player id
        """
        data["player"] = player_id
        self._data.on_data(data)
        self._db.insert_record(u_id, player_id)

    def get_by_id(self, player_id: str) -> dict:
        """
        Get player by id
        """
        self._data.on_select({"player": player_id}, PlayerGearFilterType.ID)
        records = self._db.get_records()
        if len(records) == 1:
            return records[0]
        raise RecordNotFoundException("Get PlayerData", player_id)

    def update(self, player_id: str, data: dict, u_id: str) -> bool:
        """
        Update player id
        """
        data["player"] = player_id
        self._data.on_data(data, PlayerGearFilterType.ID)
        self._db.update_record(u_id, player_id)
        return True

    def check_presence(self, player_id) -> bool:
        """
        Check if player is present in db
        """
        try:
            self.get_by_id(player_id)
            return True
        except RecordNotFoundException as _:
            return False

    def search_by_j_name_j_no(self, text: str, _: str) -> list: # pylint: disable=unused-argument
        """
        Get ids by j_name, j_no
        """
        data = {
            "jName": text,
            "jNo": text
        }
        self._data.on_select(data, PlayerGearFilterType.SEARCH)
        records = self._db.get_records()
        ids = []
        for record in records:
            ids.append(record[self._data.get_filtering_fields()[0]])
        return ids
