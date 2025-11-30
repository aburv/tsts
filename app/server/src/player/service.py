"""
Player Service
"""
from datetime import date

from src.db_duo import PostgresDbDuo
from src.location.service import LocationServices
from src.option.service import OptionValueService
from src.player.data import PlayerData, PlayerFilterType
from src.player_position.service import PlayerPositionServices
from src.responses import RecordNotFoundException
from src.user.service import UserServices


class PlayerServices:
    """
    Service Player
    """

    def __init__(self):
        self._data = PlayerData()
        self._db = PostgresDbDuo(self._data)

    def create(self, data: dict, u_id: str) -> str:
        """
        Create and return player id
        """
        self._data.on_data(data)
        self._db.insert_record(u_id)
        player_id = self._data.get("id")
        UserServices().update_user({"id": u_id, "player": player_id}, u_id)
        return player_id

    def update(self, player_id: str, data: dict, u_id: str) -> None:
        """
        Create and return player id
        """
        data["id"] = player_id
        self._data.on_data(data, PlayerFilterType.ID)
        self._db.update_record(u_id, player_id)

    def get_user_data(self, player_id: str, u_id: str) -> str:  # pylint: disable=unused-argument
        """
        Get player user info
        """
        self._data.on_select({"id": player_id, "is_active": True}, PlayerFilterType.ID)
        records = self._db.get_records()
        if len(records) == 1:
            return records[0]
        raise RecordNotFoundException("Get PlayerUserData", player_id)

    def get_player_info(self, player_id: str) -> dict:
        """
        Get player user info
        """
        self._data.on_select({"id": player_id, "is_active": True}, PlayerFilterType.ID)
        records = self._db.get_records()
        if len(records) == 1:
            record = records[0]
            dp = UserServices().get_user_dp_by_player(player_id)
            position_ids = PlayerPositionServices().get_positions(player_id)
            ids = position_ids + [record["p_gender"]]
            option_data = OptionValueService().get_option_value_by_ids(ids)
            positions = []
            for position_id in position_ids:
                positions.append(option_data[position_id])
            age = date.today().year - record["p_birth"].year
            location_id = record["p_location"]
            location_str = ""
            if location_id is not None:
                location_data = LocationServices().get_location_by_id(location_id)
                location_str = f"{location_data['city']}, {location_data['state']}, {location_data['country']}"
            player = {
                "name": record["p_call_name"],
                "dp": dp,
                "location": location_str,
                "height": record["p_height"],
                "weight": record["p_weight"],
                "age": age,
                "gender": record["p_height"],
                "positions": positions
            }
            return player
        raise RecordNotFoundException("Get PlayerUserData", player_id)

    def search_by_name(self, text: str, u_id: str) -> list:  # pylint: disable=unused-argument
        """
        Get search by name
        """
        data = {
            "callName": text
        }
        self._data.on_select(data, PlayerFilterType.SEARCH)
        records = self._db.get_records()
        ids = []
        id_key = self._data.get_filtering_fields()[0]
        for record in records:
            ids.append(record[id_key])
        return ids
