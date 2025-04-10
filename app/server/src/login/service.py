"""
User Service
"""

from src.config import Config
from src.db_duo import PostgresDbDuo
from src.image.service import ImageServices
from src.location.service import LocationServices
from src.login.data import UserLoginData
from src.responses import DataValidationException, RecordNotFoundException
from src.services.auth_service import AuthServices
from src.user.service import UserServices
from src.user_id.service import UserIdServices


class LoginServices:
    """
    Service user
    """

    def __init__(self):
        self._data = UserLoginData()
        self._db = PostgresDbDuo(self._data)

    def login(self, user_data: dict, login_data: dict) -> dict:
        """
        Login user with id
        """

        user_id_dict = user_data.get("uId", {})
        if not user_id_dict:
            raise DataValidationException("Login", "No Id data")
        user_id_value = user_id_dict.get("value", "")
        if user_id_value == "":
            raise DataValidationException("Login", "No Id value")

        u_id = UserIdServices().get_user_id_by_id_value(user_id_value)

        if u_id is None:
            u_id = UserServices().create_user(user_data)
            pic_url = user_data.get("picUrl", "")
            if pic_url != "" and user_data.get("dp", "") == "":
                i_id = ImageServices().load_and_save(pic_url, u_id)
                UserServices().update_user({"id": u_id, "dp": i_id}, u_id)
        else:
            user = UserServices().get_user_by_id(u_id)
            if not user:
                raise RecordNotFoundException("User", u_id)

        login_data.update({'userId': u_id})
        location_data = login_data.get("location", {})
        if location_data:
            try:
                long = location_data["long"]
                lat = location_data["lat"]
            except KeyError as e:
                raise DataValidationException("Get Location", f"Necessary fields not present: {e}") from e
            l_id = LocationServices().get_location_id_by_long_lat(long, lat)
            if l_id is None:
                l_id = LocationServices().create_location(location_data, u_id)
            login_data.update({'locationId': l_id})
        self._data.on_data(login_data)
        self._db.insert_record(u_id, u_id)

        tokens = AuthServices().login(u_id)

        return {
            "idToken": tokens[0],
            "accessToken": tokens[1]
        }

    @staticmethod
    def refresh(token: str) -> dict:
        """
        Refresh token on existing token
        """
        try:
            id_token, access_token = Config.get_tokens(token)

        except DataValidationException:
            return {}

        tokens = AuthServices().refresh_token(id_token, access_token)

        return {
            "idToken": tokens[0],
            "accessToken": tokens[1]
        }
