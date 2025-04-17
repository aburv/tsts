import unittest
from unittest import mock
from unittest.mock import call

from src.config import Relation
from src.data import DataModel
from src.user_id.data import UserIDData


class UserIDDataTest(unittest.TestCase):

    @mock.patch.object(DataModel, '__init__', return_value=None)
    def test_should_init_user_id_data(self, mock_model):
        data = UserIDData()

        mock_model.assert_called_once_with(Relation.UID, has_id=False, is_a_record=False)
        self.assertIsInstance(data, UserIDData)

    @mock.patch.object(DataModel, 'set_data')
    def test_should_call_set_user_id_data_on_data(self, mock_set):
        with mock.patch.object(UserIDData, '__init__', return_value=None):
            data = UserIDData()

        data.on_data({})

        mock_set.assert_called_once_with({}, True)

    @mock.patch.object(DataModel, 'set_data')
    def test_should_call_set_user_id_data_on_select(self, mock_set):
        with mock.patch.object(UserIDData, '__init__', return_value=None):
            data = UserIDData()

        data.on_select({}, "f_type")

        mock_set.assert_called_once_with({}, False)
        self.assertEqual(data._filter_type, "f_type")

    @mock.patch.object(DataModel, 'add_field')
    def test_should_add_user_id_on_add_insert_fields(self, mock_add_field):
        with mock.patch.object(UserIDData, '__init__', return_value=None):
            data = UserIDData()

        data.add_insert_fields()

        mock_add_field.assert_has_calls([
            call('t_user', 'user', str, is_optional=False),
            call('val', 'value', str, is_optional=False),
            call('type', 'type', str, is_optional=False, data_list=['P', 'M']),
            call('g_id', 'gId', str, is_optional=False),
            call('is_verified', 'isVerified', bool, is_optional=False),
        ])

    def test_should_return_user_id_querying_fields_when_filter_type_is_none_on_get_querying_fields(self):
        with mock.patch.object(UserIDData, '__init__', return_value=None):
            id_data = UserIDData()
            id_data._filter_type = None

        actual = id_data.get_querying_fields()

        self.assertEqual(actual, ["t_user", "is_verified"])

    def test_should_return_user_id_querying_fields_when_filter_type_is_id_on_get_querying_fields(self):
        with mock.patch.object(UserIDData, '__init__', return_value=None):
            id_data = UserIDData()
            id_data._filter_type = "id"

        actual = id_data.get_querying_fields()

        self.assertEqual(actual, ["val", "g_id", "is_verified"])

    def test_should_return_user_id_filtering_fields_when_filter_type_is_none_on_get_filtering_fields(self):
        with mock.patch.object(UserIDData, '__init__', return_value=None):
            id_data = UserIDData()
            id_data._filter_type = None
        actual = id_data.get_filtering_fields()

        self.assertEqual(actual, ["val", "type"])

    def test_should_return_user_id_filtering_fields_when_filter_type_is_id_on_get_filtering_fields(self):
        with mock.patch.object(UserIDData, '__init__', return_value=None):
            id_data = UserIDData()
            id_data._filter_type = "id"
        actual = id_data.get_filtering_fields()

        self.assertEqual(actual, ['t_user'])

    def test_should_return_one_when_filter_type_is_id_on_get_record_count(self):
        with mock.patch.object(UserIDData, '__init__', return_value=None):
            id_data = UserIDData()
            id_data._filter_type = "id"
        actual = id_data.get_record_count()

        self.assertEqual(actual, 1)

    def test_should_return_none_when_filter_type_is_none_on_get_record_count(self):
        with mock.patch.object(UserIDData, '__init__', return_value=None):
            id_data = UserIDData()
            id_data._filter_type = None
        actual = id_data.get_record_count()

        self.assertIsNone(actual)

    @mock.patch.object(DataModel, 'add_field')
    def test_should_set_fields_on_add_fields(self, mock_add_field):
        with mock.patch.object(UserIDData, '__init__', return_value=None):
            data = UserIDData()

        data.add_fields()

        mock_add_field.assert_has_calls([
            call('t_user', 'user', str),
            call('val', 'value', str),
            call('g_id', "gId", str),
            call('is_verified', 'isVerified', bool)
        ])
