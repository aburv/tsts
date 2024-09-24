import unittest
from unittest import mock
from unittest.mock import call

from src.config import Relation
from src.db_duo import PostgresDbDuo
from src.device.data import DeviceData
from src.device.service import DeviceServices


class DeviceServiceTest(unittest.TestCase):

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    def test_should__init_device_service(self,
                                         mock_db):
        actual = DeviceServices()

        mock_db.assert_called_once_with(Relation.DEVICE)
        self.assertTrue(isinstance(actual, DeviceServices))

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'get_records', return_value=[])
    @mock.patch.object(PostgresDbDuo, 'insert_record', return_value=True)
    @mock.patch.object(DeviceData, '__init__', return_value=None)
    @mock.patch.object(DeviceData, 'get')
    @mock.patch.object(DeviceData, 'get_insert_payload', return_value={'device_id': 'device_id', 'id': 'app_device_id'})
    def test_should_return_inserted_device_id_on_register_device(self,
                                                                 mock_get_insert_payload,
                                                                 mock_get_data,
                                                                 mock_device_data,
                                                                 mock_insert,
                                                                 mock_get_records,
                                                                 mock_db):
        mock_get_data.side_effect = [
            "device_id",
            "app_device_id"
        ]
        with mock.patch.object(DeviceServices, '__init__', return_value=None):
            service = DeviceServices()
            service._db = mock_db
            mock_db.insert_record = mock_insert
            mock_db.get_records = mock_get_records

        actual = service.register_device({})

        mock_device_data.assert_called_once_with({})
        mock_get_data.assert_has_calls([call('device_id'), call('id')])
        mock_get_records.assert_called_once_with(['id'], {'device_id': 'device_id'}, record_count=1)
        mock_get_insert_payload.assert_called_once_with()
        mock_insert.assert_called_once_with({'device_id': 'device_id', 'id': 'app_device_id'}, '')

        self.assertEqual(actual, "app_device_id")

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'get_records', return_value=[{"id": "app_device_id"}])
    @mock.patch.object(PostgresDbDuo, 'insert_record', return_value=True)
    @mock.patch.object(DeviceData, '__init__', return_value=None)
    @mock.patch.object(DeviceData, 'get', return_value="device_id")
    def test_should_return_existing_device_id_on_register_device(self,
                                                                 mock_get_data,
                                                                 mock_device_data,
                                                                 mock_insert,
                                                                 mock_get_records,
                                                                 mock_db):
        with mock.patch.object(DeviceServices, '__init__', return_value=None):
            service = DeviceServices()
            service._db = mock_db
            mock_db.insert_record = mock_insert
            mock_db.get_records = mock_get_records

        actual = service.register_device({})

        mock_device_data.assert_called_once_with({})
        mock_get_data.assert_called_once_with('device_id')
        mock_get_records.assert_called_once_with(['id'], {'device_id': 'device_id'}, record_count=1)
        mock_insert.assert_not_called()

        self.assertEqual(actual, "app_device_id")
