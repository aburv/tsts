import unittest
from unittest import mock
from unittest.mock import call

from src.db_duo import PostgresDbDuo
from src.option.data import FormOptionData, FormType, OptionData, OptionDataFilterType
from src.option.service import OptionService, OptionValueService


class FormOptionServiceTest(unittest.TestCase):

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(FormOptionData, '__init__', return_value=None)
    def test_should_init_form_field_options_service(self,
                                                    mock_data,
                                                    mock_db):
        actual = OptionService(FormType.PLAYER)

        mock_data.assert_called_once_with(FormType.PLAYER)
        mock_db.assert_called_once()
        args, _ = mock_db.call_args
        self.assertIsInstance(args[0], FormOptionData)
        self.assertIsInstance(actual, OptionService)

    @mock.patch.object(PostgresDbDuo, 'get_records')
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(FormOptionData, '__init__', return_value=None)
    @mock.patch.object(OptionService, 'get_field_key')
    def test_should_return_form_field_options_on_get_options_by_id(self,
                                                                   mock_get_field_key,
                                                                   mock_data,
                                                                   mock_db,
                                                                   mock_get_records):
        mock_get_records.return_value = [
            {
                "a.field": "color",
                "b.id": 1,
                "b.f_value": "red"
            },
            {
                "a.field": "color",
                "b.id": 2,
                "b.f_value": "blue"
            },
            {
                "a.field": "shape_s",
                "b.id": 3,
                "b.f_value": "rectangle"
            },
            {
                "a.field": "shape",
                "b.id": 4,
                "b.f_value": "square"
            },
            {
                "a.field": "shape",
                "b.id": 5,
                "b.f_value": "circle"
            }
        ]
        mock_get_field_key.side_effect = ['color', 'color', 'shapeS', 'shape', 'shape']

        with mock.patch.object(OptionService, '__init__', return_value=None):
            service = OptionService(FormType.PLAYER)
            service._db = mock_db
            service._data = mock_data
            mock_db.get_records = mock_get_records

        actual = service.get_options()

        mock_get_records.assert_called_with()
        mock_get_field_key.assert_has_calls([
            call('color'),
            call('color'),
            call('shape_s'),
            call('shape'),
            call('shape')
        ])

        self.assertEqual(actual, {'color': [{'id': 1, 'value': 'red'}, {'id': 2, 'value': 'blue'}],
                                  'shapeS': [{'id': 3, 'value': 'rectangle'}],
                                  'shape': [{'id': 4, 'value': 'square'},
                                            {'id': 5, 'value': 'circle'}]})

    def test_should_return_camelCased_str_on_get_field_key(self):
        with mock.patch.object(OptionService, '__init__', return_value=None):
            service = OptionService(FormType.PLAYER)

        actual = service.get_field_key('a_field')

        self.assertEqual(actual, 'aField')

    def test_should_return_lowercased_str_on_get_field_key(self):
        with mock.patch.object(OptionService, '__init__', return_value=None):
            service = OptionService(FormType.PLAYER)

        actual = service.get_field_key('Field')

        self.assertEqual(actual, 'field')


class OptionValueServiceTest(unittest.TestCase):

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(OptionData, '__init__', return_value=None)
    def test_should_init_option_value_option_value_service(self,
                                                           mock_data,
                                                           mock_db):
        actual = OptionValueService()

        mock_data.assert_called_once_with()
        mock_db.assert_called_once()
        args, _ = mock_db.call_args
        self.assertIsInstance(args[0], OptionData)
        self.assertIsInstance(actual, OptionValueService)

    @mock.patch.object(PostgresDbDuo, 'get_records')
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(OptionData, '__init__', return_value=None)
    def test_should_return_value_on_get_option_value_by_ids(self,
                                                            mock_data,
                                                            mock_db,
                                                            mock_get_records):
        mock_get_records.return_value = [{"id": "id1", "f_value": "val1"}, {"id": "id2", "f_value": "val2"}]
        with mock.patch.object(OptionService, '__init__', return_value=None):
            service = OptionValueService()
            service._db = mock_db
            service._data = mock_data
            mock_db.get_records = mock_get_records

        actual = service.get_option_value_by_ids(["id1", "id2"])

        mock_get_records.assert_called_once_with()
        mock_data.on_select.assert_called_once_with({'valueId': ['id1', 'id2']}, OptionDataFilterType.ID)
        self.assertEqual(actual, {'id1': 'val1', 'id2': 'val2'})
