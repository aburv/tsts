import unittest
from unittest import mock
from unittest.mock import call

from src.config import Relation
from src.data import DataModel
from src.player.data import PlayerData, PlayerFilterType


class PlayerDataTest(unittest.TestCase):

    @mock.patch.object(DataModel, '__init__', return_value=None)
    def test_should_init_player_data(self, mock_model):
        data = PlayerData()

        mock_model.assert_called_once_with(Relation.PLAYER)
        self.assertIsInstance(data, PlayerData)

    @mock.patch.object(DataModel, 'set_data')
    def test_should_call_set_player_data_on_data(self, mock_set):
        with mock.patch.object(PlayerData, '__init__', return_value=None):
            data = PlayerData()

        data.on_data({})

        mock_set.assert_called_once_with({}, True)

    @mock.patch.object(DataModel, 'set_data')
    def test_should_call_set_player_data_on_select(self, mock_set):
        with mock.patch.object(PlayerData, '__init__', return_value=None):
            data = PlayerData()

        data.on_select({})

        mock_set.assert_called_once_with({}, is_new=False)
        self.assertEqual(PlayerFilterType.DEFAULT, data._filter_type)

    @mock.patch.object(DataModel, 'add_field')
    def test_should_add_player_on_add_insert_fields(self, mock_add_field):
        with mock.patch.object(PlayerData, '__init__', return_value=None):
            PlayerData().add_insert_fields()

        mock_add_field.assert_has_calls([
            call('p_call_name', 'callName', str, is_optional=False),
            call('p_blood_group', 'bloodGroup', str, is_optional=False),
            call('p_gender', 'gender', str, is_optional=False),
            call('p_birth', 'birthDate', str, is_optional=False, validate_type='date'),
            call('p_weight', 'weight', float, is_optional=False),
            call('p_height', 'height', float, is_optional=False),
            call('p_location', 'locationId', str)
        ])

    @mock.patch.object(DataModel, 'add_field')
    def test_should_add_player_on_add_fields(self, mock_add_field):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            option_data = PlayerData()

        option_data.add_fields()

        mock_add_field.assert_has_calls([
            call('id', 'id', str),
            call('p_call_name', 'callName', str),
            call('p_blood_group', 'bloodGroup', str),
            call('p_gender', 'gender', str),
            call('p_birth', 'birthDate', str),
            call('p_weight', 'weight', float),
            call('p_height', 'height', float),
            call('p_location', 'locationId', str),
            call('is_active', 'is_active', bool)
        ])

    def test_should_return_player_id_when_filter_type_is_id_on_get_querying_fields(self):
        with mock.patch.object(PlayerData, '__init__', return_value=None):
            data = PlayerData()
            data._filter_type = PlayerFilterType.ID

        actual = data.get_querying_fields()

        self.assertEqual(actual, ['id', 'is_active'])

    def test_should_return_player_id_when_filter_type_is_id_on_get_filtering_fields(self):
        with mock.patch.object(PlayerData, '__init__', return_value=None):
            data = PlayerData()
            data._filter_type = PlayerFilterType.ID

        actual = data.get_filtering_fields()

        self.assertEqual(
            actual,
            ["p_call_name", "p_blood_group", "p_birth", "p_weight", "p_height", "p_location", "p_gender"]
        )

    def test_should_return_one_when_filter_type_is_id_on_get_record_count(self):
        with mock.patch.object(PlayerData, '__init__', return_value=None):
            data = PlayerData()
            data._filter_type = PlayerFilterType.ID

        actual = data.get_record_count()

        self.assertEqual(actual, 1)

    def test_should_return_player_when_filter_type_is_empty_on_get_querying_fields(self):
        with mock.patch.object(PlayerData, '__init__', return_value=None):
            data = PlayerData()
            data._filter_type = PlayerFilterType.DEFAULT

        actual = data.get_querying_fields()

        self.assertEqual(actual, [])

    def test_should_return_player_when_filter_type_is_empty_on_get_filtering_fields(self):
        with mock.patch.object(PlayerData, '__init__', return_value=None):
            data = PlayerData()
            data._filter_type = PlayerFilterType.DEFAULT

        actual = data.get_filtering_fields()

        self.assertEqual(
            actual,
            ["p_call_name", "p_blood_group", "p_birth", "p_weight", "p_height", "p_location", "p_gender"]
        )

    def test_should_return_none_when_filter_type_is_empty_on_get_record_count(self):
        with mock.patch.object(PlayerData, '__init__', return_value=None):
            data = PlayerData()
            data._filter_type = PlayerFilterType.DEFAULT

        actual = data.get_record_count()

        self.assertIsNone(actual)

    def test_should_return_p_call_name_when_filter_type_search_on_get_querying_fields(self):
        with mock.patch.object(PlayerData, '__init__', return_value=None):
            data = PlayerData()
            data._filter_type = PlayerFilterType.SEARCH

        actual = data.get_querying_fields()

        self.assertEqual(actual, ['p_call_name'])

    def test_should_return_id_when_filter_type_search_on_get_filtering_fields(self):
        with mock.patch.object(PlayerData, '__init__', return_value=None):
            data = PlayerData()
            data._filter_type = PlayerFilterType.SEARCH

        actual = data.get_filtering_fields()

        self.assertEqual(
            actual,
            ['id']
        )

    def test_should_return_none_when_filter_type_is_search_on_get_record_count(self):
        with mock.patch.object(PlayerData, '__init__', return_value=None):
            data = PlayerData()
            data._filter_type = PlayerFilterType.SEARCH

        actual = data.get_record_count()

        self.assertIsNone(actual)

    def test_should_return_true_when_filter_type_is_search_on_s_on_search(self):
        with mock.patch.object(PlayerData, '__init__', return_value=None):
            data = PlayerData()
            data._filter_type = PlayerFilterType.SEARCH

        actual = data.is_on_search()

        self.assertTrue(actual)

    def test_should_return_false_when_filter_type_is_not_search_on_is_on_search(self):
        with mock.patch.object(PlayerData, '__init__', return_value=None):
            data = PlayerData()
            data._filter_type = PlayerFilterType.DEFAULT

        actual = data.is_on_search()

        self.assertFalse(actual)
