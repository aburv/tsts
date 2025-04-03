import unittest
from unittest import mock
from unittest.mock import call

from src.config import Relation
from src.data import DataModel
from src.location.data import LocationData


class LocationDataTest(unittest.TestCase):

    @mock.patch.object(DataModel, '__init__', return_value=None)
    def test_should_init_location_data(self, mock_model):
        data = LocationData()

        mock_model.assert_called_once_with(Relation.LOCATION)
        self.assertIsInstance(data, LocationData)

    @mock.patch.object(DataModel, 'set_data')
    def test_should_call_set_location_data_on_data(self, mock_set):
        with mock.patch.object(LocationData, '__init__', return_value=None):
            data = LocationData()

        data.on_data({})

        mock_set.assert_called_once_with({}, True)

    @mock.patch.object(DataModel, 'add_field')
    def test_should_add_location_fields_on_add_insert_fields(self, mock_add_field):
        with mock.patch.object(LocationData, '__init__', return_value=None):
            LocationData().add_insert_fields()

        mock_add_field.assert_has_calls([
            call('l_name', 'name', str),
            call('locality', 'locality', str),
            call('l_city', 'city', str),
            call('l_state', 'state', str),
            call('l_country', 'country', str),
            call('l_pin', 'pin', str),
            call('lat', 'lat', str, is_optional=False),
            call('long', 'long', str, is_optional=False)
        ])

    def test_should_return_one_on_get_record_count(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            data = LocationData()

        actual = data.get_record_count()

        self.assertEqual(1, actual)

    def test_should_return_query_fields_on_get_querying_fields(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            data = LocationData()

        actual = data.get_querying_fields()

        self.assertEqual(['id'], actual)

    @mock.patch.object(DataModel, 'add_field', return_value=None)
    def test_should_return_none_on_add_fields(self, mock_add_field):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            data = LocationData()

        data.add_fields()

        mock_add_field.assert_has_calls([
            call('id', 'id', str)
        ])

    @mock.patch.object(DataModel, 'set_data')
    def test_should_set_data_to_select_on_select(self, mock_set):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            data = LocationData()

        data.on_select({}, "")

        mock_set.assert_called_once_with({}, False)
        self.assertEqual(data._filter_type, "")

    def test_should_return_short_fields_on_get_filtering_fields(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            image_data = LocationData()
            image_data._filter_type = 's'

        actual = image_data.get_filtering_fields()

        self.assertEqual(['l_name', 'lat', 'long'], actual)

    def test_should_return_long_fields_on_get_filtering_fields(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            image_data = LocationData()
            image_data._filter_type = None

        actual = image_data.get_filtering_fields()

        self.assertEqual(['l_name', 'locality', 'l_city', 'l_state', 'l_country', 'l_pin', 'lat', 'long'], actual)
