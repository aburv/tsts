import unittest
from unittest import mock
from unittest.mock import call

from src.data import DataModel
from src.device.data import DeviceData


class DeviceDataTest(unittest.TestCase):

    @mock.patch.object(DataModel, 'add_field')
    @mock.patch.object(DataModel, '__init__', return_value=None)
    def test_should_init_device_data(self, mock_data_model, mock_add_field):
        data = {
            "deviceId": "id",
            "os": "Android",
            "version": "14",
            "other": "other",
            "deviceType": "Phone",
            "platform": "App"
        }

        DeviceData(data)

        mock_data_model.assert_called_once_with(data)
        mock_add_field.assert_has_calls([
            call('device_id', 'deviceId', str, is_optional=False),
            call('other', 'other', str, is_optional=False),
            call('os', 'os', str, is_optional=False),
            call('os_version', 'version', str, is_optional=False),
            call('device_type', 'deviceType', str, data_list=["Desktop", "Phone", "Tab"]),
            call('platform', 'platform', str, data_list=["App", "browsers"])
        ])
