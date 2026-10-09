import unittest
from unittest import mock

from src.db_duo import PostgresDbDuo
from src.player_gear.data import PlayerGearData, PlayerGearFilterType
from src.player_gear.service import PlayerGearServices
from src.responses import RecordNotFoundException


class PlayerPositionServiceTest(unittest.TestCase):

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerGearData, '__init__', return_value=None)
    def test_should_init_player_gear_service(self,
                                             mock_data,
                                             mock_db):
        actual = PlayerGearServices()

        mock_data.assert_called_once_with()
        mock_db.assert_called_once()
        args, _ = mock_db.call_args
        self.assertIsInstance(args[0], PlayerGearData)
        self.assertIsInstance(actual, PlayerGearServices)

    @mock.patch.object(PostgresDbDuo, 'get_records', return_value=[{"id": "player_id"}])
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerGearData, '__init__', return_value=None)
    def test_should_return_player_gear_data_on_get_by_id(self,
                                                         mock_data,
                                                         mock_db,
                                                         mock_get_records):
        with mock.patch.object(PlayerGearServices, '__init__', return_value=None):
            service = PlayerGearServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.get_records = mock_get_records

        actual = service.get_by_id("player_id")

        mock_data.on_select.assert_called_once_with({'player': 'player_id'}, PlayerGearFilterType.ID)
        mock_get_records.assert_called_once_with()

        self.assertEqual(actual, {"id": "player_id"})

    @mock.patch.object(RecordNotFoundException, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'get_records', return_value=[])
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerGearData, '__init__', return_value=None)
    def test_should_raise_record_not_found_exception_on_get_by_id(self,
                                                                  mock_data,
                                                                  mock_db,
                                                                  mock_get_records,
                                                                  mock_exception):
        with mock.patch.object(PlayerGearServices, '__init__', return_value=None):
            service = PlayerGearServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.get_records = mock_get_records

        with self.assertRaises(RecordNotFoundException):
            service.get_by_id("player_id")

        mock_data.on_select.assert_called_once_with({'player': 'player_id'}, PlayerGearFilterType.ID)
        mock_get_records.assert_called_once_with()
        mock_exception.assert_called_once_with('Get PlayerData', 'player_id')

    @mock.patch.object(PostgresDbDuo, 'insert_record', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerGearData, '__init__', return_value=None)
    def test_should_do_insert_record_on_create(self,
                                               mock_data,
                                               mock_db,
                                               mock_insert_record):
        with mock.patch.object(PlayerGearServices, '__init__', return_value=None):
            service = PlayerGearServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.insert_record = mock_insert_record

        service.create("player_id", {}, "user_id")

        mock_data.on_data.assert_called_once_with({'player': 'player_id'})
        mock_insert_record.assert_called_once_with('user_id', 'player_id')

    @mock.patch.object(PostgresDbDuo, 'update_record', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerGearData, '__init__', return_value=None)
    def test_should_do_update_record_on_update(self,
                                               mock_data,
                                               mock_db,
                                               mock_update_record):
        with mock.patch.object(PlayerGearServices, '__init__', return_value=None):
            service = PlayerGearServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.update_record = mock_update_record

        service.update("player_id", {}, "user_id")

        mock_data.on_data.assert_called_once_with(
            {'player': 'player_id'},
            PlayerGearFilterType.ID
        )
        mock_update_record.assert_called_once_with('user_id', 'player_id')

    @mock.patch.object(PlayerGearServices, 'get_by_id')
    def test_should_return_false_on_check_presence(self,
                                                   mock_get_by_id):
        with mock.patch.object(RecordNotFoundException, '__init__', return_value=None):
            mock_get_by_id.side_effect = RecordNotFoundException("player", "player_id")

        with mock.patch.object(PlayerGearServices, '__init__', return_value=None):
            service = PlayerGearServices()

        actual = service.check_presence("player_id")

        mock_get_by_id.assert_called_once_with("player_id")
        self.assertFalse(actual)

    @mock.patch.object(PlayerGearServices, 'get_by_id')
    def test_should_return_true_on_check_presence(self,
                                                  mock_get_by_id):
        with mock.patch.object(PlayerGearServices, '__init__', return_value=None):
            service = PlayerGearServices()

        actual = service.check_presence("player_id")

        mock_get_by_id.assert_called_once_with("player_id")
        self.assertTrue(actual)

    @mock.patch.object(PostgresDbDuo, 'get_records', return_value=[{"id": "player_id"}])
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerGearData, 'get_filtering_fields', return_value=["id"])
    @mock.patch.object(PlayerGearData, '__init__', return_value=None)
    def test_should_return_player_ids_on_search_by_j_name_j_no(self,
                                                               mock_data,
                                                               mock_get_filtering_fields,
                                                               mock_db,
                                                               mock_get_records):
        with mock.patch.object(PlayerGearServices, '__init__', return_value=None):
            service = PlayerGearServices()
            service._db = mock_db
            service._data = mock_data
            mock_data.get_filtering_fields = mock_get_filtering_fields
            mock_db.get_records = mock_get_records

        actual = service.search_by_j_name_j_no("text", "user_id")

        mock_data.on_select.assert_called_once_with({'jName': 'text', 'jNo': 'text'}, PlayerGearFilterType.SEARCH)
        mock_data.get_filtering_fields.assert_called_once_with()
        mock_get_records.assert_called_once_with()

        self.assertEqual(actual, ["player_id"])
