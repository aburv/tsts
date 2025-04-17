"""
User Data
"""
from src.config import Relation
from src.data import DataModel


class UserData(DataModel):
    """
    Data User
    """

    def __init__(self):
        super().__init__(Relation.USER)

    def on_data(self, data: dict, is_inserting: bool):
        """
        Set up the data
        """
        self.set_data(data, is_inserting)

    def on_select(self, data: dict, filter_type: str):
        """
        Set up the data
        """
        self.set_data(data, False)
        self._filter_type = filter_type

    def add_insert_fields(self):
        self.add_field('u_name', "name", str, is_optional=False)
        self.add_field('dp', "dp", str)

    def add_fields(self):
        self._filter_type = "id"
        self.add_field('id', "id", str)
        self.add_field('u_name', "name", str)
        self.add_field('dp', "dp", str)

    def get_record_count(self) -> int | None:
        if self._filter_type == "id":
            return 1
        return None

    def get_querying_fields(self) -> list:
        if self._filter_type == "id":
            return ["id", "is_active"]
        return []

    def get_filtering_fields(self) -> list:
        if self._filter_type == "id":
            return ["u_name", "dp"]
        return []
