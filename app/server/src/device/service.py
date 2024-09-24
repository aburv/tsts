"""
Device Service
"""

from src.config import Relation
from src.db_duo import PostgresDbDuo
from src.device.data import DeviceData


class DeviceServices:
    """
    Service on Device
    """

    def __init__(self):
        self._db = PostgresDbDuo(Relation.DEVICE)

    def register_device(self, data: dict) -> str:
        """
        :return:
        :rtype:
        """
        device_data = DeviceData(data)
        devices = self._db.get_records(
            ["id"],
            {"device_id": device_data.get("device_id")},
            record_count=1
        )
        if len(devices) == 1:
            return devices[0]["id"]
        self._db.insert_record(device_data.get_insert_payload(), "")
        return device_data.get("id")
