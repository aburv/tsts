import unittest
from unittest import mock

from src.db_duo import PostgresDbDuo
from src.device.data import DeviceData
from src.device.service import DeviceServices


class DeviceServiceTest(unittest.TestCase):

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(DeviceData, '__init__', return_value=None)
    def test_should__init_device_service(self,
                                         mock_data,
                                         mock_db):
        actual = DeviceServices()

        mock_data.assert_called_once_with()
        mock_db.assert_called_once()
        args, _ = mock_db.call_args
        self.assertIsInstance(args[0], DeviceData)
        self.assertTrue(isinstance(actual, DeviceServices))

    @mock.patch.object(PostgresDbDuo, 'get_records', return_value=[])
    @mock.patch.object(PostgresDbDuo, 'insert_record', return_value=True)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(DeviceData, '__init__', return_value=None)
    def test_should_return_inserted_device_id_on_register_device(self,
                                                                 mock_data,
                                                                 mock_db,
                                                                 mock_insert,
                                                                 mock_get_records):
        mock_data.get.side_effect = ["app_device_id"]
        with mock.patch.object(DeviceServices, '__init__', return_value=None):
            service = DeviceServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.insert_record = mock_insert
            mock_db.get_records = mock_get_records

        actual = service.register_device({})

        mock_data.on_data.assert_called_once_with({})
        mock_get_records.assert_called_once_with()
        assert not mock_data.get_filtering_fields.called

        mock_insert.assert_called_once_with('')
        mock_data.get.assert_called_once_with('id')

        self.assertEqual(actual, "app_device_id")

    @mock.patch.object(PostgresDbDuo, 'get_records', return_value=[{"id": "app_device_id"}])
    @mock.patch.object(PostgresDbDuo, 'insert_record', return_value=True)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(DeviceData, '__init__', return_value=None)
    def test_should_return_existing_device_id_on_register_device(self,
                                                                 mock_data,
                                                                 mock_db,
                                                                 mock_insert,
                                                                 mock_get_records):
        mock_data.get_filtering_fields.return_value = ['id']
        with mock.patch.object(DeviceServices, '__init__', return_value=None):
            service = DeviceServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.insert_record = mock_insert
            mock_db.get_records = mock_get_records

        actual = service.register_device({})

        mock_data.on_data.assert_called_once_with({})
        mock_get_records.assert_called_once_with()
        mock_data.get_filtering_fields.assert_called_once_with()

        assert not mock_insert.called
        assert not mock_data.get.called

        self.assertEqual(actual, "app_device_id")
