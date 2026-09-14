import datetime
import unittest
from unittest import mock

from src.db_duo import PostgresDbDuo
from src.location.service import LocationServices
from src.option.service import OptionValueService
from src.player.data import PlayerData, PlayerFilterType
from src.player.service import PlayerServices
from src.player_position.service import PlayerPositionServices
from src.responses import RecordNotFoundException
from src.user.service import UserServices


class PlayerServiceTest(unittest.TestCase):

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerData, '__init__', return_value=None)
    def test_should_init_player_service(self,
                                        mock_data,
                                        mock_db):
        actual = PlayerServices()

        mock_data.assert_called_once_with()
        mock_db.assert_called_once()
        args, _ = mock_db.call_args
        self.assertIsInstance(args[0], PlayerData)
        self.assertIsInstance(actual, PlayerServices)

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'insert_record', return_value=True)
    @mock.patch.object(PlayerData, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'update_user', return_value=None)
    @mock.patch.object(UserServices, '__init__', return_value=None)
    def test_should_insert_player_on_create(self,
                                            mock_user_service,
                                            mock_update_user,
                                            mock_player_data,
                                            mock_insert,
                                            mock_db):
        mock_player_data.get.side_effect = ["player_id"]
        with mock.patch.object(PlayerServices, '__init__', return_value=None):
            service = PlayerServices()
            service._data = mock_player_data
            service._db = mock_db
            mock_db.insert_record = mock_insert

        actual = service.create({}, "")

        mock_user_service.assert_called_once_with()
        mock_update_user.assert_called_once_with({'id': '', 'player': 'player_id'}, '')
        mock_player_data.on_data.assert_called_once_with({})
        mock_insert.assert_called_once_with("")

        self.assertEqual("player_id", actual)

    @mock.patch.object(PostgresDbDuo, 'get_records')
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerData, '__init__', return_value=None)
    def test_should_return_player_data_on_get_user_data(self,
                                                        mock_data,
                                                        mock_db,
                                                        mock_get_records):
        mock_get_records.return_value = [{"data": "player_data"}]

        with mock.patch.object(PlayerServices, '__init__', return_value=None):
            service = PlayerServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.get_records = mock_get_records

        actual = service.get_user_data("player_id", "user_id")

        mock_get_records.assert_called_once_with()
        mock_data.on_select.assert_called_once_with({'id': 'player_id', 'is_active': True}, PlayerFilterType.ID)

        self.assertEqual(actual, {"data": "player_data"})

    @mock.patch.object(RecordNotFoundException, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'get_records')
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerData, '__init__', return_value=None)
    def test_should_raise_record_not_found_exception_on_get_user_data(self,
                                                                      mock_data,
                                                                      mock_db,
                                                                      mock_get_records,
                                                                      mock_exception):
        mock_get_records.return_value = []

        with mock.patch.object(PlayerServices, '__init__', return_value=None):
            service = PlayerServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.get_records = mock_get_records

        with self.assertRaises(RecordNotFoundException):
            service.get_user_data("player_id", "user_id")

        mock_get_records.assert_called_once_with()
        mock_data.on_select.assert_called_once_with({'id': 'player_id', 'is_active': True}, PlayerFilterType.ID)

        mock_exception.assert_called_once()

    @mock.patch.object(PostgresDbDuo, 'update_record', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerData, '__init__', return_value=None)
    def test_should_do_update_record_on_update_(self,
                                                mock_data,
                                                mock_db,
                                                mock_update_record):
        with mock.patch.object(PlayerServices, '__init__', return_value=None):
            service = PlayerServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.update_record = mock_update_record

        service.update("player_id", {}, "user_id")

        mock_data.on_data.assert_called_once_with(
            {'id': 'player_id'},
            PlayerFilterType.ID
        )
        mock_update_record.assert_called_once_with('user_id', 'player_id')

    @mock.patch.object(PostgresDbDuo, 'get_records')
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerData, 'get_filtering_fields', return_value=["id"])
    @mock.patch.object(PlayerData, '__init__', return_value=None)
    def test_should_return_player_ids_on_search_by_name(self,
                                                        mock_data,
                                                        mock_get_filtering_fields,
                                                        mock_db,
                                                        mock_get_records):
        mock_get_records.return_value = [{"id": "player_id1"}, {"id": "player_id2"}]

        with mock.patch.object(PlayerServices, '__init__', return_value=None):
            service = PlayerServices()
            service._db = mock_db
            service._data = mock_data
            mock_data.get_filtering_fields = mock_get_filtering_fields
            mock_db.get_records = mock_get_records

        actual = service.search_by_name("text", "user_id")

        mock_get_records.assert_called_once_with()
        mock_data.get_filtering_fields.assert_called_once_with()
        mock_data.on_select.assert_called_once_with({'callName': 'text'}, PlayerFilterType.SEARCH)

        self.assertEqual(actual, ["player_id1", "player_id2"])

    @mock.patch.object(PostgresDbDuo, 'get_records')
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerData, '__init__', return_value=None)
    @mock.patch.object(LocationServices, 'get_location_by_id',
                       return_value={'city': 'city', 'state': 'state', 'country': 'country'})
    @mock.patch.object(LocationServices, '__init__', return_value=None)
    @mock.patch.object(OptionValueService, 'get_option_value_by_ids')
    @mock.patch.object(OptionValueService, '__init__', return_value=None)
    @mock.patch.object(PlayerPositionServices, 'get_positions', return_value=["idP1"])
    @mock.patch.object(PlayerPositionServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_dp_by_player', return_value="dp_id")
    @mock.patch.object(UserServices, '__init__', return_value=None)
    def test_should_return_player_data_on_get_player_info(self,
                                                          mock_user_service,
                                                          mock_get_user_dp,
                                                          mock_player_position_service,
                                                          mock_get_positions,
                                                          mock_option_value_service,
                                                          mock_get_option_value_by_ids,
                                                          mock_location_service,
                                                          mock_get_location,
                                                          mock_data,
                                                          mock_db,
                                                          mock_get_records):
        today = datetime.datetime.now()
        mocked_b_date = datetime.date(today.year - 10, today.month, today.day)
        mock_get_option_value_by_ids.return_value = {"idP1": "position", "idG1": "M"}
        mock_get_records.return_value = [
            {
                "id": "player_id",
                "p_gender": "idG1",
                "p_birth": mocked_b_date,
                "p_location": "idL1",
                'p_call_name': "call_name",
                "p_height": "20",
                "p_weight": "20",
            }
        ]

        with mock.patch.object(PlayerServices, '__init__', return_value=None):
            service = PlayerServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.get_records = mock_get_records

        actual = service.get_player_info("player_id")

        mock_get_records.assert_called_once_with()
        mock_data.on_select.assert_called_once_with({'id': 'player_id', 'is_active': True}, PlayerFilterType.ID)

        mock_user_service.assert_called_once_with()
        mock_get_user_dp.assert_called_once_with("player_id")
        mock_player_position_service.assert_called_once_with()
        mock_get_positions.assert_called_once_with("player_id")
        mock_option_value_service.assert_called_once_with()
        mock_get_option_value_by_ids.assert_called_once_with(['idP1', 'idG1'])
        mock_location_service.assert_called_once_with()
        mock_get_location.assert_called_once_with('idL1')

        self.assertEqual(actual, {'age': 10,
                                  'dp': 'dp_id',
                                  'gender': '20',
                                  'height': '20',
                                  'location': 'city, state, country',
                                  'name': 'call_name',
                                  'positions': ['position'],
                                  'weight': '20'})

    @mock.patch.object(RecordNotFoundException, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'get_records')
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PlayerData, '__init__', return_value=None)
    @mock.patch.object(LocationServices, 'get_location_by_id',
                       return_value={'city': 'city', 'state': 'state', 'country': 'country'})
    @mock.patch.object(LocationServices, '__init__', return_value=None)
    @mock.patch.object(OptionValueService, 'get_option_value_by_ids')
    @mock.patch.object(OptionValueService, '__init__', return_value=None)
    @mock.patch.object(PlayerPositionServices, 'get_positions', return_value=["idP1"])
    @mock.patch.object(PlayerPositionServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_dp_by_player', return_value="dp_id")
    @mock.patch.object(UserServices, '__init__', return_value=None)
    def test_should_raise_record_not_found_exception_on_get_player_info(self,
                                                                        mock_user_service,
                                                                        mock_get_user_dp,
                                                                        mock_player_position_service,
                                                                        mock_get_positions,
                                                                        mock_option_value_service,
                                                                        mock_get_option_value_by_ids,
                                                                        mock_location_service,
                                                                        mock_get_location,
                                                                        mock_data,
                                                                        mock_db,
                                                                        mock_get_records,
                                                                        mock_exception):
        mock_get_records.return_value = []

        with mock.patch.object(PlayerServices, '__init__', return_value=None):
            service = PlayerServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.get_records = mock_get_records

        with self.assertRaises(RecordNotFoundException):
            service.get_player_info("player_id")

        assert not mock_user_service.called
        assert not mock_get_user_dp.called
        assert not mock_player_position_service.called
        assert not mock_get_positions.called
        assert not mock_option_value_service.called
        assert not mock_get_option_value_by_ids.called
        assert not mock_location_service.called
        assert not mock_get_location.called

        mock_get_records.assert_called_once_with()
        mock_data.on_select.assert_called_once_with({'id': 'player_id', 'is_active': True}, PlayerFilterType.ID)

        mock_exception.assert_called_once_with('Get PlayerUserData', 'player_id')
