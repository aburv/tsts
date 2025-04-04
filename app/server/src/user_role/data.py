"""
User Role Data
"""
from src.config import Relation
from src.data import DataModel


class UserRoleData(DataModel):
    """
    Data User Role
    """

    def __init__(self):
        super().__init__(Relation.ROLE, has_id=False, is_a_record=False)

    def on_data(self, data: dict):
        """
        Set up the data
        """
        self.set_data(data, True)

    def add_insert_fields(self):
        self.add_field('user', "user", str, is_optional=False)
        self.add_field('record_id', "id", str, is_optional=False)
        self.add_field('permission', "permission", str, is_optional=False)

    def add_fields(self):
        return None

    def get_querying_fields(self) -> list:
        return ["user"]

    def get_filtering_fields(self):
        return ["record_id", "permission"]
