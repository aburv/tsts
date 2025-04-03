import unittest
from unittest import mock
from unittest.mock import call

from src.config import Relation
from src.data import DataModel
from src.device.data import DeviceData


class DeviceDataTest(unittest.TestCase):

    @mock.patch.object(DataModel, '__init__', return_value=None)
    def test_should_init_device_data(self, mock_data_model):
        DeviceData()

        mock_data_model.assert_called_once_with(Relation.DEVICE)

    @mock.patch.object(DataModel, 'add_field', return_value=None)
    def test_should_add_fields_on_add_insert_fields(self, mock_add_field):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            device_data = DeviceData()

        device_data.add_insert_fields()

        mock_add_field.assert_has_calls([
            call('device_id', 'deviceId', str, is_optional=False),
            call('other', 'other', str, is_optional=False),
            call('os', 'os', str, is_optional=False),
            call('os_version', 'version', str, is_optional=False),
            call('device_type', 'deviceType', str, data_list=["D", "P", "T"]),
            call('platform', 'platform', str, data_list=["A", "B"])
        ])

    @mock.patch.object(DataModel, 'add_field', return_value=None)
    def test_should_return_none_on_add_update_fields(self, mock_add_field):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            device_data = DeviceData()

        actual = device_data.add_fields()

        assert not mock_add_field.called
        self.assertIsNone(actual)

    @mock.patch.object(DataModel, 'set_data', return_value=None)
    def test_should_set_data_on_data(self, mock_set_data):
        data = {
            "deviceId": "id",
            "os": "Android",
            "version": "14",
            "other": "other",
            "deviceType": "Phone",
            "platform": "App"
        }
        with mock.patch.object(DataModel, '__init__', return_value=None):
            device_data = DeviceData()

        device_data.on_data(data)

        mock_set_data.assert_called_once_with(data, True)

    def test_should_return_one_on_get_record_count(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            device_data = DeviceData()

        actual = device_data.get_record_count()

        self.assertEqual(1, actual)

    def test_should_return_query_fields_on_get_querying_fields(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            device_data = DeviceData()

        actual = device_data.get_querying_fields()

        self.assertEqual(['device_id'], actual)

    def test_should_return_filter_fields_on_get_filtering_fields(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            device_data = DeviceData()

        actual = device_data.get_filtering_fields()

        self.assertEqual(['id'], actual)
