import unittest
from unittest import mock

from src.db_duo import PostgresDbDuo
from src.location.data import LocationData
from src.location.service import LocationServices
from src.responses import RecordNotFoundException


class LocationServiceTest(unittest.TestCase):

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(LocationData, '__init__', return_value=None)
    def test_should_init_location_service(self,
                                          mock_data,
                                          mock_db):
        actual = LocationServices()

        mock_data.assert_called_once_with()
        mock_db.assert_called_once()
        args, _ = mock_db.call_args
        self.assertIsInstance(args[0], LocationData)
        self.assertIsInstance(actual, LocationServices)

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'insert_record', return_value=True)
    @mock.patch.object(LocationData, '__init__', return_value=None)
    def test_should_return_inserted_location_id_on_create_location(self,
                                                                   mock_location_data,
                                                                   mock_insert,
                                                                   mock_db):
        mock_location_data.get.side_effect = ["location_id"]
        with mock.patch.object(LocationServices, '__init__', return_value=None):
            service = LocationServices()
            service._data = mock_location_data
            service._db = mock_db
            mock_db.insert_record = mock_insert

        actual = service.create_location({}, "")

        mock_location_data.on_data.assert_called_once_with({})
        mock_location_data.get.assert_called_once_with('id')
        mock_insert.assert_called_once()
        mock_insert.assert_called_once_with("")

        self.assertEqual(actual, "location_id")

    @mock.patch.object(PostgresDbDuo, 'get_records')
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(LocationData, '__init__', return_value=None)
    def test_should_return_location_data_on_get_location_by_id(self,
                                                               mock_data,
                                                               mock_db,
                                                               mock_get_records):
        mock_get_records.return_value = [{"data": "location_data"}]

        with mock.patch.object(LocationServices, '__init__', return_value=None):
            service = LocationServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.get_records = mock_get_records

        actual = service.get_location_by_id("location_id")

        mock_get_records.assert_called_once_with()
        mock_data.on_select.assert_called_once_with({'id': 'location_id'}, 'id')

        self.assertEqual(actual, {"data": "location_data"})

    @mock.patch.object(RecordNotFoundException, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'get_records', return_value=[])
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(LocationData, '__init__', return_value=None)
    def test_should_raise_record_not_found_exception_when_no_data_from_db_on_get_location_by_id(self,
                                                                                                mock_data,
                                                                                                mock_db,
                                                                                                mock_get_records,
                                                                                                mock_exception):
        with mock.patch.object(LocationServices, '__init__', return_value=None):
            service = LocationServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.get_records = mock_get_records

        with self.assertRaises(RecordNotFoundException):
            service.get_location_by_id("location_id")

        mock_exception.assert_called_once_with('Location', 'location_id')
        mock_get_records.assert_called_once_with()
        mock_data.on_select.assert_called_once_with({'id': 'location_id'}, "id")

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(LocationData, '__init__', return_value=None)
    def test_should_return_location_id_on_get_location_id_by_long_lat(self,
                                                                      mock_data,
                                                                      mock_db):
        with mock.patch.object(LocationServices, '__init__', return_value=None):
            service = LocationServices()
            mock_db.get_record_field_value.return_value = "location_id"
            mock_data.get_filtering_fields.return_value = ["id"]
            service._db = mock_db
            service._data = mock_data

        actual = service.get_location_id_by_long_lat("long", "lat")

        mock_data.on_select.assert_called_once_with({'long': 'long', 'lat': 'lat'}, 'point')
        mock_db.get_record_field_value.assert_called_once_with()

        self.assertEqual(actual, "location_id")
