"""
Location Data
"""
from enum import Enum

from src.config import Relation
from src.data import DataModel, FilterMeta


class LocationFilterType(Enum):
    """
    Location Filter Type
    """
    ID = FilterMeta(querying_fields=['id'], filtering_fields=['l_name', 'lat', 'long'], record_count=1)
    POINT = FilterMeta(querying_fields=['long', 'lat'], filtering_fields=['id'], record_count=1)
    DEFAULT = FilterMeta(
        querying_fields=['id'],
        filtering_fields=['l_name', 'locality', 'l_city', 'l_state', 'l_country', 'l_pin', 'lat', 'long'],
        record_count=1)


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
        self.add_field('long', "long", str)
        self.add_field('lat', "lat", str)

    def on_select(self, data: dict, _filter_type: LocationFilterType):
        """
        sets on select data
        """
        self.set_data(data, False)
        self._filter_type = _filter_type
