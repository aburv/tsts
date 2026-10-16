import unittest
from unittest import mock

from src.db_duo import PostgresDbDuo
from src.player_position.data import PlayerPositionData, PlayerPositionFilterType
from src.player_position.service import PlayerPositionServices


class PlayerPositionServiceTest(unittest.TestCase):

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerPositionData, '__init__', return_value=None)
    def test_should_init_player_position_service(self,
                                                 mock_data,
                                                 mock_db):
        actual = PlayerPositionServices()

        mock_data.assert_called_once_with()
        mock_db.assert_called_once()
        args, _ = mock_db.call_args
        self.assertIsInstance(args[0], PlayerPositionData)
        self.assertIsInstance(actual, PlayerPositionServices)

    @mock.patch.object(PostgresDbDuo, 'get_records', return_value=[{"p_position": "position"}])
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerPositionData, '__init__', return_value=None)
    def test_should_return_positions_on_get_positions_id(self,
                                                         mock_data,
                                                         mock_db,
                                                         mock_get_records):
        with mock.patch.object(PlayerPositionServices, '__init__', return_value=None):
            service = PlayerPositionServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.get_records = mock_get_records

        actual = service.get_positions("player_id")

        mock_data.on_select.assert_called_once_with({'player': 'player_id'})
        mock_get_records.assert_called_once_with()

        self.assertEqual(actual, ["position"])

    @mock.patch.object(PostgresDbDuo, 'insert_record', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerPositionData, '__init__', return_value=None)
    def test_should_do_insert_position_on_create_position(self,
                                                          mock_data,
                                                          mock_db,
                                                          mock_insert_record):
        with mock.patch.object(PlayerPositionServices, '__init__', return_value=None):
            service = PlayerPositionServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.insert_record = mock_insert_record

        service.create_position("player_id", "position", "user_id")

        mock_data.on_data.assert_called_once_with({'player': 'player_id', 'position': 'position', 'percent': 0})
        mock_insert_record.assert_called_once_with('user_id', 'player_id')

    @mock.patch.object(PostgresDbDuo, 'update_record', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerPositionData, '__init__', return_value=None)
    def test_should_do_update_position_on_update_position(self,
                                                          mock_data,
                                                          mock_db,
                                                          mock_update_record):
        with mock.patch.object(PlayerPositionServices, '__init__', return_value=None):
            service = PlayerPositionServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.update_record = mock_update_record

        service.update_position_delta("player_id", "position", 90, "user_id")

        mock_data.on_data.assert_called_once_with(
            {'player': 'player_id', 'position': 'position', 'percent': 90},
            PlayerPositionFilterType.POSITION
        )
        mock_update_record.assert_called_once_with('user_id', 'player_id')
