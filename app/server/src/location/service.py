"""
Location Service
"""
from src.db_duo import PostgresDbDuo
from src.location.data import LocationData
from src.responses import RecordNotFoundException


class LocationServices:
    """
    Service location
    """

    def __init__(self):
        self._data = LocationData()
        self._db = PostgresDbDuo(self._data)

    def create_location(self, data: dict, u_id: str) -> str:
        """
        Create location and return its id
        """
        self._data.on_data(data)
        self._db.insert_record(u_id)
        return self._data.get("id")

    def get_location_by_id(self, location_id: str) -> dict:
        """
        Get location by id
        """
        self._data.on_select({"id": location_id}, 's')
        data = self._db.get_records()
        if len(data) > 0:
            return data[0]
        raise RecordNotFoundException("Location", location_id)
