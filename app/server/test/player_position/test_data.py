import unittest
from unittest import mock
from unittest.mock import call

from src.config import Relation
from src.data import DataModel
from src.player_position.data import PlayerPositionData, PlayerPositionFilterType


class PlayerPositionDataTest(unittest.TestCase):

    @mock.patch.object(DataModel, '__init__', return_value=None)
    def test_should_init_player_data(self, mock_model):
        data = PlayerPositionData()

        mock_model.assert_called_once_with(Relation.PLAYER_POSITION, has_id=False, is_a_record=False)
        self.assertIsInstance(data, PlayerPositionData)

    @mock.patch.object(DataModel, 'set_data')
    def test_should_call_set_player_data_on_data(self, mock_set):
        with mock.patch.object(PlayerPositionData, '__init__', return_value=None):
            data = PlayerPositionData()

        data.on_data({})

        mock_set.assert_called_once_with({}, False)

    @mock.patch.object(DataModel, 'set_data')
    def test_should_call_set_player_data_on_select(self, mock_set):
        with mock.patch.object(PlayerPositionData, '__init__', return_value=None):
            data = PlayerPositionData()

        data.on_select({})

        mock_set.assert_called_once_with({}, is_new=False)
        self.assertEqual(PlayerPositionFilterType.DEFAULT, data._filter_type)

    @mock.patch.object(DataModel, 'add_field')
    def test_should_add_player_on_add_insert_fields(self, mock_add_field):
        with mock.patch.object(PlayerPositionData, '__init__', return_value=None):
            PlayerPositionData().add_insert_fields()

        mock_add_field.assert_has_calls([
            call('t_player', 'player', str, is_optional=False),
            call('p_position', 'position', str, is_optional=False),
            call('delta', 'percent', float, is_optional=False)
        ])

    @mock.patch.object(DataModel, 'add_field')
    def test_should_add_player_on_add_fields(self, mock_add_field):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            option_data = PlayerPositionData()

        option_data.add_fields()

        mock_add_field.assert_has_calls([
            call('t_player', 'player', str),
            call('p_position', 'position', str),
            call('delta', 'percent', float)
        ])

    def test_should_return_player_when_filter_type_is_empty_on_get_querying_fields(self):
        with mock.patch.object(PlayerPositionData, '__init__', return_value=None):
            data = PlayerPositionData()
            data._filter_type = PlayerPositionFilterType.DEFAULT

        actual = data.get_querying_fields()

        self.assertEqual(actual, ['t_player'])

    def test_should_return_player_when_filter_type_is_empty_on_get_filtering_fields(self):
        with mock.patch.object(PlayerPositionData, '__init__', return_value=None):
            data = PlayerPositionData()
            data._filter_type = PlayerPositionFilterType.DEFAULT

        actual = data.get_filtering_fields()

        self.assertEqual(
            actual,
            ['p_position']
        )

    def test_should_return_none_when_filter_type_is_empty_on_get_record_count(self):
        with mock.patch.object(PlayerPositionData, '__init__', return_value=None):
            data = PlayerPositionData()
            data._filter_type = PlayerPositionFilterType.DEFAULT

        actual = data.get_record_count()

        self.assertIsNone(actual)

    def test_should_return_p_call_name_when_filter_type_position_on_get_querying_fields(self):
        with mock.patch.object(PlayerPositionData, '__init__', return_value=None):
            data = PlayerPositionData()
            data._filter_type = PlayerPositionFilterType.POSITION

        actual = data.get_querying_fields()

        self.assertEqual(actual, ['t_player', 'p_position'])

    def test_should_return_id_when_filter_type_position_on_get_filtering_fields(self):
        with mock.patch.object(PlayerPositionData, '__init__', return_value=None):
            data = PlayerPositionData()
            data._filter_type = PlayerPositionFilterType.POSITION

        actual = data.get_filtering_fields()

        self.assertEqual(
            actual,
            ['delta']
        )

    def test_should_return_none_when_filter_type_is_position_on_get_record_count(self):
        with mock.patch.object(PlayerPositionData, '__init__', return_value=None):
            data = PlayerPositionData()
            data._filter_type = PlayerPositionFilterType.POSITION

        actual = data.get_record_count()

        self.assertIsNone(actual)
