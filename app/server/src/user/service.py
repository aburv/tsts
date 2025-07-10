"""
User Service
"""
from src.db_duo import PostgresDbDuo
from src.user.data import UserData
from src.user_id.service import UserIdServices
from src.user_role.service import UserRoleServices


class UserServices:
    """
    Service user
    """

    def __init__(self):
        self._data = UserData()
        self._db = PostgresDbDuo(self._data)

    def create_user(self, data: dict) -> str:
        """
        Create user and return id
        """
        self._data.on_data(data, True)
        u_id = self._data.get("id")
        self._db.insert_record(u_id)

        data["uId"].update({'user': u_id, "isVerified": True})
        UserIdServices().create_user_id(data["uId"], u_id)

        return u_id

    def update_user(self, data: dict, u_id: str) -> None:
        """
        Update user with data
        """
        self._data.on_data(data, False)
        self._db.update_record(u_id)

    def get_user_by_id(self, user_id: str) -> dict | None:
        """
        Get user by id
        """
        self._data.on_select({"id": user_id, "is_active": True}, "id")
        records = self._db.get_records()
        if len(records) > 0:
            return records[0]
        return None

    def get_user_data(self, u_id: str) -> dict:
        """
        :return:
        :rtype:
        """
        return {}

    def done_user_onboarding(self, u_id) -> str:
        """
        mark done on OnBoarding
        :return:
        :rtype:
        """
        UserRoleServices().assign_user_permission(
            {
                'user': u_id,
                'resource': "U",
                'record_id': u_id,
                'permission': "E"
            },
            u_id
        )

        return "t"
