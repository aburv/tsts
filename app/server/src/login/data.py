"""
User Login Data
"""
from src.config import Relation
from src.data import DataModel


class UserLoginData(DataModel):
    """
    Data User Login
    """

    def __init__(self):
        super().__init__(Relation.LOGIN, has_id=False, is_a_record=False)

    def on_data(self, data: dict):
        """
        Set up the data
        """
        self.set_data(data, True)

    def add_insert_fields(self):
        self.add_field('t_user', "userId", str, is_optional=False)
        self.add_field('device', "deviceId", str, is_optional=False)
        self.add_field('l_location', "locationId", str)
        self.add_field('ipv4', "ip", str, is_optional=False)

    def add_fields(self):
        return None
