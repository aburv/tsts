"""
Device Data
"""

from src.data import Data, DataModel


class DeviceData(DataModel):
    """
    Data Device
    """
    TYPES = Data.get_device_types()
    PLATFORMS = Data.get_platforms()

    def __init__(self, data: dict):
        super().__init__(data)
        self.add_field('device_id', "deviceId", str, is_optional=False)
        self.add_field('other', "other", str, is_optional=False)
        self.add_field('os', "os", str, is_optional=False)
        self.add_field('os_version', "version", str, is_optional=False)
        self.add_field('device_type', "deviceType", str, data_list=DeviceData.TYPES)
        self.add_field('platform', "platform", str, data_list=DeviceData.PLATFORMS)
