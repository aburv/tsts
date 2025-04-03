"""
User Role Service
"""
from src.db_duo import PostgresDbDuo
from src.user_role.data import UserRoleData


class UserRoleServices:
    """
    Service user role
    """

    def __init__(self):
        self._data = UserRoleData()
        self._db = PostgresDbDuo(self._data)

    def assign_user_permission(self, data: dict, u_id: str) -> None:
        """
        Assign user with record with permission
        """
        self._data.on_data(data)
        self._db.insert_record(u_id)

    def get_user_permission(self, u_id: str) -> list:
        """
        Get user record permissions
        """
        self._data.on_data({'user': u_id})
        return self._db.get_records()
