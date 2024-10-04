import unittest
from unittest import mock

from src.data import DataModel
from src.responses import DataValidationException


class DataModelTest(unittest.TestCase):

    def test_should_init_device_data(self):
        data = {"key": "value"}

        model = DataModel(data)

        self.assertEqual(model._data, data)
        self.assertEqual(model._fields, {})

    def test_should_return_value_by_id_on_get(self):
        model = DataModel({})
        model._fields = {"d_id": "id"}

        actual = model.get("d_id")

        self.assertEqual(actual, "id")

    @mock.patch.object(DataValidationException, "__init__", return_value=None)
    def test_should_raise_data_validation_exception_in_get_on_unknown_key(self, mock_exception):
        model = DataModel({})
        model._fields = {"d_id": "id"}

        with self.assertRaises(DataValidationException):
            model.get("id")

        mock_exception.assert_called_once_with('Unable to find', 'id')

    @mock.patch("uuid.uuid4", return_value="d_id")
    def test_should_return_insert_data_on_get_insert_payload(self, mock_id):
        model = DataModel({})
        model._fields = {"d_id": "id"}

        actual = model.get_insert_payload()

        mock_id.assert_called_once_with()
        self.assertEqual(actual, {'d_id': 'id', 'id': 'd_id', 'is_active': True})

    def test_should_return_update_data_on_get_update_payload(self):
        model = DataModel({})
        model._fields = {"d_id": "id"}

        actual = model.get_update_payload()

        self.assertEqual(actual, {'d_id': 'id'})

    def test_should_add_validated_field_and_value_on_add_field(self):
        model = DataModel({"dId": "device_id"})

        model.add_field("d_id", "dId", str)

        self.assertEqual(model._fields, {"d_id": "device_id"})

    @mock.patch.object(DataValidationException, "__init__", return_value=None)
    def test_should_raise_data_validation_exception_on_mismatch_type_in_add_field(self, mock_exception):
        model = DataModel({"dId": "device_id"})

        with self.assertRaises(DataValidationException):
            model.add_field("d_id", "dId", int)

        mock_exception.assert_called_once_with('Improper data values', " {'dId': 'device_id'} d_id device_id")
        self.assertEqual(model._fields, {})

    @mock.patch.object(DataValidationException, "__init__", return_value=None)
    def test_should_raise_data_validation_exception_on_unknown_key_in_add_field(self, mock_exception):
        model = DataModel({"dId": "device_id"})

        with self.assertRaises(DataValidationException):
            model.add_field("d_id", "eId", str, is_optional=False)

        mock_exception.assert_called_once_with('Necessary field not present', "{'dId': 'device_id'} d_id")
        self.assertEqual(model._fields, {})

    def test_should_not_add_optional_field_on_unknown_key_in_add_field(self):
        model = DataModel({"dId": "device_id"})

        model.add_field("d_id", "eId", str)

        self.assertEqual(model._fields, {})

    def test_should_true_if_fields_are_empty_on_is_empty(self):
        model = DataModel({"dId": "device_id"})

        self.assertTrue(model.is_empty())

    def test_should_false_if_fields_are_non_empty_on_is_empty(self):
        model = DataModel({"dId": "device_id"})
        model._fields = {"id": "id"}

        self.assertFalse(model.is_empty())
