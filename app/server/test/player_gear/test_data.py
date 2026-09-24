import unittest
from unittest import mock
from unittest.mock import call

from src.config import Relation
from src.data import DataModel
from src.player_gear.data import PlayerGearData, PlayerGearFilterType


class PlayerGearDataTest(unittest.TestCase):

    @mock.patch.object(DataModel, '__init__', return_value=None)
    def test_should_init_player_data(self, mock_model):
        data = PlayerGearData()

        mock_model.assert_called_once_with(Relation.T_PLAYER, has_id=False, is_a_record=False)
        self.assertIsInstance(data, PlayerGearData)

    @mock.patch.object(DataModel, 'set_data')
    def test_should_call_set_player_data_on_data(self, mock_set):
        with mock.patch.object(PlayerGearData, '__init__', return_value=None):
            data = PlayerGearData()

        data.on_data({})

        mock_set.assert_called_once_with({}, False)

    @mock.patch.object(DataModel, 'set_data')
    def test_should_call_set_player_data_on_select(self, mock_set):
        with mock.patch.object(PlayerGearData, '__init__', return_value=None):
            data = PlayerGearData()

        data.on_select({}, PlayerGearFilterType.ID)

        mock_set.assert_called_once_with({}, is_new=False)
        self.assertEqual(PlayerGearFilterType.ID, data._filter_type)

    @mock.patch.object(DataModel, 'add_field')
    def test_should_add_player_on_add_insert_fields(self, mock_add_field):
        with mock.patch.object(PlayerGearData, '__init__', return_value=None):
            PlayerGearData().add_insert_fields()

        mock_add_field.assert_has_calls([
            call('t_player', 'player', str, is_optional=False),
            call('p_jersey_name', 'jName', str, is_optional=False),
            call('p_jersey_number', 'jNo', str, is_optional=False),
            call('p_jersey_size', 'jSize', str, is_optional=False),
            call('p_shoe_size', 'sSize', str, is_optional=False)
        ])

    @mock.patch.object(DataModel, 'add_field')
    def test_should_add_player_on_add_fields(self, mock_add_field):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            option_data = PlayerGearData()

        option_data.add_fields()

        mock_add_field.assert_has_calls([
            call('t_player', 'player', str),
            call('p_jersey_name', 'jName', str),
            call('p_jersey_number', 'jNo', str),
            call('p_jersey_size', 'jSize', str),
            call('p_shoe_size', 'sSize', str)
        ])

    def test_should_return_player_id_when_filter_type_is_id_on_get_querying_fields(self):
        with mock.patch.object(PlayerGearData, '__init__', return_value=None):
            data = PlayerGearData()
            data._filter_type = PlayerGearFilterType.ID

        actual = data.get_querying_fields()

        self.assertEqual(actual, ['t_player'])

    def test_should_return_player_id_when_filter_type_is_id_on_get_filtering_fields(self):
        with mock.patch.object(PlayerGearData, '__init__', return_value=None):
            data = PlayerGearData()
            data._filter_type = PlayerGearFilterType.ID

        actual = data.get_filtering_fields()

        self.assertEqual(
            actual,
            ['p_jersey_name', 'p_jersey_number', 'p_jersey_size', 'p_shoe_size']
        )

    def test_should_return_one_when_filter_type_is_id_on_get_record_count(self):
        with mock.patch.object(PlayerGearData, '__init__', return_value=None):
            data = PlayerGearData()
            data._filter_type = PlayerGearFilterType.ID

        actual = data.get_record_count()

        self.assertEqual(actual, 1)

    def test_should_return_p_call_name_when_filter_type_search_on_get_querying_fields(self):
        with mock.patch.object(PlayerGearData, '__init__', return_value=None):
            data = PlayerGearData()
            data._filter_type = PlayerGearFilterType.SEARCH

        actual = data.get_querying_fields()

        self.assertEqual(actual, ['p_jersey_name', 'p_jersey_number'])

    def test_should_return_id_when_filter_type_search_on_get_filtering_fields(self):
        with mock.patch.object(PlayerGearData, '__init__', return_value=None):
            data = PlayerGearData()
            data._filter_type = PlayerGearFilterType.SEARCH

        actual = data.get_filtering_fields()

        self.assertEqual(
            actual,
            ['t_player']
        )

    def test_should_return_none_when_filter_type_is_search_on_get_record_count(self):
        with mock.patch.object(PlayerGearData, '__init__', return_value=None):
            data = PlayerGearData()
            data._filter_type = PlayerGearFilterType.SEARCH

        actual = data.get_record_count()

        self.assertIsNone(actual)

    def test_should_return_true_when_filter_type_is_search_on_s_on_search(self):
        with mock.patch.object(PlayerGearData, '__init__', return_value=None):
            data = PlayerGearData()
            data._filter_type = PlayerGearFilterType.SEARCH

        actual = data.is_on_search()

        self.assertTrue(actual)

    def test_should_return_false_when_filter_type_is_not_search_on_is_on_search(self):
        with mock.patch.object(PlayerGearData, '__init__', return_value=None):
            data = PlayerGearData()
            data._filter_type = PlayerGearFilterType.ID

        actual = data.is_on_search()

        self.assertFalse(actual)
