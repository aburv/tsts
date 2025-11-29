import unittest
from unittest import mock
from unittest.mock import call

from src.config import Relation
from src.data import DataModel
from src.option.data import OptionData, FormOptionData, FormData, FormType, OptionDataFilterType, \
    FormOptionDataFilterType


class OptionDataTest(unittest.TestCase):
    @mock.patch.object(DataModel, '__init__', return_value=None)
    def test_should_init_option_data(self, mock_data_model):
        OptionData()

        mock_data_model.assert_called_once_with(Relation.OPTION_DATA)

    @mock.patch.object(DataModel, 'add_field', return_value=None)
    def test_should_option_add_fields_on_add_insert_fields(self, mock_add_field):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            option_data = OptionData()

        option_data.add_insert_fields()

        mock_add_field.assert_has_calls([
            call('field_id', 'fieldId', str, is_optional=False),
            call('f_value', 'fValue', str, is_optional=False)
        ])

    @mock.patch.object(DataModel, 'set_data', return_value=None)
    def test_should_set_data_on_data(self, mock_set_data):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            option_data = OptionData()

        option_data.on_data({"form": "form_value"})

        mock_set_data.assert_called_once_with({"form": "form_value"}, True)

    @mock.patch.object(DataModel, 'set_data', return_value=None)
    def test_should_set_data_on_select(self, mock_set_data):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            form_data = OptionData()

        form_data.on_select({"form_field": "field_value"}, OptionDataFilterType.ID)

        mock_set_data.assert_called_once_with({"form_field": "field_value"}, False)
        self.assertEqual(form_data._filter_type, OptionDataFilterType.ID)

    @mock.patch.object(DataModel, 'add_field', return_value=None)
    def test_should_return_none_on_add_fields(self, mock_add_fields):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            option_data = OptionData()

        option_data.add_fields()

        mock_add_fields.assert_has_calls([
            call('id', 'valueId', list),
            call('f_value', 'fValue', str),
        ])

    def test_should_return_fields_on_get_querying_fields(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            option_data = OptionData()
            option_data._filter_type = OptionDataFilterType.DEFAULT

        actual = option_data.get_querying_fields()

        self.assertEqual(actual, ['id', 'is_active'])

    def test_should_return_fields_on_get_filtering_fields(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            option_data = OptionData()
            option_data._filter_type = OptionDataFilterType.DEFAULT

        actual = option_data.get_filtering_fields()

        self.assertEqual(actual, ['id', 'f_value'])


class FormDataTest(unittest.TestCase):
    @mock.patch.object(DataModel, '__init__', return_value=None)
    def test_should_init_form_data(self, mock_data_model):
        FormData()

        mock_data_model.assert_called_once_with(Relation.FORM_FIELD)

    @mock.patch.object(DataModel, 'add_field', return_value=None)
    def test_should_add_fields_on_add_insert_fields(self, mock_add_field):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            form_data = FormData()

        form_data.add_insert_fields()

        mock_add_field.assert_has_calls([
            call('form', 'form', str, is_optional=False),
            call('field', 'field', str, is_optional=False)
        ])

    @mock.patch.object(DataModel, 'set_data', return_value=None)
    def test_should_set_data_on_data(self, mock_set_data):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            form_data = FormData()

        form_data.on_data({"form_field": "field_value"})

        mock_set_data.assert_called_once_with({"form_field": "field_value"}, True)

    def test_should_return_none_on_add_fields(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            option_data = FormData()

        actual = option_data.add_fields()

        self.assertIsNone(actual)


class FormOptionDataTest(unittest.TestCase):
    @mock.patch.object(DataModel, 'set_data', return_value=None)
    @mock.patch.object(DataModel, '__init__', return_value=None)
    def test_should_init_form_data(self, mock_data_model, mock_set_data):
        FormOptionData(FormType.PLAYER)

        mock_data_model.assert_called_once_with(Relation.OPTION)
        mock_set_data.assert_called_once_with({'is_active': 'true', 'form': ['player', 'general']}, False)

    @mock.patch.object(DataModel, 'set_data', return_value=None)
    @mock.patch.object(DataModel, 'add_field', return_value=None)
    def test_should_add_fields_on_add_insert_fields(self, mock_add_field, _):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            form_data = FormOptionData(FormType.PLAYER)

        form_data.add_fields()

        mock_add_field.assert_has_calls([
            call('b.is_active', 'is_active', bool),
            call('a.is_active', 'is_active', bool),
            call('a.form', 'form', list)
        ])

    def test_should_return_none_on_add_insert_fields(self):
        with mock.patch.object(FormOptionData, '__init__', return_value=None):
            option_data = FormOptionData(FormType.PLAYER)

        actual = option_data.add_insert_fields()

        self.assertIsNone(actual)

    def test_should_return_fields_on_get_querying_fields(self):
        with mock.patch.object(FormOptionData, '__init__', return_value=None):
            form_data = FormOptionData(FormType.PLAYER)
            form_data._filter_type = FormOptionDataFilterType.DEFAULT

        actual = form_data.get_querying_fields()

        self.assertEqual(actual, ['a.form', 'a.is_active', 'b.is_active'])

    def test_should_return_fields_on_get_filtering_fields(self):
        with mock.patch.object(FormOptionData, '__init__', return_value=None):
            option_data = FormOptionData(FormType.PLAYER)
            option_data._filter_type = FormOptionDataFilterType.DEFAULT

        actual = option_data.get_filtering_fields()

        self.assertEqual(actual, ['a.field', 'b.id', 'b.f_value'])

    def test_should_return_fields_on_get_grouping_fields(self):
        with mock.patch.object(FormOptionData, '__init__', return_value=None):
            option_data = FormOptionData(FormType.PLAYER)
            option_data._filter_type = FormOptionDataFilterType.DEFAULT

        actual = option_data.get_grouping_field()

        self.assertEqual(actual, ['a.field'])
