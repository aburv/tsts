import unittest
from unittest import mock

from src.config import Relation, Table
from src.data import DataModel, OrderType
from src.responses import DataValidationException


class OrderTypeTest(unittest.TestCase):

    def test_should_instantiate_order_type(self):
        order_type = OrderType("field", True)

        self.assertEqual(order_type.field, "field")
        self.assertEqual(order_type.is_desc, True)


class DataModelTest(unittest.TestCase):

    def test_should_init_device_data(self):
        data = {"key": "value"}

        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)
        model._data = data

        self.assertEqual(model._data, data)
        self.assertEqual(model._fields, {})
        self.assertEqual(model._has_id, False)
        self.assertEqual(model._is_a_record, False)

    def test_should_return_value_by_id_on_get(self):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)
        model._fields = {"d_id": "id"}

        actual = model.get("d_id")

        self.assertEqual(actual, "id")

    @mock.patch.object(DataValidationException, "__init__", return_value=None)
    def test_should_raise_data_validation_exception_in_get_on_unknown_key(self, mock_exception):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)
        model._fields = {"d_id": "id"}

        with self.assertRaises(DataValidationException):
            model.get("id")

        mock_exception.assert_called_once_with('Unable to find', 'id')

    @mock.patch.object(DataModel, "add_insert_fields")
    @mock.patch("uuid.uuid4", return_value="id")
    def test_should_set_data_with_id_and_for_record_for_insert_operation_on_set_data(self, mock_id, mock_add):
        model = DataModel(Relation.INIT, has_id=True, is_a_record=True)

        model.set_data({"dId": "device_id"}, is_new=True)

        mock_add.assert_called_once_with()
        mock_id.assert_called_once_with()
        self.assertEqual(model._fields, {'id': 'id', 'is_active': True})
        self.assertEqual(model._data, {"dId": "device_id"})

    @mock.patch.object(DataModel, "add_insert_fields")
    def test_should_set_data_without_id_and_for_non_record_for_insert_operation_on_set_data(self, mock_add):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)

        model.set_data({"dId": "device_id"}, is_new=True)

        mock_add.assert_called_once_with()
        self.assertEqual(model._fields, {})
        self.assertEqual(model._data, {"dId": "device_id"})

    @mock.patch.object(DataModel, "add_fields")
    def test_should_set_data_for_update_operation_on_set_data(self, mock_add):
        model = DataModel(Relation.INIT, has_id=True, is_a_record=True)

        model.set_data({"dId": "device_id"}, is_new=False)

        mock_add.assert_called_once_with()
        self.assertEqual(model._fields, {})
        self.assertEqual(model._data, {"dId": "device_id"})

    def test_should_raise_not_implemented_on_add_insert_fields(self):
        model = DataModel(Relation.INIT)

        with self.assertRaises(NotImplementedError):
            model.add_insert_fields()

    def test_should_raise_not_implemented_on_add_update_fields(self):
        model = DataModel(Relation.INIT)

        with self.assertRaises(NotImplementedError):
            model.add_fields()

    def test_should_add_validated_field_and_value_on_add_field(self):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)
        model._data = {"dId": "device_id"}

        model.add_field("d_id", "dId", str)

        self.assertEqual(model._fields, {"d_id": "device_id"})

    def test_should_add_validated_field_and_value_by_data_list_on_add_field(self):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)
        model._data = {"dId": "device_id"}

        model.add_field("d_id", "dId", str, data_list=["device_id"])

        self.assertEqual(model._fields, {"d_id": "device_id"})

    @mock.patch.object(DataValidationException, "__init__", return_value=None)
    def test_should_raise_data_validation_exception_on_mismatch_type_in_add_field(self, mock_exception):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)
        model._data = {"dId": "device_id"}

        with self.assertRaises(DataValidationException):
            model.add_field("d_id", "dId", int)

        mock_exception.assert_called_once_with('Improper data values', " {'dId': 'device_id'} d_id device_id")
        self.assertEqual(model._fields, {})

    @mock.patch.object(DataValidationException, "__init__", return_value=None)
    def test_should_raise_data_validation_exception_on_matched_type_but_not_in_list_in_add_field(self, mock_exception):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)
        model._data = {"dId": "device_id"}

        with self.assertRaises(DataValidationException):
            model.add_field("d_id", "dId", str, data_list=["d"])

        mock_exception.assert_called_once_with('Improper data values', " {'dId': 'device_id'} d_id device_id")
        self.assertEqual(model._fields, {})

    @mock.patch.object(DataValidationException, "__init__", return_value=None)
    def test_should_raise_data_validation_exception_on_value_is_empty_on_non_optional_in_add_field(self,
                                                                                                   mock_exception):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)
        model._data = {"dId": ""}

        with self.assertRaises(DataValidationException):
            model.add_field("d_id", "dId", str)

        mock_exception.assert_called_once_with('Improper data values', " {'dId': ''} d_id ")
        self.assertEqual(model._fields, {})

    @mock.patch.object(DataValidationException, "__init__", return_value=None)
    def test_should_raise_data_validation_exception_on_unknown_key_in_add_field(self, mock_exception):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)
        model._data = {"dId": "device_id"}

        with self.assertRaises(DataValidationException):
            model.add_field("d_id", "eId", str, is_optional=False)

        mock_exception.assert_called_once_with('Necessary field not present', "{'dId': 'device_id'} d_id")
        self.assertEqual(model._fields, {})

    def test_should_not_raise_exception_and_not_add_optional_field_on_unknown_key_in_add_field(self):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)
        model._data = {"dId": "device_id"}

        model.add_field("d_id", "eId", str)

        self.assertEqual(model._fields, {})

    def test_should_true_if_fields_are_empty_on_is_empty(self):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)

        self.assertTrue(model.is_empty())

    def test_should_false_if_fields_are_non_empty_on_is_empty(self):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)
        model._fields = {"id": "id"}

        self.assertFalse(model.is_empty())

    def test_should_assert_payload_without_id_on_get_audit_payload(self):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)
        model._fields = {"id": "id", "d_id": "device_id"}
        expected = {"d_id": "device_id"}

        actual = model.get_audit_payload()

        self.assertEqual(actual, expected)

    @mock.patch.object(DataModel, 'get_filtering_fields', return_value=['field_1', 'field_2'])
    def test_should_return_list_of_records_on_frame_records(self, mock_filter_fields):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)

        expected = [{'field_1': 'value_1', 'field_2': 'value_2'}, {'field_1': 'value_3', 'field_2': 'value_4'}]
        actual = model.frame_records((('value_1', 'value_2'), ('value_3', 'value_4'),))

        mock_filter_fields.assert_called_once_with()
        self.assertEqual(expected, actual)

    def test_should_return_empty_list_on_get_querying_fields(self):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)

        actual = model.get_querying_fields()

        self.assertEqual([], actual)

    def test_should_return_empty_list_on_get_filtering_fields(self):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)

        actual = model.get_filtering_fields()

        self.assertEqual([], actual)

    def test_should_return_none_on_get_record_count(self):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)

        actual = model.get_record_count()

        self.assertIsNone(actual)

    def test_should_return_none_on_get_grouping_field(self):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)

        actual = model.get_grouping_field()

        self.assertIsNone(actual)

    def test_should_return_none_on_get_ordering_type(self):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)

        actual = model.get_ordering_type()

        self.assertIsNone(actual)

    @mock.patch.object(DataModel, 'get_querying_fields', return_value=[])
    def test_should_return_none_when_query_fields_is_empty_on_get_querying_fields_and_value(self,
                                                                                            mock_get_querying_fields):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)

        actual = model.get_querying_fields_and_value()

        mock_get_querying_fields.assert_called_once_with()
        self.assertIsNone(actual)

    @mock.patch.object(DataModel, 'get_querying_fields', return_value=['field_1', 'field_2'])
    def test_should_return_query_fields_and_values_on_get_querying_fields_and_value(self,
                                                                                    mock_get_querying_fields):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)
        model._fields = {'field_1': 'value1', 'field_2': 'value2', 'field_3': 'value3', 'field_4': 'value4'}

        actual = model.get_querying_fields_and_value()

        mock_get_querying_fields.assert_called_once_with()
        self.assertEqual({'field_1': 'value1', 'field_2': 'value2'}, actual)

    @mock.patch.object(Table, '__init__', return_value=None)
    def test_should_return_table_name_on_get_table_name(self, mock_table):
        mock_table.get_name.return_value = "table"
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)
        model.table = mock_table

        actual = model.get_table_name()

        mock_table.get_name.assert_called_once_with()
        self.assertEqual("table", actual)

    def test_should_return_fields_on_get_fields(self):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)
        model._fields = {'field1': 'value1', 'field2': 'value2', 'field3': 'value3'}

        actual = model.get_fields()

        self.assertEqual(['field1', 'field2', 'field3'], actual)

    def test_should_return_values_on_get_values(self):
        model = DataModel(Relation.INIT, has_id=False, is_a_record=False)
        model._fields = {'field1': 'value1', 'field2': 'value2', 'field3': 'value3'}

        actual = model.get_values()

        self.assertEqual(['value1', 'value2', 'value3'], actual)
