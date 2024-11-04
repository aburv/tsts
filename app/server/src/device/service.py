"""
Device Service
"""

from src.db_duo import PostgresDbDuo
from src.device.data import DeviceData


class DeviceServices:
    """
    Service on Device
    """

    def __init__(self):
        self._data = DeviceData()
        self._db = PostgresDbDuo(self._data)

    def register_device(self, data: dict) -> str:
        """
        :return:
        :rtype:
        """
        self._data.on_data(data)
        devices = self._db.get_records()
        if len(devices) == 1:
            return devices[0][self._data.get_filtering_fields()[0]]
        self._db.insert_record("")
        return self._data.get("id")
