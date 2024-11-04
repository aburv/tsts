"""
Device Data
"""
from src.config import Relation
from src.data import DataModel
from src.option_data import OptionData


class DeviceData(DataModel):
    """
    Data Device
    """
    TYPES = OptionData.get_device_types()
    PLATFORMS = OptionData.get_platforms()

    def __init__(self):
        super().__init__(Relation.DEVICE)

    def on_data(self, data: dict):
        """
        Set up the data
        """
        self.set_data(data, True)

    def add_insert_fields(self):
        self.add_field('device_id', "deviceId", str, is_optional=False)
        self.add_field('other', "other", str, is_optional=False)
        self.add_field('os', "os", str, is_optional=False)
        self.add_field('os_version', "version", str, is_optional=False)
        self.add_field('device_type', "deviceType", str, data_list=DeviceData.TYPES)
        self.add_field('platform', "platform", str, data_list=DeviceData.PLATFORMS)

    def add_fields(self):
        return None

    def get_record_count(self) -> int | None:
        return 1

    def get_filtering_fields(self) -> list:
        """
        Subset of Fields to be retrieved from db
        """
        return ['id']

    def get_querying_fields(self) -> list:
        return ['device_id']
