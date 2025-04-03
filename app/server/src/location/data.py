"""
Location Data
"""
from src.config import Relation
from src.data import DataModel


class LocationData(DataModel):
    """
    Data Location
    """

    def __init__(self):
        super().__init__(Relation.LOCATION)

    def on_data(self, data: dict):
        """
        Set up the data
        """
        self.set_data(data, True)

    def add_insert_fields(self):
        self.add_field('l_name', "name", str)
        self.add_field('locality', "locality", str)
        self.add_field('l_city', "city", str)
        self.add_field('l_state', "state", str)
        self.add_field('l_country', "country", str)
        self.add_field('l_pin', "pin", str)
        self.add_field('lat', "lat", str, is_optional=False)
        self.add_field('long', "long", str, is_optional=False)

    def add_fields(self):
        self.add_field('id', "id", str)

    def get_querying_fields(self) -> list:
        return ['id']

    def get_record_count(self) -> int | None:
        return 1

    def on_select(self, data: dict, _filter_type: str):
        """
        sets on select data
        """
        self.set_data(data, False)
        self._filter_type = _filter_type

    def get_filtering_fields(self) -> list:
        if self._filter_type == "s":
            return ['l_name', 'lat', 'long']
        return ['l_name', 'locality', 'l_city', 'l_state', 'l_country', 'l_pin', 'lat', 'long']
