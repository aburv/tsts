"""
User Id Service
"""
from src.db_duo import PostgresDbDuo
from src.user_id.data import UserIDData


class UserIdServices:
    """
    Service user id
    """

    def __init__(self):
        self._data = UserIDData()
        self._db = PostgresDbDuo(self._data)

    def create_user_id(self, data: dict, u_id: str) -> None:
        """
        Create user id
        """
        self._data.on_data(data)
        self._db.insert_record(u_id, data["user"])

    def get_user_ids_by_user(self, user_id: str) -> list:
        """
        Get user ids value by user id
        """
        self._data.on_select({"user": user_id, "is_verified": True})
        return self._db.get_records()

    def get_user_id_by_id_value(self, id_value: str) -> str | None:
        """
        Get user id by id value
        """
        self._data.on_select({"value": id_value, "is_verified": True}, "id")
        return self._db.get_record_field_value()
