import unittest
from unittest import mock
from unittest.mock import call

from src.config import Relation
from src.data import DataModel
from src.user.data import UserData, UserFilterType


class UserDataTest(unittest.TestCase):

    @mock.patch.object(DataModel, '__init__', return_value=None)
    def test_should_init_user_data(self, mock_model):
        data = UserData()

        mock_model.assert_called_once_with(Relation.USER)
        self.assertIsInstance(data, UserData)

    @mock.patch.object(DataModel, 'set_data')
    def test_should_call_set_user_data_on_data_with_inserting(self, mock_set):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()

        data.on_data({}, True)

        mock_set.assert_called_once_with({}, True)

    @mock.patch.object(DataModel, 'set_data')
    def test_should_call_set_user_data_on_data_with_non_inserting(self, mock_set):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()

        data.on_data({}, False)

        mock_set.assert_called_once_with({}, False)
        self.assertEqual(data._filter_type, UserFilterType.ID)

    @mock.patch.object(DataModel, 'set_data')
    def test_should_call_set_user_data_on_select(self, mock_set):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()

        data.on_select({}, UserFilterType.DEFAULT)

        mock_set.assert_called_once_with({}, False)
        self.assertEqual(data._filter_type, UserFilterType.DEFAULT)

    @mock.patch.object(DataModel, 'add_field')
    def test_should_add_user_fields_on_add_insert_fields(self, mock_add_field):
        with mock.patch.object(UserData, '__init__', return_value=None):
            UserData().add_insert_fields()

        mock_add_field.assert_has_calls([
            call('u_name', 'name', str, is_optional=False),
            call('dp', 'dp', str)
        ])

    def test_should_return_user_filtering_fields_when_filter_type_id_on_get_filtering_fields(self):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()
            data._filter_type = UserFilterType.ID

        actual = data.get_filtering_fields()

        self.assertEqual(actual, ['u_name', 'dp'])

    def test_should_return_one_when_filter_type_id_on_get_record_count(self):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()
            data._filter_type = UserFilterType.ID

        actual = data.get_record_count()

        self.assertEqual(actual, 1)

    def test_should_return_user_querying_fields_when_filter_type_id_on_get_querying_fields(self):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()
            data._filter_type = UserFilterType.ID

        actual = data.get_querying_fields()

        self.assertEqual(actual, ['id', 'is_active'])

    def test_should_return_empty_list_when_filter_type_is_default_on_get_filtering_fields(self):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()
            data._filter_type = UserFilterType.DEFAULT

        actual = data.get_filtering_fields()

        self.assertEqual(actual, [])

    def test_should_return_none_when_filter_type_is_default_on_get_record_count(self):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()
            data._filter_type = UserFilterType.DEFAULT

        actual = data.get_record_count()

        self.assertIsNone(actual)

    def test_should_return_empty_list_when_filter_type_is_default_on_get_querying_fields(self):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()
            data._filter_type = UserFilterType.DEFAULT

        actual = data.get_querying_fields()

        self.assertEqual(actual, [])

    def test_should_return_empty_list_when_filter_type_is_player_id_on_get_filtering_fields(self):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()
            data._filter_type = UserFilterType.PLAYER_ID

        actual = data.get_filtering_fields()

        self.assertEqual(actual, ['player'])

    def test_should_return_none_when_filter_type_is_player_id_on_get_record_count(self):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()
            data._filter_type = UserFilterType.PLAYER_ID

        actual = data.get_record_count()

        self.assertEqual(actual, 1)

    def test_should_return_empty_list_when_filter_type_is_player_id_on_get_querying_fields(self):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()
            data._filter_type = UserFilterType.PLAYER_ID

        actual = data.get_querying_fields()

        self.assertEqual(actual, ['id', 'is_active'])

    def test_should_return_empty_list_when_filter_type_is_players_on_get_filtering_fields(self):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()
            data._filter_type = UserFilterType.PLAYERS

        actual = data.get_filtering_fields()

        self.assertEqual(actual, ['player', 'u_name', 'dp'])

    def test_should_return_none_when_filter_type_is_players_on_get_record_count(self):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()
            data._filter_type = UserFilterType.PLAYERS

        actual = data.get_record_count()

        self.assertIsNone(actual)

    def test_should_return_empty_list_when_filter_type_is_players_on_get_querying_fields(self):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()
            data._filter_type = UserFilterType.PLAYERS

        actual = data.get_querying_fields()

        self.assertEqual(actual,  ['player', 'is_active'])

    def test_should_return_empty_list_when_filter_type_is_player_dp_on_get_filtering_fields(self):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()
            data._filter_type = UserFilterType.PLAYER_DP

        actual = data.get_filtering_fields()

        self.assertEqual(actual,['dp'])

    def test_should_return_none_when_filter_type_is_player_dp_on_get_record_count(self):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()
            data._filter_type = UserFilterType.PLAYER_DP

        actual = data.get_record_count()

        self.assertIsNone(actual)

    def test_should_return_empty_list_when_filter_type_is_player_dp_on_get_querying_fields(self):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()
            data._filter_type = UserFilterType.PLAYER_DP

        actual = data.get_querying_fields()

        self.assertEqual(actual, ['player', 'is_active'])

    @mock.patch.object(DataModel, 'add_field')
    def test_should_set_fields_on_add_fields(self, mock_add_field):
        with mock.patch.object(UserData, '__init__', return_value=None):
            data = UserData()

        data.add_fields()

        mock_add_field.assert_has_calls([
            call('u_name', "name", str),
            call('dp', "dp", str)
        ])
